"""
Simple test script for backend services
"""

from services.recipe_engine import RecipeEngine
from services.nutrition_calculator import NutritionCalculator
from services.indianization_engine import IndianizationEngine

def test_services():
    """Test basic service functionality"""
    
    print("=" * 60)
    print("PANTRY ORACLE - Backend Services Test")
    print("=" * 60)
    
    # Test Recipe Engine
    print("\n1. Testing Recipe Engine...")
    try:
        recipe_engine = RecipeEngine()
        print("   ✓ RecipeEngine initialized")
        
        # Test search with mock ingredients
        results = recipe_engine.search_recipes(
            pantry_ingredients=["tomato", "onion", "garlic"],
            max_time=30,
            page=1,
            limit=5
        )
        print(f"   ✓ Search returned {results['total_results']} recipes")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test Nutrition Calculator
    print("\n2. Testing Nutrition Calculator...")
    try:
        nutrition_calc = NutritionCalculator()
        print("   ✓ NutritionCalculator initialized")
        
        # Test with mock recipe
        mock_recipe = {
            'nutrition': {
                'calories': 450,
                'protein': 25,
                'carbs': 50,
                'fat': 15
            },
            'servings': 4
        }
        
        nutrition = nutrition_calc.calculate_recipe_nutrition(mock_recipe, servings=2)
        print(f"   ✓ Nutrition calculated: {nutrition['per_serving']['calories']} cal/serving")
        
        health_score = nutrition_calc.get_health_score(mock_recipe['nutrition'])
        print(f"   ✓ Health score: {health_score['score']}/100 ({health_score['rating']})")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    # Test Indianization Engine
    print("\n3. Testing Indianization Engine...")
    try:
        indianization_engine = IndianizationEngine()
        print("   ✓ IndianizationEngine initialized")
        
        # Test with mock recipe
        mock_recipe = {
            'name': 'Grilled Chicken with Broccoli',
            'ingredients': ['chicken breast', 'broccoli', 'olive oil', 'butter'],
            'steps': ['Grill the chicken', 'Steam the broccoli'],
            'nutrition': {'calories': 350, 'protein': 30, 'carbs': 20, 'fat': 15},
            'time_minutes': 25,
            'servings': 2
        }
        
        indianized = indianization_engine.indianize_recipe(mock_recipe, region='north')
        print(f"   ✓ Original: {mock_recipe['name']}")
        print(f"   ✓ Indianized: {indianized['indianized_name']}")
        print(f"   ✓ Substitutions: {len(indianized['ingredient_substitutions'])} ingredients")
        
        # Test regional info
        regional_info = indianization_engine.get_regional_info('south')
        print(f"   ✓ Regional info: {regional_info['description'][:50]}...")
        
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_services()
