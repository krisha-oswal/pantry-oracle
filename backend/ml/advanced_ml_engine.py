"""
Advanced ML Recommendation Engine with FAISS
Implements fast similarity search using FAISS index
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
import pickle
import os

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS not available. Install with: pip install faiss-cpu")

from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


class AdvancedMLEngine:
    """
    Advanced ML recommendation engine with FAISS for fast similarity search
    """
    
    def __init__(self, model_path: str = 'ml/models'):
        """Initialize the advanced ML engine"""
        self.model_path = model_path
        self.vectorizer = None
        self.faiss_index = None
        self.recipe_ids = []
        self.recipe_vectors = None
        self.is_trained = False
        self.use_faiss = FAISS_AVAILABLE
        
        os.makedirs(model_path, exist_ok=True)
        self.load_model()
    
    def train(self, recipes: List[Dict], use_faiss: bool = True):
        """
        Train the recommendation model with FAISS indexing
        
        Args:
            recipes: List of recipe dictionaries
            use_faiss: Whether to use FAISS for indexing
        """
        if not recipes:
            logger.warning("No recipes provided for training")
            return
        
        logger.info(f"Training advanced ML model on {len(recipes)} recipes")
        
        # Extract recipe IDs
        self.recipe_ids = [recipe.get('id', i) for i, recipe in enumerate(recipes)]
        
        # Create text representations
        recipe_texts = []
        for recipe in recipes:
            ingredients = ' '.join(recipe.get('ingredients', []))
            tags = ' '.join(recipe.get('tags', []))
            name = recipe.get('name', '')
            text = f"{name} {ingredients} {tags}"
            recipe_texts.append(text)
        
        # Train TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=500,  # Reduced for FAISS efficiency
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1
        )
        
        # Get TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(recipe_texts)
        self.recipe_vectors = tfidf_matrix.toarray().astype('float32')
        
        # Build FAISS index if available
        if use_faiss and FAISS_AVAILABLE:
            self._build_faiss_index()
        
        self.is_trained = True
        logger.info("Advanced ML model training completed")
        self.save_model()
    
    def _build_faiss_index(self):
        """Build FAISS index for fast similarity search"""
        if self.recipe_vectors is None:
            return
        
        dimension = self.recipe_vectors.shape[1]
        
        # Normalize vectors for cosine similarity
        faiss.normalize_L2(self.recipe_vectors)
        
        # Create FAISS index (using IndexFlatIP for inner product = cosine similarity)
        self.faiss_index = faiss.IndexFlatIP(dimension)
        self.faiss_index.add(self.recipe_vectors)
        
        logger.info(f"FAISS index built with {self.faiss_index.ntotal} vectors")
    
    def get_recommendations(
        self,
        pantry_ingredients: List[str],
        n_recommendations: int = 10,
        exclude_ids: Optional[List[int]] = None,
        min_score: float = 0.0
    ) -> List[Tuple[int, float]]:
        """
        Get recipe recommendations using FAISS
        
        Args:
            pantry_ingredients: List of available ingredients
            n_recommendations: Number of recommendations
            exclude_ids: Recipe IDs to exclude
            min_score: Minimum similarity score
        
        Returns:
            List of (recipe_id, similarity_score) tuples
        """
        if not self.is_trained:
            logger.warning("Model not trained")
            return []
        
        # Create query vector
        query_text = ' '.join(pantry_ingredients)
        query_vector = self.vectorizer.transform([query_text]).toarray().astype('float32')
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_vector)
        
        # Search using FAISS if available
        if self.use_faiss and self.faiss_index is not None:
            # Search for more results to account for exclusions
            k = min(n_recommendations * 3, len(self.recipe_ids))
            distances, indices = self.faiss_index.search(query_vector, k)
            
            recommendations = []
            for idx, score in zip(indices[0], distances[0]):
                if idx < 0 or idx >= len(self.recipe_ids):
                    continue
                
                recipe_id = self.recipe_ids[idx]
                
                # Skip excluded recipes
                if exclude_ids and recipe_id in exclude_ids:
                    continue
                
                # Skip low scores
                if score < min_score:
                    continue
                
                recommendations.append((recipe_id, float(score)))
                
                if len(recommendations) >= n_recommendations:
                    break
            
            return recommendations
        else:
            # Fallback to numpy-based search
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(query_vector, self.recipe_vectors)[0]
            
            # Get top indices
            top_indices = np.argsort(similarities)[::-1]
            
            recommendations = []
            for idx in top_indices:
                recipe_id = self.recipe_ids[idx]
                
                if exclude_ids and recipe_id in exclude_ids:
                    continue
                
                similarity = float(similarities[idx])
                if similarity < min_score:
                    continue
                
                recommendations.append((recipe_id, similarity))
                
                if len(recommendations) >= n_recommendations:
                    break
            
            return recommendations
    
    def get_similar_recipes(
        self,
        recipe_id: int,
        n_similar: int = 5
    ) -> List[Tuple[int, float]]:
        """Find similar recipes using FAISS"""
        if not self.is_trained:
            return []
        
        try:
            recipe_idx = self.recipe_ids.index(recipe_id)
        except ValueError:
            logger.warning(f"Recipe {recipe_id} not found")
            return []
        
        # Get recipe vector
        recipe_vector = self.recipe_vectors[recipe_idx:recipe_idx+1]
        
        if self.use_faiss and self.faiss_index is not None:
            # Search for n+1 to exclude the recipe itself
            distances, indices = self.faiss_index.search(recipe_vector, n_similar + 1)
            
            similar_recipes = []
            for idx, score in zip(indices[0], distances[0]):
                if idx == recipe_idx:  # Skip the recipe itself
                    continue
                
                similar_id = self.recipe_ids[idx]
                similar_recipes.append((similar_id, float(score)))
                
                if len(similar_recipes) >= n_similar:
                    break
            
            return similar_recipes
        else:
            # Fallback
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(recipe_vector, self.recipe_vectors)[0]
            top_indices = np.argsort(similarities)[::-1][1:n_similar+1]
            
            return [(self.recipe_ids[idx], float(similarities[idx])) for idx in top_indices]
    
    def save_model(self):
        """Save model to disk"""
        if not self.is_trained:
            return
        
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'recipe_vectors': self.recipe_vectors,
                'recipe_ids': self.recipe_ids,
                'use_faiss': self.use_faiss
            }
            
            model_file = os.path.join(self.model_path, 'advanced_ml_model.pkl')
            with open(model_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            # Save FAISS index separately
            if self.use_faiss and self.faiss_index is not None:
                faiss_file = os.path.join(self.model_path, 'faiss_index.bin')
                faiss.write_index(self.faiss_index, faiss_file)
            
            logger.info(f"Advanced model saved to {model_file}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self):
        """Load model from disk"""
        model_file = os.path.join(self.model_path, 'advanced_ml_model.pkl')
        
        if not os.path.exists(model_file):
            return
        
        try:
            with open(model_file, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.recipe_vectors = model_data['recipe_vectors']
            self.recipe_ids = model_data['recipe_ids']
            self.use_faiss = model_data.get('use_faiss', False)
            
            # Load FAISS index
            if self.use_faiss and FAISS_AVAILABLE:
                faiss_file = os.path.join(self.model_path, 'faiss_index.bin')
                if os.path.exists(faiss_file):
                    self.faiss_index = faiss.read_index(faiss_file)
            
            self.is_trained = True
            logger.info(f"Advanced model loaded from {model_file}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
    
    def get_model_stats(self) -> Dict:
        """Get model statistics"""
        if not self.is_trained:
            return {
                'is_trained': False,
                'num_recipes': 0,
                'num_features': 0,
                'using_faiss': False
            }
        
        return {
            'is_trained': True,
            'num_recipes': len(self.recipe_ids),
            'num_features': self.recipe_vectors.shape[1],
            'using_faiss': self.use_faiss and self.faiss_index is not None,
            'faiss_total_vectors': self.faiss_index.ntotal if self.faiss_index else 0
        }
