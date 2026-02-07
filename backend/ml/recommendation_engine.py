"""
ML-based Recipe Recommendation Engine
Uses embeddings and similarity search for intelligent recipe recommendations
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

logger = logging.getLogger(__name__)


class MLRecommendationEngine:
    """
    Machine Learning engine for recipe recommendations
    Uses TF-IDF and cosine similarity for now, can be upgraded to embeddings
    """
    
    def __init__(self, model_path: str = 'ml/models'):
        """Initialize the ML recommendation engine"""
        self.model_path = model_path
        self.vectorizer = None
        self.recipe_vectors = None
        self.recipe_ids = []
        self.is_trained = False
        
        # Create model directory if it doesn't exist
        os.makedirs(model_path, exist_ok=True)
        
        # Try to load existing model
        self.load_model()
    
    def train(self, recipes: List[Dict]):
        """
        Train the recommendation model on recipe data
        
        Args:
            recipes: List of recipe dictionaries with ingredients and tags
        """
        if not recipes:
            logger.warning("No recipes provided for training")
            return
        
        logger.info(f"Training ML model on {len(recipes)} recipes")
        
        # Extract recipe IDs
        self.recipe_ids = [recipe.get('id', i) for i, recipe in enumerate(recipes)]
        
        # Create text representations of recipes
        recipe_texts = []
        for recipe in recipes:
            # Combine ingredients, tags, and name for rich representation
            ingredients = ' '.join(recipe.get('ingredients', []))
            tags = ' '.join(recipe.get('tags', []))
            name = recipe.get('name', '')
            
            text = f"{name} {ingredients} {tags}"
            recipe_texts.append(text)
        
        # Train TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.recipe_vectors = self.vectorizer.fit_transform(recipe_texts)
        self.is_trained = True
        
        logger.info("ML model training completed")
        
        # Save model
        self.save_model()
    
    def get_recommendations(
        self,
        pantry_ingredients: List[str],
        n_recommendations: int = 10,
        exclude_ids: Optional[List[int]] = None
    ) -> List[Tuple[int, float]]:
        """
        Get recipe recommendations based on pantry ingredients
        
        Args:
            pantry_ingredients: List of available ingredients
            n_recommendations: Number of recommendations to return
            exclude_ids: Recipe IDs to exclude from recommendations
        
        Returns:
            List of (recipe_id, similarity_score) tuples
        """
        if not self.is_trained:
            logger.warning("Model not trained, returning empty recommendations")
            return []
        
        # Create query vector from pantry ingredients
        query_text = ' '.join(pantry_ingredients)
        query_vector = self.vectorizer.transform([query_text])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, self.recipe_vectors)[0]
        
        # Get top N recommendations
        top_indices = np.argsort(similarities)[::-1]
        
        recommendations = []
        for idx in top_indices:
            recipe_id = self.recipe_ids[idx]
            
            # Skip excluded recipes
            if exclude_ids and recipe_id in exclude_ids:
                continue
            
            similarity = float(similarities[idx])
            recommendations.append((recipe_id, similarity))
            
            if len(recommendations) >= n_recommendations:
                break
        
        return recommendations
    
    def get_similar_recipes(
        self,
        recipe_id: int,
        n_similar: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Find similar recipes to a given recipe
        
        Args:
            recipe_id: ID of the reference recipe
            n_similar: Number of similar recipes to return
        
        Returns:
            List of (recipe_id, similarity_score) tuples
        """
        if not self.is_trained:
            logger.warning("Model not trained, returning empty results")
            return []
        
        # Find index of the recipe
        try:
            recipe_idx = self.recipe_ids.index(recipe_id)
        except ValueError:
            logger.warning(f"Recipe {recipe_id} not found in trained model")
            return []
        
        # Get recipe vector
        recipe_vector = self.recipe_vectors[recipe_idx]
        
        # Calculate similarities
        similarities = cosine_similarity(recipe_vector, self.recipe_vectors)[0]
        
        # Get top N similar (excluding the recipe itself)
        top_indices = np.argsort(similarities)[::-1][1:n_similar+1]
        
        similar_recipes = []
        for idx in top_indices:
            similar_id = self.recipe_ids[idx]
            similarity = float(similarities[idx])
            similar_recipes.append((similar_id, similarity))
        
        return similar_recipes
    
    def save_model(self):
        """Save the trained model to disk"""
        if not self.is_trained:
            logger.warning("Cannot save untrained model")
            return
        
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'recipe_vectors': self.recipe_vectors,
                'recipe_ids': self.recipe_ids
            }
            
            model_file = os.path.join(self.model_path, 'recommendation_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Model saved to {model_file}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self):
        """Load a trained model from disk"""
        model_file = os.path.join(self.model_path, 'recommendation_model.pkl')
        
        if not os.path.exists(model_file):
            logger.info("No saved model found")
            return
        
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.recipe_vectors = model_data['recipe_vectors']
            self.recipe_ids = model_data['recipe_ids']
            self.is_trained = True
            
            logger.info(f"Model loaded from {model_file}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
    
    def get_model_stats(self) -> Dict:
        """Get statistics about the trained model"""
        if not self.is_trained:
            return {
                'is_trained': False,
                'num_recipes': 0,
                'num_features': 0
            }
        
        return {
            'is_trained': True,
            'num_recipes': len(self.recipe_ids),
            'num_features': self.recipe_vectors.shape[1],
            'vectorizer_type': 'TfidfVectorizer'
        }
