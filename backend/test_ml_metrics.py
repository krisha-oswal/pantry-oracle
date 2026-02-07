"""
Test script for ML and Metrics systems
"""

from ml.recommendation_engine import MLRecommendationEngine
from services.metrics_tracker import MetricsTracker

def test_ml_and_metrics():
    """Test ML recommendation engine and metrics tracker"""
    
    print("=" * 60)
    print("PANTRY ORACLE - ML & Metrics Test")
    print("=" * 60)
    
    # Test ML Recommendation Engine
    print("\n1. Testing ML Recommendation Engine...")
    try:
        ml_engine = MLRecommendationEngine()
        print("   ✓ MLRecommendationEngine initialized")
        
        # Create mock recipes for training
        mock_recipes = [
            {
                'id': 1,
                'name': 'Tomato Pasta',
                'ingredients': ['tomato', 'pasta', 'garlic', 'olive oil'],
                'tags': ['italian', 'vegetarian', 'quick']
            },
            {
                'id': 2,
                'name': 'Chicken Curry',
                'ingredients': ['chicken', 'curry powder', 'onion', 'tomato'],
                'tags': ['indian', 'spicy', 'main course']
            },
            {
                'id': 3,
                'name': 'Caesar Salad',
                'ingredients': ['lettuce', 'chicken', 'parmesan', 'croutons'],
                'tags': ['salad', 'healthy', 'quick']
            }
        ]
        
        # Train model
        ml_engine.train(mock_recipes)
        print("   ✓ Model trained on 3 recipes")
        
        # Get recommendations
        recommendations = ml_engine.get_recommendations(
            pantry_ingredients=['tomato', 'garlic', 'pasta'],
            n_recommendations=2
        )
        print(f"   ✓ Got {len(recommendations)} recommendations")
        for recipe_id, score in recommendations:
            print(f"      - Recipe {recipe_id}: {score:.3f} similarity")
        
        # Get model stats
        stats = ml_engine.get_model_stats()
        print(f"   ✓ Model stats: {stats['num_recipes']} recipes, {stats['num_features']} features")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test Metrics Tracker
    print("\n2. Testing Metrics Tracker...")
    try:
        metrics_tracker = MetricsTracker()
        print("   ✓ MetricsTracker initialized")
        
        # Track some events
        metrics_tracker.track_recipe_search(
            pantry_ingredients=['tomato', 'onion'],
            results_count=10,
            top_coverage=0.85,
            search_time_ms=45.2
        )
        print("   ✓ Tracked recipe search")
        
        metrics_tracker.track_indianization(
            recipe_id=1,
            region='north',
            num_substitutions=3,
            num_technique_adaptations=1,
            success=True
        )
        print("   ✓ Tracked Indianization")
        
        metrics_tracker.track_user_feedback(
            recipe_id=1,
            feedback_type='relevance',
            rating=5,
            comment='Great recipe!'
        )
        print("   ✓ Tracked user feedback")
        
        # Get summary stats
        summary = metrics_tracker.get_summary_stats(days=7)
        print(f"   ✓ Summary stats:")
        print(f"      - Total searches: {summary['total_searches']}")
        print(f"      - Total Indianizations: {summary['total_indianizations']}")
        print(f"      - Overall rating: {summary['overall_avg_rating']:.1f}/5")
        
        # Get performance metrics
        performance = metrics_tracker.get_performance_metrics()
        print(f"   ✓ Performance metrics:")
        print(f"      - Avg search time: {performance['search_performance']['avg_time_ms']:.1f}ms")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("ML & Metrics tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_ml_and_metrics()
