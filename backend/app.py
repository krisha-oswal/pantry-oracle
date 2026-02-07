"""
Pantry Oracle - Flask Backend API
Main application entry point
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import os
from dotenv import load_dotenv
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS - Use environment variable for allowed origins
allowed_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Configure caching
cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Configure rate limiting from environment
rate_limit_per_hour = os.getenv('RATE_LIMIT_PER_HOUR', '50')
rate_limit_per_day = os.getenv('RATE_LIMIT_PER_DAY', '200')
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{rate_limit_per_day} per day", f"{rate_limit_per_hour} per hour"]
)

# Setup logging
logger = setup_logger(__name__)

# Import services
from services.recipe_engine import RecipeEngine
from services.nutrition_calculator import NutritionCalculator
from services.indianization_engine import IndianizationEngine
from services.ocr_service import OCRService
from services.metrics_tracker import MetricsTracker
from ml.recommendation_engine import MLRecommendationEngine

# Import API blueprints
from api.metrics_api import metrics_bp, get_metrics_tracker
from api.ocr_api import ocr_bp

# Initialize services
recipe_engine = RecipeEngine()
nutrition_calculator = NutritionCalculator()
indianization_engine = IndianizationEngine()
ocr_service = OCRService()
metrics_tracker = MetricsTracker()
ml_engine = MLRecommendationEngine()

# Register blueprints
app.register_blueprint(metrics_bp)
app.register_blueprint(ocr_bp)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Pantry Oracle API"}), 200

@app.route('/api/recipes/search', methods=['POST'])
@limiter.limit("30 per minute")
def search_recipes():
    """
    Search recipes based on pantry ingredients and preferences
    Request: {
        "ingredients": ["tomato", "butter", "onion"],
        "diet": "vegetarian",
        "maxTime": 30,
        "indianize": false,
        "region": "north",
        "page": 1,
        "limit": 20
    }
    """
    import time
    start_time = time.time()
    
    try:
        data = request.get_json()
        logger.info(f"Recipe search request: {data}")
        
        ingredients = data.get('ingredients', [])
        max_time = data.get('maxTime')
        diet = data.get('diet')
        page = data.get('page', 1)
        limit = data.get('limit', 20)
        
        # Search recipes
        results = recipe_engine.search_recipes(
            pantry_ingredients=ingredients,
            max_time=max_time,
            diet=diet,
            page=page,
            limit=limit
        )
        
        # Track metrics
        search_time_ms = (time.time() - start_time) * 1000
        top_coverage = results['recipes'][0]['pantry_coverage'] if results['recipes'] else 0
        
        metrics_tracker.track_recipe_search(
            pantry_ingredients=ingredients,
            results_count=results['total_results'],
            top_coverage=top_coverage,
            search_time_ms=search_time_ms
        )
        
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Error in recipe search: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """
    Get a specific recipe by ID
    """
    try:
        logger.info(f"Get recipe request: {recipe_id}")
        
        recipe = recipe_engine.get_recipe_by_id(recipe_id)
        
        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404
        
        return jsonify(recipe), 200
    except Exception as e:
        logger.error(f"Error getting recipe: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/pantry/ocr', methods=['POST'])
@limiter.limit("10 per minute")
def ocr_pantry():
    """
    OCR endpoint for pantry image scanning
    Request: multipart/form-data with image file
    """
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        image_file = request.files['image']
        logger.info(f"OCR request for file: {image_file.filename}")
        
        # Read image data
        image_data = image_file.read()
        
        # Process with OCR
        result = ocr_service.extract_ingredients_from_image(image_data)
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error in OCR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/nutrition/calculate', methods=['POST'])
def calculate_nutrition():
    """
    Calculate nutrition for a recipe
    Request: {
        "recipe_id": 137739,
        "servings": 2
    }
    """
    try:
        data = request.get_json()
        logger.info(f"Nutrition calculation request: {data}")
        
        recipe_id = data.get('recipe_id')
        servings = data.get('servings')
        
        # Get recipe
        recipe = recipe_engine.get_recipe_by_id(recipe_id)
        
        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404
        
        # Calculate nutrition
        nutrition = nutrition_calculator.calculate_recipe_nutrition(recipe, servings)
        
        # Add macro percentages and health score
        nutrition['macro_percentages'] = nutrition_calculator.calculate_macros_percentage(
            nutrition['per_serving']
        )
        nutrition['health_score'] = nutrition_calculator.get_health_score(
            nutrition['total']
        )
        
        return jsonify(nutrition), 200
    except Exception as e:
        logger.error(f"Error in nutrition calculation: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/indianize', methods=['POST'])
def indianize_recipe():
    """
    Indianize a recipe
    Request: {
        "recipe_id": 31490,
        "region": "south"
    }
    """
    try:
        data = request.get_json()
        logger.info(f"Indianization request: {data}")
        
        recipe_id = data.get('recipe_id')
        region = data.get('region', 'north')
        
        # Get recipe
        recipe = recipe_engine.get_recipe_by_id(recipe_id)
        
        if recipe is None:
            return jsonify({"error": "Recipe not found"}), 404
        
        # Indianize recipe
        indianized = indianization_engine.indianize_recipe(recipe, region)
        
        return jsonify(indianized), 200
    except Exception as e:
        logger.error(f"Error in Indianization: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/regions/<string:region>', methods=['GET'])
def get_regional_info(region):
    """
    Get information about a specific Indian region's cuisine
    """
    try:
        logger.info(f"Regional info request: {region}")
        
        info = indianization_engine.get_regional_info(region)
        
        return jsonify(info), 200
    except Exception as e:
        logger.error(f"Error getting regional info: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Get configuration from environment
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    env = os.getenv('FLASK_ENV', 'development')
    
    logger.info(f"Starting Pantry Oracle API server in {env} mode...")
    logger.info(f"Allowed CORS origins: {allowed_origins}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)


