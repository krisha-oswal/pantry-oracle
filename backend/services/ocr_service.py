"""
OCR Service for Pantry Image Scanning
Uses Tesseract OCR to extract ingredients from images
"""

from typing import List, Dict, Optional
import logging
from PIL import Image
import io
import re

# Try to import pytesseract, but make it optional for now
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("pytesseract not available. OCR functionality will be limited.")

logger = logging.getLogger(__name__)


class OCRService:
    """
    Service for extracting ingredients from pantry images
    """
    
    def __init__(self):
        """Initialize the OCR service"""
        self.tesseract_available = TESSERACT_AVAILABLE
        
        # Common ingredient keywords to help with extraction
        self.ingredient_keywords = [
            'tomato', 'onion', 'garlic', 'ginger', 'potato', 'carrot',
            'chicken', 'beef', 'pork', 'fish', 'egg', 'milk', 'butter',
            'cheese', 'yogurt', 'cream', 'oil', 'salt', 'pepper', 'sugar',
            'flour', 'rice', 'pasta', 'bread', 'beans', 'lentils',
            'spinach', 'broccoli', 'cauliflower', 'cabbage', 'lettuce',
            'apple', 'banana', 'orange', 'lemon', 'lime', 'avocado'
        ]
    
    def extract_ingredients_from_image(
        self,
        image_data: bytes,
        language: str = 'eng'
    ) -> Dict:
        """
        Extract ingredients from an image using OCR
        
        Args:
            image_data: Image file data as bytes
            language: OCR language (default: 'eng')
        
        Returns:
            Dictionary with extracted ingredients and metadata
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR
            if self.tesseract_available:
                text = pytesseract.image_to_string(image, lang=language)
                confidence = self._estimate_confidence(text)
            else:
                # Fallback: return mock data
                logger.warning("Tesseract not available, returning mock data")
                text = "Mock OCR result - Tesseract not installed"
                confidence = 0.0
            
            # Extract ingredients from text
            ingredients = self._extract_ingredients_from_text(text)
            
            # Detect language
            detected_language = self._detect_language(text)
            
            return {
                'ingredients': ingredients,
                'raw_text': text,
                'confidence': confidence,
                'language_detected': detected_language,
                'image_size': image.size
            }
        
        except Exception as e:
            logger.error(f"Error in OCR processing: {str(e)}")
            return {
                'ingredients': [],
                'raw_text': '',
                'confidence': 0.0,
                'language_detected': 'unknown',
                'error': str(e)
            }
    
    def _extract_ingredients_from_text(self, text: str) -> List[str]:
        """
        Extract ingredient names from OCR text
        
        Args:
            text: Raw OCR text
        
        Returns:
            List of extracted ingredients
        """
        ingredients = []
        text_lower = text.lower()
        
        # Split into lines
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Skip empty lines
            if not line_lower:
                continue
            
            # Check if line contains ingredient keywords
            for keyword in self.ingredient_keywords:
                if keyword in line_lower:
                    # Clean up the line
                    cleaned = self._clean_ingredient_text(line)
                    if cleaned and cleaned not in ingredients:
                        ingredients.append(cleaned)
                    break
        
        return ingredients
    
    def _clean_ingredient_text(self, text: str) -> str:
        """
        Clean up extracted ingredient text
        
        Args:
            text: Raw ingredient text
        
        Returns:
            Cleaned ingredient name
        """
        # Remove numbers and common measurement units
        text = re.sub(r'\d+\.?\d*\s*(kg|g|lb|oz|ml|l|cup|tbsp|tsp)s?', '', text, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters
        text = re.sub(r'[^\w\s-]', '', text)
        
        return text
    
    def _estimate_confidence(self, text: str) -> float:
        """
        Estimate OCR confidence based on text quality
        
        Args:
            text: OCR extracted text
        
        Returns:
            Confidence score (0-1)
        """
        if not text:
            return 0.0
        
        # Simple heuristic: ratio of alphanumeric characters to total characters
        alphanumeric = sum(c.isalnum() for c in text)
        total = len(text)
        
        if total == 0:
            return 0.0
        
        confidence = alphanumeric / total
        return min(1.0, confidence)
    
    def _detect_language(self, text: str) -> str:
        """
        Detect language from text (simple heuristic)
        
        Args:
            text: Text to analyze
        
        Returns:
            Detected language code
        """
        # Simple detection: check for common Hindi/Indian language characters
        if any(ord(c) >= 0x0900 and ord(c) <= 0x097F for c in text):
            return 'hin'  # Hindi
        
        return 'eng'  # Default to English
    
    def process_batch_images(
        self,
        images: List[bytes],
        language: str = 'eng'
    ) -> List[Dict]:
        """
        Process multiple images in batch
        
        Args:
            images: List of image data
            language: OCR language
        
        Returns:
            List of OCR results
        """
        results = []
        
        for i, image_data in enumerate(images):
            logger.info(f"Processing image {i+1}/{len(images)}")
            result = self.extract_ingredients_from_image(image_data, language)
            results.append(result)
        
        return results
    
    def merge_ingredient_lists(self, ocr_results: List[Dict]) -> List[str]:
        """
        Merge ingredients from multiple OCR results
        
        Args:
            ocr_results: List of OCR result dictionaries
        
        Returns:
            Merged list of unique ingredients
        """
        all_ingredients = set()
        
        for result in ocr_results:
            ingredients = result.get('ingredients', [])
            all_ingredients.update(ingredients)
        
        return sorted(list(all_ingredients))
