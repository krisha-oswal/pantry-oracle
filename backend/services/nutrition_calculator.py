"""
Nutrition Calculator Service
Calculates nutritional information for recipes
"""

from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)


class NutritionCalculator:
    """
    Calculate and format nutritional information for recipes
    """
    
    def __init__(self):
        """Initialize the nutrition calculator"""
        self.nutrient_database = self._load_nutrient_database()
    
    def _load_nutrient_database(self) -> Dict:
        """Load nutrient database (placeholder for now)"""
        # In a real implementation, this would load from USDA database or similar
        return {}
    
    def calculate_recipe_nutrition(
        self,
        recipe: Dict,
        servings: Optional[int] = None
    ) -> Dict:
        """
        Calculate nutrition for a recipe
        
        Args:
            recipe: Recipe dictionary with nutrition data
            servings: Number of servings (if different from recipe default)
        
        Returns:
            Dictionary with total and per-serving nutrition
        """
        nutrition = recipe.get('nutrition', {})
        recipe_servings = recipe.get('servings', 1)
        target_servings = servings if servings else recipe_servings
        
        # Extract nutrition values
        calories = float(nutrition.get('calories', 0))
        protein = float(nutrition.get('protein', 0))
        carbs = float(nutrition.get('carbs', 0))
        fat = float(nutrition.get('fat', 0))
        sugar = float(nutrition.get('sugar', 0))
        sodium = float(nutrition.get('sodium', 0))
        
        # Calculate per serving
        per_serving = {
            'calories': round(calories / target_servings, 1),
            'protein': round(protein / target_servings, 1),
            'carbs': round(carbs / target_servings, 1),
            'fat': round(fat / target_servings, 1),
            'sugar': round(sugar / target_servings, 1),
            'sodium': round(sodium / target_servings, 1)
        }
        
        return {
            'total': {
                'calories': round(calories, 1),
                'protein': round(protein, 1),
                'carbs': round(carbs, 1),
                'fat': round(fat, 1),
                'sugar': round(sugar, 1),
                'sodium': round(sodium, 1)
            },
            'per_serving': per_serving,
            'servings': target_servings,
            'units': 'grams'
        }
    
    def calculate_macros_percentage(self, nutrition: Dict) -> Dict:
        """
        Calculate macronutrient percentages
        
        Args:
            nutrition: Nutrition dictionary
        
        Returns:
            Dictionary with macro percentages
        """
        protein = float(nutrition.get('protein', 0))
        carbs = float(nutrition.get('carbs', 0))
        fat = float(nutrition.get('fat', 0))
        
        # Calculate calories from macros (protein: 4 cal/g, carbs: 4 cal/g, fat: 9 cal/g)
        protein_cals = protein * 4
        carbs_cals = carbs * 4
        fat_cals = fat * 9
        
        total_cals = protein_cals + carbs_cals + fat_cals
        
        if total_cals == 0:
            return {
                'protein_percent': 0,
                'carbs_percent': 0,
                'fat_percent': 0
            }
        
        return {
            'protein_percent': round((protein_cals / total_cals) * 100, 1),
            'carbs_percent': round((carbs_cals / total_cals) * 100, 1),
            'fat_percent': round((fat_cals / total_cals) * 100, 1)
        }
    
    def get_health_score(self, nutrition: Dict) -> Dict:
        """
        Calculate a simple health score based on nutrition
        
        Args:
            nutrition: Nutrition dictionary
        
        Returns:
            Dictionary with health score and breakdown
        """
        score = 100
        factors = []
        
        # Penalize high sugar
        sugar = float(nutrition.get('sugar', 0))
        if sugar > 50:
            penalty = min(30, (sugar - 50) / 2)
            score -= penalty
            factors.append(f"High sugar content (-{penalty:.0f})")
        
        # Penalize high sodium
        sodium = float(nutrition.get('sodium', 0))
        if sodium > 2000:  # mg
            penalty = min(20, (sodium - 2000) / 100)
            score -= penalty
            factors.append(f"High sodium (-{penalty:.0f})")
        
        # Reward high protein
        protein = float(nutrition.get('protein', 0))
        if protein > 20:
            bonus = min(10, (protein - 20) / 5)
            score += bonus
            factors.append(f"Good protein content (+{bonus:.0f})")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return {
            'score': round(score, 1),
            'rating': self._get_rating(score),
            'factors': factors
        }
    
    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Fair"
        else:
            return "Poor"
