"""
Indianization Engine Service
Adapts recipes to Indian cuisine with ingredient substitutions and technique modifications
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class IndianizationEngine:
    """
    Engine for Indianizing recipes with regional variations
    """
    
    # Ingredient substitution mappings
    INGREDIENT_SUBSTITUTIONS = {
        # Dairy
        'butter': {'north': 'ghee', 'south': 'coconut oil', 'west': 'ghee', 'east': 'mustard oil'},
        'cream': {'north': 'malai', 'south': 'coconut cream', 'west': 'malai', 'east': 'malai'},
        'cheese': {'north': 'paneer', 'south': 'paneer', 'west': 'paneer', 'east': 'chhena'},
        'milk': {'north': 'whole milk', 'south': 'coconut milk', 'west': 'whole milk', 'east': 'whole milk'},
        
        # Proteins
        'chicken': {'north': 'chicken', 'south': 'chicken', 'west': 'chicken', 'east': 'fish'},
        'beef': {'north': 'mutton', 'south': 'mutton', 'west': 'mutton', 'east': 'mutton'},
        'pork': {'north': 'mutton', 'south': 'mutton', 'west': 'mutton', 'east': 'pork'},
        'tofu': {'north': 'paneer', 'south': 'paneer', 'west': 'paneer', 'east': 'chhena'},
        
        # Vegetables
        'zucchini': {'north': 'bottle gourd (lauki)', 'south': 'ash gourd', 'west': 'bottle gourd', 'east': 'bottle gourd'},
        'broccoli': {'north': 'cauliflower (gobi)', 'south': 'cabbage', 'west': 'cauliflower', 'east': 'cauliflower'},
        'bell pepper': {'north': 'capsicum (shimla mirch)', 'south': 'capsicum', 'west': 'capsicum', 'east': 'capsicum'},
        
        # Grains
        'pasta': {'north': 'wheat noodles (sevaiyan)', 'south': 'rice noodles (idiyappam)', 'west': 'vermicelli', 'east': 'rice noodles'},
        'rice': {'north': 'basmati rice', 'south': 'sona masoori rice', 'west': 'basmati rice', 'east': 'gobindobhog rice'},
        'bread': {'north': 'roti/naan', 'south': 'dosa/idli', 'west': 'bhakri', 'east': 'luchi'},
        
        # Spices & Seasonings
        'oregano': {'north': 'kasuri methi', 'south': 'curry leaves', 'west': 'kasuri methi', 'east': 'panch phoron'},
        'basil': {'north': 'tulsi', 'south': 'curry leaves', 'west': 'tulsi', 'east': 'tulsi'},
        'thyme': {'north': 'ajwain', 'south': 'curry leaves', 'west': 'ajwain', 'east': 'radhuni'},
        'soy sauce': {'north': 'tamarind chutney', 'south': 'tamarind paste', 'west': 'tamarind chutney', 'east': 'tamarind paste'},
        
        # Oils
        'olive oil': {'north': 'ghee', 'south': 'coconut oil', 'west': 'groundnut oil', 'east': 'mustard oil'},
        'vegetable oil': {'north': 'refined oil', 'south': 'coconut oil', 'west': 'groundnut oil', 'east': 'mustard oil'},
    }
    
    # Technique adaptations
    TECHNIQUE_ADAPTATIONS = {
        'baking': {
            'north': 'tandoor cooking or stovetop',
            'south': 'steaming or tawa cooking',
            'west': 'tawa or kadhai cooking',
            'east': 'steaming or shallow frying'
        },
        'grilling': {
            'north': 'tandoor or tawa',
            'south': 'tawa or appam pan',
            'west': 'tawa',
            'east': 'tawa or kadhai'
        },
        'roasting': {
            'north': 'dry roasting in kadhai',
            'south': 'dry roasting on tawa',
            'west': 'dry roasting in kadhai',
            'east': 'bhuna (slow roasting)'
        }
    }
    
    # Regional spice blends
    REGIONAL_SPICES = {
        'north': ['garam masala', 'kasuri methi', 'kasoori methi', 'dried fenugreek'],
        'south': ['curry leaves', 'mustard seeds', 'urad dal', 'sambar powder'],
        'west': ['goda masala', 'kokum', 'peanuts', 'sesame seeds'],
        'east': ['panch phoron', 'mustard oil', 'poppy seeds', 'nigella seeds']
    }
    
    def __init__(self):
        """Initialize the Indianization engine"""
        pass
    
    def indianize_recipe(
        self,
        recipe: Dict,
        region: str = 'north'
    ) -> Dict:
        """
        Indianize a recipe with regional variations
        
        Args:
            recipe: Original recipe dictionary
            region: Indian region (north, south, east, west)
        
        Returns:
            Indianized recipe with substitutions and adaptations
        """
        region = region.lower()
        if region not in ['north', 'south', 'east', 'west']:
            region = 'north'
        
        original_name = recipe.get('name', 'Unknown Recipe')
        ingredients = recipe.get('ingredients', [])
        steps = recipe.get('steps', [])
        
        # Perform ingredient substitutions
        substitutions = []
        indianized_ingredients = []
        
        for ingredient in ingredients:
            substituted = self._substitute_ingredient(ingredient, region)
            if substituted != ingredient:
                substitutions.append({
                    'original': ingredient,
                    'substitute': substituted,
                    'reason': f'Regional adaptation for {region} India'
                })
            indianized_ingredients.append(substituted)
        
        # Adapt techniques
        technique_adaptations = self._adapt_techniques(steps, region)
        
        # Add regional spices
        regional_spices = self.REGIONAL_SPICES.get(region, [])
        spice_additions = []
        for spice in regional_spices[:2]:  # Add top 2 regional spices
            if spice not in ' '.join(indianized_ingredients).lower():
                spice_additions.append(spice)
                indianized_ingredients.append(f"1 tsp {spice}")
        
        # Generate Indianized name
        indianized_name = self._generate_indian_name(original_name, region)
        
        return {
            'original_name': original_name,
            'indianized_name': indianized_name,
            'region': region,
            'ingredients': indianized_ingredients,
            'ingredient_substitutions': substitutions,
            'technique_adaptations': technique_adaptations,
            'spice_additions': spice_additions,
            'steps': steps,  # Steps would be modified in a full implementation
            'nutrition': recipe.get('nutrition', {}),
            'time_minutes': recipe.get('time_minutes', 0),
            'servings': recipe.get('servings', 4)
        }
    
    def _substitute_ingredient(self, ingredient: str, region: str) -> str:
        """
        Substitute an ingredient with Indian equivalent
        
        Args:
            ingredient: Original ingredient
            region: Target region
        
        Returns:
            Substituted ingredient
        """
        ingredient_lower = ingredient.lower()
        
        # Check each substitution mapping
        for key, regional_subs in self.INGREDIENT_SUBSTITUTIONS.items():
            if key in ingredient_lower:
                substitute = regional_subs.get(region, ingredient)
                # Preserve quantity if present
                quantity_match = ingredient.split(key)[0].strip()
                if quantity_match:
                    return f"{quantity_match} {substitute}"
                return substitute
        
        return ingredient
    
    def _adapt_techniques(self, steps: List[str], region: str) -> List[Dict]:
        """
        Adapt cooking techniques for Indian kitchen
        
        Args:
            steps: Original cooking steps
            region: Target region
        
        Returns:
            List of technique adaptations
        """
        adaptations = []
        
        for technique, regional_adaptations in self.TECHNIQUE_ADAPTATIONS.items():
            # Check if technique is mentioned in steps
            steps_text = ' '.join(steps).lower()
            if technique in steps_text:
                adaptation = regional_adaptations.get(region, technique)
                adaptations.append({
                    'original_technique': technique,
                    'adapted_technique': adaptation,
                    'reason': f'Traditional {region} Indian cooking method'
                })
        
        return adaptations
    
    def _generate_indian_name(self, original_name: str, region: str) -> str:
        """
        Generate an Indianized recipe name
        
        Args:
            original_name: Original recipe name
            region: Target region
        
        Returns:
            Indianized name
        """
        # Simple name adaptation
        regional_suffixes = {
            'north': 'Masala',
            'south': 'Curry',
            'west': 'Bhaji',
            'east': 'Jhol'
        }
        
        suffix = regional_suffixes.get(region, 'Masala')
        
        # Remove common Western terms
        name = original_name.replace('Baked', 'Tandoori')
        name = name.replace('Grilled', 'Tandoori')
        name = name.replace('Roasted', 'Bhuna')
        name = name.replace('Fried', 'Tala')
        
        # Add regional suffix if not already present
        if suffix.lower() not in name.lower():
            name = f"{name} {suffix}"
        
        return name
    
    def get_regional_info(self, region: str) -> Dict:
        """
        Get information about a specific region's cuisine
        
        Args:
            region: Region name
        
        Returns:
            Dictionary with regional cuisine information
        """
        regional_info = {
            'north': {
                'description': 'North Indian cuisine features rich gravies, tandoor cooking, and dairy products',
                'key_ingredients': ['ghee', 'paneer', 'cream', 'garam masala', 'kasuri methi'],
                'popular_dishes': ['Butter Chicken', 'Dal Makhani', 'Naan', 'Biryani']
            },
            'south': {
                'description': 'South Indian cuisine emphasizes rice, lentils, coconut, and tangy flavors',
                'key_ingredients': ['coconut', 'curry leaves', 'tamarind', 'mustard seeds', 'rice'],
                'popular_dishes': ['Dosa', 'Sambar', 'Rasam', 'Idli']
            },
            'west': {
                'description': 'Western Indian cuisine features diverse flavors from coastal to desert regions',
                'key_ingredients': ['kokum', 'peanuts', 'jaggery', 'coconut', 'goda masala'],
                'popular_dishes': ['Dhokla', 'Vada Pav', 'Pav Bhaji', 'Modak']
            },
            'east': {
                'description': 'Eastern Indian cuisine is known for subtle spices, mustard oil, and fish',
                'key_ingredients': ['mustard oil', 'panch phoron', 'poppy seeds', 'fish', 'rice'],
                'popular_dishes': ['Macher Jhol', 'Rasgulla', 'Luchi', 'Chingri Malai Curry']
            }
        }
        
        return regional_info.get(region.lower(), regional_info['north'])
