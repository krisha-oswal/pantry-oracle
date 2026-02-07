"""
OCR API endpoints for Pantry Oracle
"""

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from services.ocr_service import OCRService
import logging
import os

logger = logging.getLogger(__name__)

# Create blueprint
ocr_bp = Blueprint('ocr', __name__, url_prefix='/api/ocr')

# Initialize OCR service
ocr_service = OCRService()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ocr_bp.route('/scan', methods=['POST'])
def scan_image():
    """
    Scan an image and extract ingredients
    
    Request: multipart/form-data with 'image' file
    Optional: language parameter (default: 'eng')
    
    Response: {
        "ingredients": [...],
        "raw_text": "...",
        "confidence": 0.85,
        "language_detected": "eng"
    }
    """
    try:
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Get optional language parameter
        language = request.form.get('language', 'eng')
        
        # Read file data
        image_data = file.read()
        
        # Process image with OCR
        result = ocr_service.extract_ingredients_from_image(image_data, language)
        
        # Check for errors
        if 'error' in result:
            return jsonify({
                "error": result['error'],
                "ingredients": [],
                "confidence": 0.0
            }), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in OCR scan: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ocr_bp.route('/batch', methods=['POST'])
def scan_batch():
    """
    Scan multiple images and merge ingredients
    
    Request: multipart/form-data with multiple 'images[]' files
    
    Response: {
        "ingredients": [...],
        "results": [...],
        "total_images": 3
    }
    """
    try:
        # Check if images are in request
        if 'images' not in request.files:
            return jsonify({"error": "No image files provided"}), 400
        
        files = request.files.getlist('images')
        
        if len(files) == 0:
            return jsonify({"error": "No files selected"}), 400
        
        # Get optional language parameter
        language = request.form.get('language', 'eng')
        
        # Process all images
        image_data_list = []
        for file in files:
            if file and allowed_file(file.filename):
                image_data_list.append(file.read())
        
        if len(image_data_list) == 0:
            return jsonify({"error": "No valid image files"}), 400
        
        # Process batch
        results = ocr_service.process_batch_images(image_data_list, language)
        
        # Merge ingredients
        merged_ingredients = ocr_service.merge_ingredient_lists(results)
        
        return jsonify({
            "ingredients": merged_ingredients,
            "results": results,
            "total_images": len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error in batch OCR scan: {str(e)}")
        return jsonify({"error": str(e)}), 500


@ocr_bp.route('/health', methods=['GET'])
def health_check():
    """Check if OCR service is available"""
    return jsonify({
        "status": "ok",
        "tesseract_available": ocr_service.tesseract_available
    }), 200
