"""
Metrics Tracking System
Tracks and analyzes performance metrics for Pantry Oracle
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MetricsTracker:
    """
    Track and analyze system performance metrics
    """
    
    def __init__(self, metrics_dir: str = 'data/metrics'):
        """Initialize metrics tracker"""
        self.metrics_dir = metrics_dir
        os.makedirs(metrics_dir, exist_ok=True)
        
        # In-memory metrics storage
        self.metrics = {
            'recipe_searches': [],
            'indianizations': [],
            'ocr_scans': [],
            'nutrition_calculations': [],
            'user_feedback': []
        }
        
        # Load existing metrics
        self.load_metrics()
    
    def track_recipe_search(
        self,
        pantry_ingredients: List[str],
        results_count: int,
        top_coverage: float,
        search_time_ms: float
    ):
        """Track a recipe search event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'num_ingredients': len(pantry_ingredients),
            'results_count': results_count,
            'top_coverage': top_coverage,
            'search_time_ms': search_time_ms
        }
        
        self.metrics['recipe_searches'].append(event)
        self._save_metrics()
    
    def track_indianization(
        self,
        recipe_id: int,
        region: str,
        num_substitutions: int,
        num_technique_adaptations: int,
        success: bool
    ):
        """Track an Indianization event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'recipe_id': recipe_id,
            'region': region,
            'num_substitutions': num_substitutions,
            'num_technique_adaptations': num_technique_adaptations,
            'success': success
        }
        
        self.metrics['indianizations'].append(event)
        self._save_metrics()
    
    def track_ocr_scan(
        self,
        num_ingredients_found: int,
        confidence: float,
        processing_time_ms: float,
        success: bool
    ):
        """Track an OCR scan event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'num_ingredients_found': num_ingredients_found,
            'confidence': confidence,
            'processing_time_ms': processing_time_ms,
            'success': success
        }
        
        self.metrics['ocr_scans'].append(event)
        self._save_metrics()
    
    def track_nutrition_calculation(
        self,
        recipe_id: int,
        health_score: float,
        calculation_time_ms: float
    ):
        """Track a nutrition calculation event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'recipe_id': recipe_id,
            'health_score': health_score,
            'calculation_time_ms': calculation_time_ms
        }
        
        self.metrics['nutrition_calculations'].append(event)
        self._save_metrics()
    
    def track_user_feedback(
        self,
        recipe_id: int,
        feedback_type: str,  # 'relevance', 'indianization', 'health', 'ux'
        rating: int,  # 1-5
        comment: Optional[str] = None
    ):
        """Track user feedback"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'recipe_id': recipe_id,
            'feedback_type': feedback_type,
            'rating': rating,
            'comment': comment
        }
        
        self.metrics['user_feedback'].append(event)
        self._save_metrics()
    
    def get_summary_stats(self, days: int = 7) -> Dict:
        """
        Get summary statistics for the last N days
        
        Args:
            days: Number of days to include in summary
        
        Returns:
            Dictionary with summary statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter metrics by date
        recent_searches = self._filter_by_date(
            self.metrics['recipe_searches'], cutoff_date
        )
        recent_indianizations = self._filter_by_date(
            self.metrics['indianizations'], cutoff_date
        )
        recent_ocr = self._filter_by_date(
            self.metrics['ocr_scans'], cutoff_date
        )
        recent_feedback = self._filter_by_date(
            self.metrics['user_feedback'], cutoff_date
        )
        
        # Calculate statistics
        stats = {
            'period_days': days,
            'total_searches': len(recent_searches),
            'total_indianizations': len(recent_indianizations),
            'total_ocr_scans': len(recent_ocr),
            'total_feedback': len(recent_feedback),
            
            # Recipe search metrics
            'avg_search_time_ms': self._avg([s['search_time_ms'] for s in recent_searches]),
            'avg_results_per_search': self._avg([s['results_count'] for s in recent_searches]),
            'avg_top_coverage': self._avg([s['top_coverage'] for s in recent_searches]),
            
            # Indianization metrics
            'indianization_by_region': self._count_by_field(recent_indianizations, 'region'),
            'avg_substitutions': self._avg([i['num_substitutions'] for i in recent_indianizations]),
            'indianization_success_rate': self._success_rate(recent_indianizations),
            
            # OCR metrics
            'avg_ocr_confidence': self._avg([o['confidence'] for o in recent_ocr]),
            'avg_ingredients_per_scan': self._avg([o['num_ingredients_found'] for o in recent_ocr]),
            'ocr_success_rate': self._success_rate(recent_ocr),
            
            # User feedback metrics
            'feedback_by_type': self._count_by_field(recent_feedback, 'feedback_type'),
            'avg_rating_by_type': self._avg_rating_by_type(recent_feedback),
            'overall_avg_rating': self._avg([f['rating'] for f in recent_feedback])
        }
        
        return stats
    
    def get_performance_metrics(self) -> Dict:
        """Get detailed performance metrics"""
        all_searches = self.metrics['recipe_searches']
        all_ocr = self.metrics['ocr_scans']
        all_nutrition = self.metrics['nutrition_calculations']
        
        return {
            'search_performance': {
                'avg_time_ms': self._avg([s['search_time_ms'] for s in all_searches]),
                'p95_time_ms': self._percentile([s['search_time_ms'] for s in all_searches], 95),
                'p99_time_ms': self._percentile([s['search_time_ms'] for s in all_searches], 99)
            },
            'ocr_performance': {
                'avg_time_ms': self._avg([o['processing_time_ms'] for o in all_ocr]),
                'avg_confidence': self._avg([o['confidence'] for o in all_ocr]),
                'success_rate': self._success_rate(all_ocr)
            },
            'nutrition_performance': {
                'avg_time_ms': self._avg([n['calculation_time_ms'] for n in all_nutrition]),
                'avg_health_score': self._avg([n['health_score'] for n in all_nutrition])
            }
        }
    
    def get_user_satisfaction_metrics(self) -> Dict:
        """Get user satisfaction metrics"""
        feedback = self.metrics['user_feedback']
        
        if not feedback:
            return {
                'overall_satisfaction': 0,
                'by_category': {},
                'total_feedback_count': 0
            }
        
        return {
            'overall_satisfaction': self._avg([f['rating'] for f in feedback]),
            'by_category': self._avg_rating_by_type(feedback),
            'total_feedback_count': len(feedback),
            'rating_distribution': self._rating_distribution(feedback)
        }
    
    def _filter_by_date(self, events: List[Dict], cutoff_date: datetime) -> List[Dict]:
        """Filter events by date"""
        filtered = []
        for event in events:
            event_date = datetime.fromisoformat(event['timestamp'])
            if event_date >= cutoff_date:
                filtered.append(event)
        return filtered
    
    def _avg(self, values: List[float]) -> float:
        """Calculate average"""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile"""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _success_rate(self, events: List[Dict]) -> float:
        """Calculate success rate"""
        if not events:
            return 0.0
        successes = sum(1 for e in events if e.get('success', False))
        return successes / len(events)
    
    def _count_by_field(self, events: List[Dict], field: str) -> Dict:
        """Count events by field value"""
        counts = defaultdict(int)
        for event in events:
            value = event.get(field)
            if value:
                counts[value] += 1
        return dict(counts)
    
    def _avg_rating_by_type(self, feedback: List[Dict]) -> Dict:
        """Calculate average rating by feedback type"""
        by_type = defaultdict(list)
        for f in feedback:
            by_type[f['feedback_type']].append(f['rating'])
        
        return {
            ftype: self._avg(ratings)
            for ftype, ratings in by_type.items()
        }
    
    def _rating_distribution(self, feedback: List[Dict]) -> Dict:
        """Get distribution of ratings"""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for f in feedback:
            rating = f['rating']
            if 1 <= rating <= 5:
                distribution[rating] += 1
        return distribution
    
    def _save_metrics(self):
        """Save metrics to disk"""
        try:
            metrics_file = os.path.join(self.metrics_dir, 'metrics.json')
            with open(metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving metrics: {str(e)}")
    
    def load_metrics(self):
        """Load metrics from disk"""
        metrics_file = os.path.join(self.metrics_dir, 'metrics.json')
        
        if not os.path.exists(metrics_file):
            logger.info("No saved metrics found")
            return
        
        try:
            with open(metrics_file, 'r') as f:
                self.metrics = json.load(f)
            logger.info(f"Metrics loaded from {metrics_file}")
        except Exception as e:
            logger.error(f"Error loading metrics: {str(e)}")
    
    def export_metrics(self, output_file: str):
        """Export metrics to a file"""
        try:
            with open(output_file, 'w') as f:
                json.dump({
                    'metrics': self.metrics,
                    'summary': self.get_summary_stats(),
                    'performance': self.get_performance_metrics(),
                    'satisfaction': self.get_user_satisfaction_metrics()
                }, f, indent=2)
            logger.info(f"Metrics exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting metrics: {str(e)}")
