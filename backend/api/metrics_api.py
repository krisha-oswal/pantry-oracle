"""
Metrics API endpoints for Pantry Oracle
"""

from flask import Blueprint, jsonify, request
from services.metrics_tracker import MetricsTracker
import logging

logger = logging.getLogger(__name__)

# Create blueprint
metrics_bp = Blueprint('metrics', __name__, url_prefix='/api/metrics')

# Initialize metrics tracker
metrics_tracker = MetricsTracker()


@metrics_bp.route('/summary', methods=['GET'])
def get_summary():
    """
    Get summary statistics
    Query params: days (default: 7)
    """
    try:
        days = int(request.args.get('days', 7))
        summary = metrics_tracker.get_summary_stats(days=days)
        return jsonify(summary), 200
    except Exception as e:
        logger.error(f"Error getting summary: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/performance', methods=['GET'])
def get_performance():
    """Get performance metrics"""
    try:
        performance = metrics_tracker.get_performance_metrics()
        return jsonify(performance), 200
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/satisfaction', methods=['GET'])
def get_satisfaction():
    """Get user satisfaction metrics"""
    try:
        satisfaction = metrics_tracker.get_user_satisfaction_metrics()
        return jsonify(satisfaction), 200
    except Exception as e:
        logger.error(f"Error getting satisfaction metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit user feedback
    Request: {
        "recipe_id": 123,
        "feedback_type": "relevance",
        "rating": 4,
        "comment": "Great recipe!"
    }
    """
    try:
        data = request.get_json()
        
        recipe_id = data.get('recipe_id')
        feedback_type = data.get('feedback_type')
        rating = data.get('rating')
        comment = data.get('comment')
        
        if not all([recipe_id, feedback_type, rating]):
            return jsonify({"error": "Missing required fields"}), 400
        
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400
        
        metrics_tracker.track_user_feedback(
            recipe_id=recipe_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment
        )
        
        return jsonify({"message": "Feedback submitted successfully"}), 200
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/export', methods=['GET'])
def export_metrics():
    """Export all metrics to a file"""
    try:
        output_file = 'data/metrics/metrics_export.json'
        metrics_tracker.export_metrics(output_file)
        return jsonify({
            "message": "Metrics exported successfully",
            "file": output_file
        }), 200
    except Exception as e:
        logger.error(f"Error exporting metrics: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/analytics/anomalies', methods=['GET'])
def get_anomalies():
    """
    Detect anomalies in metrics
    Query params: metric_type (searches, ocr, etc.), threshold (default: 2.0)
    """
    try:
        from services.analytics_engine import AnalyticsEngine
        
        metric_type = request.args.get('metric_type', 'searches')
        threshold = float(request.args.get('threshold', 2.0))
        
        analytics = AnalyticsEngine()
        
        # Get appropriate metrics
        if metric_type == 'searches':
            metrics = metrics_tracker.metrics['recipe_searches']
            metric_key = 'search_time_ms'
        elif metric_type == 'ocr':
            metrics = metrics_tracker.metrics['ocr_scans']
            metric_key = 'processing_time_ms'
        else:
            return jsonify({"error": "Invalid metric_type"}), 400
        
        anomalies = analytics.detect_anomalies(metrics, metric_key, threshold)
        
        return jsonify({
            'metric_type': metric_type,
            'anomalies_found': len(anomalies),
            'anomalies': anomalies[:10]  # Return top 10
        }), 200
    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/analytics/trends', methods=['GET'])
def get_trends():
    """
    Get trend analysis
    Query params: metric_type, window_days (default: 7)
    """
    try:
        from services.analytics_engine import AnalyticsEngine
        
        metric_type = request.args.get('metric_type', 'searches')
        window_days = int(request.args.get('window_days', 7))
        
        analytics = AnalyticsEngine()
        
        # Get appropriate metrics
        if metric_type == 'searches':
            metrics = metrics_tracker.metrics['recipe_searches']
            metric_key = 'search_time_ms'
        elif metric_type == 'coverage':
            metrics = metrics_tracker.metrics['recipe_searches']
            metric_key = 'top_coverage'
        else:
            return jsonify({"error": "Invalid metric_type"}), 400
        
        trends = analytics.analyze_trends(metrics, metric_key, window_days=window_days)
        
        return jsonify({
            'metric_type': metric_type,
            'window_days': window_days,
            'trends': trends
        }), 200
    except Exception as e:
        logger.error(f"Error analyzing trends: {str(e)}")
        return jsonify({"error": str(e)}), 500


@metrics_bp.route('/analytics/insights', methods=['GET'])
def get_insights():
    """Get performance insights"""
    try:
        from services.analytics_engine import AnalyticsEngine
        
        analytics = AnalyticsEngine()
        insights = analytics.get_performance_insights(
            metrics_tracker.metrics['recipe_searches']
        )
        
        return jsonify({'insights': insights}), 200
    except Exception as e:
        logger.error(f"Error getting insights: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Helper function to get metrics tracker instance
def get_metrics_tracker():
    """Get the metrics tracker instance"""
    return metrics_tracker
