"""
Recipe Engine Service
Handles recipe search, ranking, and matching based on pantry ingredients
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
import ast
import re
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class RecipeEngine:
    """
    Core recipe search and ranking engine
    """
    
    def __init__(self, data_path: str = 'data/RAW_recipes.csv'):
        """Initialize the recipe engine with the dataset"""
        self.data_path = data_path
        self.recipes_df = None
        self.ingredient_index = {}
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the recipe dataset"""
        try:
            logger.info(f"Loading recipe data from {self.data_path}")
            self.recipes_df = pd.read_csv(self.data_path)
            
            # Parse ingredients column (stored as string representation of list)
            if 'ingredients' in self.recipes_df.columns:
                self.recipes_df['ingredients_list'] = self.recipes_df['ingredients'].apply(
                    lambda x: self._parse_ingredients(x)
                )
            
            # Parse nutrition column
            if 'nutrition' in self.recipes_df.columns:
                self.recipes_df['nutrition_dict'] = self.recipes_df['nutrition'].apply(
                    lambda x: self._parse_nutrition(x)
                )
            
            # Build ingredient index for faster searching
            self._build_ingredient_index()
            
            logger.info(f"Loaded {len(self.recipes_df)} recipes")
        except Exception as e:
            logger.error(f"Error loading recipe data: {str(e)}")
            # Create empty dataframe as fallback
            self.recipes_df = pd.DataFrame()
    
    def _parse_ingredients(self, ingredients_str: str) -> List[str]:
        """Parse ingredients from string format to list"""
        try:
            if pd.isna(ingredients_str):
                return []
            # Handle string representation of list
            if isinstance(ingredients_str, str):
                # Try to evaluate as Python literal
                try:
                    return ast.literal_eval(ingredients_str)
                except:
                    # Fallback: split by common delimiters
                    return [ing.strip() for ing in ingredients_str.split(',')]
            return ingredients_str
        except Exception as e:
            logger.warning(f"Error parsing ingredients: {str(e)}")
            return []
    
    def _parse_nutrition(self, nutrition_str: str) -> Dict[str, float]:
        """Parse nutrition information from string format"""
        try:
            if pd.isna(nutrition_str):
                return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
            
            # Nutrition is stored as [calories, total_fat, sugar, sodium, protein, saturated_fat, carbs]
            if isinstance(nutrition_str, str):
                values = ast.literal_eval(nutrition_str)
            else:
                values = nutrition_str
            
            return {
                'calories': float(values[0]) if len(values) > 0 else 0,
                'fat': float(values[1]) if len(values) > 1 else 0,
                'sugar': float(values[2]) if len(values) > 2 else 0,
                'sodium': float(values[3]) if len(values) > 3 else 0,
                'protein': float(values[4]) if len(values) > 4 else 0,
                'saturated_fat': float(values[5]) if len(values) > 5 else 0,
                'carbs': float(values[6]) if len(values) > 6 else 0
            }
        except Exception as e:
            logger.warning(f"Error parsing nutrition: {str(e)}")
            return {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    
    def _build_ingredient_index(self):
        """Build an inverted index of ingredients to recipe IDs"""
        if self.recipes_df is None or self.recipes_df.empty:
            return
        
        for idx, row in self.recipes_df.iterrows():
            ingredients = row.get('ingredients_list', [])
            for ingredient in ingredients:
                # Normalize ingredient name
                normalized = self._normalize_ingredient(ingredient)
                if normalized not in self.ingredient_index:
                    self.ingredient_index[normalized] = set()
                self.ingredient_index[normalized].add(idx)
    
    def _normalize_ingredient(self, ingredient: str) -> str:
        """Normalize ingredient name for matching"""
        if not ingredient:
            return ""
        # Convert to lowercase, remove extra spaces
        normalized = ingredient.lower().strip()
        # Remove quantities and measurements
        normalized = re.sub(r'\d+\.?\d*\s*(cup|tbsp|tsp|oz|lb|g|kg|ml|l)s?', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def search_recipes(
        self,
        pantry_ingredients: List[str],
        max_time: Optional[int] = None,
        diet: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict:
        """
        Search for recipes based on pantry ingredients
        
        Args:
            pantry_ingredients: List of available ingredients
            max_time: Maximum cooking time in minutes
            diet: Dietary preference (vegetarian, vegan, etc.)
            page: Page number for pagination
            limit: Number of results per page
        
        Returns:
            Dictionary with recipes and metadata
        """
        if self.recipes_df is None or self.recipes_df.empty:
            return {
                'recipes': [],
                'total_results': 0,
                'page': page,
                'total_pages': 0
            }
        
        # Normalize pantry ingredients
        normalized_pantry = [self._normalize_ingredient(ing) for ing in pantry_ingredients]
        
        # Calculate pantry coverage for each recipe
        recipes_with_scores = []
        
        for idx, row in self.recipes_df.iterrows():
            recipe_ingredients = row.get('ingredients_list', [])
            normalized_recipe_ingredients = [
                self._normalize_ingredient(ing) for ing in recipe_ingredients
            ]
            
            # Calculate coverage
            coverage, missing = self._calculate_coverage(
                normalized_pantry,
                normalized_recipe_ingredients
            )
            
            # Apply filters
            if max_time and row.get('minutes', 0) > max_time:
                continue
            
            # Create recipe object
            recipe = {
                'id': int(row.get('id', idx)),
                'name': row.get('name', 'Unknown Recipe'),
                'pantry_coverage': coverage,
                'missing_ingredients': missing,
                'ingredients': recipe_ingredients,
                'time_minutes': int(row.get('minutes', 0)),
                'servings': int(row.get('n_steps', 4)),  # Using n_steps as proxy for servings
                'nutrition': row.get('nutrition_dict', {}),
                'steps': self._parse_steps(row.get('steps', '')),
                'tags': self._parse_tags(row.get('tags', ''))
            }
            
            recipes_with_scores.append(recipe)
        
        # Sort by pantry coverage (descending)
        recipes_with_scores.sort(key=lambda x: x['pantry_coverage'], reverse=True)
        
        # Pagination
        total_results = len(recipes_with_scores)
        total_pages = (total_results + limit - 1) // limit
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        
        paginated_recipes = recipes_with_scores[start_idx:end_idx]
        
        return {
            'recipes': paginated_recipes,
            'total_results': total_results,
            'page': page,
            'total_pages': total_pages
        }
    
    def _calculate_coverage(
        self,
        pantry: List[str],
        recipe_ingredients: List[str]
    ) -> Tuple[float, List[str]]:
        """
        Calculate what percentage of recipe ingredients are in pantry
        
        Returns:
            Tuple of (coverage_percentage, missing_ingredients)
        """
        if not recipe_ingredients:
            return 1.0, []
        
        pantry_set = set(pantry)
        recipe_set = set(recipe_ingredients)
        
        # Find matches using fuzzy matching
        matched = 0
        missing = []
        
        for recipe_ing in recipe_ingredients:
            found = False
            for pantry_ing in pantry:
                if self._ingredients_match(recipe_ing, pantry_ing):
                    matched += 1
                    found = True
                    break
            if not found:
                missing.append(recipe_ing)
        
        coverage = matched / len(recipe_ingredients) if recipe_ingredients else 0
        return coverage, missing
    
    def _ingredients_match(self, ing1: str, ing2: str) -> bool:
        """Check if two ingredients match (fuzzy matching)"""
        # Simple substring matching for now
        return ing1 in ing2 or ing2 in ing1
    
    def _parse_steps(self, steps_str: str) -> List[str]:
        """Parse cooking steps from string format"""
        try:
            if pd.isna(steps_str):
                return []
            if isinstance(steps_str, str):
                return ast.literal_eval(steps_str)
            return steps_str
        except:
            return []
    
    def _parse_tags(self, tags_str: str) -> List[str]:
        """Parse tags from string format"""
        try:
            if pd.isna(tags_str):
                return []
            if isinstance(tags_str, str):
                return ast.literal_eval(tags_str)
            return tags_str
        except:
            return []
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict]:
        """Get a specific recipe by ID"""
        if self.recipes_df is None or self.recipes_df.empty:
            return None
        
        recipe_row = self.recipes_df[self.recipes_df['id'] == recipe_id]
        
        if recipe_row.empty:
            return None
        
        row = recipe_row.iloc[0]
        
        return {
            'id': int(row.get('id', recipe_id)),
            'name': row.get('name', 'Unknown Recipe'),
            'ingredients': row.get('ingredients_list', []),
            'time_minutes': int(row.get('minutes', 0)),
            'servings': int(row.get('n_steps', 4)),
            'nutrition': row.get('nutrition_dict', {}),
            'steps': self._parse_steps(row.get('steps', '')),
            'tags': self._parse_tags(row.get('tags', ''))
        }
