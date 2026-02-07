"""
Analytics Engine for Advanced Metrics
Implements anomaly detection, trend analysis, and predictive metrics
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import logging

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Advanced analytics engine for metrics analysis
    """
    
    def __init__(self):
        """Initialize analytics engine"""
        pass
    
    def detect_anomalies(
        self,
        metrics: List[Dict],
        metric_key: str,
        threshold_std: float = 2.0
    ) -> List[Dict]:
        """
        Detect anomalies in metrics using standard deviation
        
        Args:
            metrics: List of metric events
            metric_key: Key to analyze (e.g., 'search_time_ms')
            threshold_std: Number of standard deviations for anomaly
        
        Returns:
            List of anomalous events
        """
        if not metrics:
            return []
        
        # Extract values
        values = [m.get(metric_key, 0) for m in metrics if metric_key in m]
        
        if len(values) < 3:
            return []
        
        # Calculate statistics
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return []
        
        # Find anomalies
        anomalies = []
        for i, metric in enumerate(metrics):
            if metric_key not in metric:
                continue
            
            value = metric[metric_key]
            z_score = abs((value - mean) / std)
            
            if z_score > threshold_std:
                anomalies.append({
                    **metric,
                    'z_score': z_score,
                    'deviation_from_mean': value - mean
                })
        
        return anomalies
    
    def analyze_trends(
        self,
        metrics: List[Dict],
        metric_key: str,
        time_key: str = 'timestamp',
        window_days: int = 7
    ) -> Dict:
        """
        Analyze trends in metrics over time
        
        Args:
            metrics: List of metric events
            metric_key: Key to analyze
            time_key: Timestamp key
            window_days: Window for trend analysis
        
        Returns:
            Trend analysis results
        """
        if not metrics:
            return {
                'trend': 'unknown',
                'slope': 0,
                'average': 0,
                'change_percent': 0
            }
        
        # Group by day
        daily_values = defaultdict(list)
        
        for metric in metrics:
            if metric_key not in metric or time_key not in metric:
                continue
            
            timestamp = datetime.fromisoformat(metric[time_key])
            day = timestamp.date()
            daily_values[day].append(metric[metric_key])
        
        if len(daily_values) < 2:
            return {
                'trend': 'insufficient_data',
                'slope': 0,
                'average': np.mean([m.get(metric_key, 0) for m in metrics]),
                'change_percent': 0
            }
        
        # Calculate daily averages
        sorted_days = sorted(daily_values.keys())
        daily_averages = [np.mean(daily_values[day]) for day in sorted_days]
        
        # Calculate trend (simple linear regression)
        x = np.arange(len(daily_averages))
        y = np.array(daily_averages)
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
        else:
            slope = 0
        
        # Calculate change percentage
        if len(daily_averages) >= 2:
            first_avg = daily_averages[0]
            last_avg = daily_averages[-1]
            change_percent = ((last_avg - first_avg) / first_avg * 100) if first_avg != 0 else 0
        else:
            change_percent = 0
        
        # Determine trend direction
        if slope > 0.1:
            trend = 'increasing'
        elif slope < -0.1:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'slope': float(slope),
            'average': float(np.mean(daily_averages)),
            'change_percent': float(change_percent),
            'daily_data': {
                'dates': [str(d) for d in sorted_days],
                'values': [float(v) for v in daily_averages]
            }
        }
    
    def calculate_user_cohorts(
        self,
        feedback_metrics: List[Dict],
        cohort_by: str = 'feedback_type'
    ) -> Dict:
        """
        Calculate user cohort statistics
        
        Args:
            feedback_metrics: List of feedback events
            cohort_by: Field to group cohorts by
        
        Returns:
            Cohort analysis results
        """
        cohorts = defaultdict(lambda: {
            'count': 0,
            'avg_rating': 0,
            'ratings': []
        })
        
        for feedback in feedback_metrics:
            cohort_key = feedback.get(cohort_by, 'unknown')
            rating = feedback.get('rating', 0)
            
            cohorts[cohort_key]['count'] += 1
            cohorts[cohort_key]['ratings'].append(rating)
        
        # Calculate averages
        for cohort_key, cohort_data in cohorts.items():
            if cohort_data['ratings']:
                cohort_data['avg_rating'] = np.mean(cohort_data['ratings'])
                cohort_data['std_rating'] = np.std(cohort_data['ratings'])
            del cohort_data['ratings']  # Remove raw ratings
        
        return dict(cohorts)
    
    def analyze_conversion_funnel(
        self,
        search_metrics: List[Dict],
        indianization_metrics: List[Dict],
        feedback_metrics: List[Dict]
    ) -> Dict:
        """
        Analyze conversion funnel from search to feedback
        
        Args:
            search_metrics: Recipe search events
            indianization_metrics: Indianization events
            feedback_metrics: User feedback events
        
        Returns:
            Funnel analysis results
        """
        total_searches = len(search_metrics)
        total_indianizations = len(indianization_metrics)
        total_feedback = len(feedback_metrics)
        
        # Calculate conversion rates
        indianization_rate = (total_indianizations / total_searches * 100) if total_searches > 0 else 0
        feedback_rate = (total_feedback / total_searches * 100) if total_searches > 0 else 0
        
        # Calculate drop-off rates
        search_to_indian_dropoff = 100 - indianization_rate
        search_to_feedback_dropoff = 100 - feedback_rate
        
        return {
            'funnel_stages': {
                'searches': total_searches,
                'indianizations': total_indianizations,
                'feedback': total_feedback
            },
            'conversion_rates': {
                'search_to_indianization': round(indianization_rate, 2),
                'search_to_feedback': round(feedback_rate, 2)
            },
            'dropoff_rates': {
                'search_to_indianization': round(search_to_indian_dropoff, 2),
                'search_to_feedback': round(search_to_feedback_dropoff, 2)
            }
        }
    
    def predict_next_period(
        self,
        metrics: List[Dict],
        metric_key: str,
        time_key: str = 'timestamp',
        periods_ahead: int = 7
    ) -> Dict:
        """
        Predict metrics for next period using simple trend extrapolation
        
        Args:
            metrics: Historical metrics
            metric_key: Key to predict
            time_key: Timestamp key
            periods_ahead: Number of periods to predict
        
        Returns:
            Prediction results
        """
        trend_analysis = self.analyze_trends(metrics, metric_key, time_key)
        
        if trend_analysis['trend'] == 'insufficient_data':
            return {
                'prediction': 'insufficient_data',
                'predicted_value': 0,
                'confidence': 0
            }
        
        # Simple linear extrapolation
        current_avg = trend_analysis['average']
        slope = trend_analysis['slope']
        
        predicted_value = current_avg + (slope * periods_ahead)
        
        # Confidence based on trend stability
        if trend_analysis['trend'] == 'stable':
            confidence = 0.8
        elif abs(trend_analysis['change_percent']) < 20:
            confidence = 0.6
        else:
            confidence = 0.4
        
        return {
            'prediction': trend_analysis['trend'],
            'predicted_value': float(max(0, predicted_value)),  # Ensure non-negative
            'confidence': confidence,
            'current_average': current_avg,
            'trend_slope': slope
        }
    
    def get_performance_insights(
        self,
        search_metrics: List[Dict]
    ) -> List[str]:
        """
        Generate performance insights from metrics
        
        Args:
            search_metrics: Search performance metrics
        
        Returns:
            List of insight strings
        """
        insights = []
        
        if not search_metrics:
            return ["Insufficient data for insights"]
        
        # Analyze search times
        search_times = [m.get('search_time_ms', 0) for m in search_metrics]
        avg_time = np.mean(search_times)
        p95_time = np.percentile(search_times, 95)
        
        if avg_time < 50:
            insights.append("✅ Excellent search performance (avg < 50ms)")
        elif avg_time < 100:
            insights.append("✓ Good search performance (avg < 100ms)")
        else:
            insights.append("⚠️ Search performance could be improved (avg > 100ms)")
        
        if p95_time > 200:
            insights.append("⚠️ Some searches are slow (P95 > 200ms)")
        
        # Analyze coverage
        coverages = [m.get('top_coverage', 0) for m in search_metrics]
        avg_coverage = np.mean(coverages)
        
        if avg_coverage > 0.8:
            insights.append("✅ High pantry coverage (avg > 80%)")
        elif avg_coverage > 0.5:
            insights.append("✓ Moderate pantry coverage (avg > 50%)")
        else:
            insights.append("⚠️ Low pantry coverage - users may need more ingredients")
        
        # Analyze result counts
        result_counts = [m.get('results_count', 0) for m in search_metrics]
        avg_results = np.mean(result_counts)
        
        if avg_results < 5:
            insights.append("⚠️ Low average results per search - consider expanding recipe database")
        elif avg_results > 20:
            insights.append("✓ Good variety of recipe results")
        
        return insights
