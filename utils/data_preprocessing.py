import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import streamlit as st
from typing import Tuple, Optional

class MedicalImagePreprocessor:
    """Handles preprocessing of medical images for AI analysis without OpenCV dependency"""
    
    def __init__(self):
        self.target_sizes = {
            'chest_xray': (224, 224),
            'skin_lesion': (224, 224)
        }
    
    def preprocess_image(self, image: Image.Image, model_type: str) -> Optional[np.ndarray]:
        """
        Preprocess uploaded image for model prediction
        
        Args:
            image: PIL Image object
            model_type: Type of model ('chest_xray' or 'skin_lesion')
            
        Returns:
            Preprocessed numpy array or None if error
        """
        
        try:
            if model_type not in self.target_sizes:
                st.error(f"Unknown model type: {model_type}")
                return None
            
            target_size = self.target_sizes[model_type]
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Normalize pixel values to [0, 1]
            img_array = img_array.astype(np.float32) / 255.0
            
            # Apply model-specific preprocessing
            if model_type == 'chest_xray':
                img_array = self.preprocess_chest_xray(img_array)
            elif model_type == 'skin_lesion':
                img_array = self.preprocess_skin_lesion(img_array)
            
            return img_array
            
        except Exception as e:
            st.error(f"Image preprocessing error: {str(e)}")
            return None
    
    def preprocess_chest_xray(self, img_array: np.ndarray) -> np.ndarray:
        """Specific preprocessing for chest X-ray images using PIL only"""
        
        # Convert to PIL Image for processing
        img_pil = Image.fromarray((img_array * 255).astype(np.uint8))
        
        # Convert to grayscale and back to RGB for consistency
        gray = img_pil.convert('L')
        
        # Enhance contrast (alternative to CLAHE)
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)  # Increase contrast
        
        # Convert back to RGB
        enhanced_rgb = enhanced.convert('RGB')
        enhanced_array = np.array(enhanced_rgb).astype(np.float32) / 255.0
        
        # ImageNet normalization (since we use pre-trained models)
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        
        normalized = (enhanced_array - mean) / std
        
        return normalized
    
    def preprocess_skin_lesion(self, img_array: np.ndarray) -> np.ndarray:
        """Specific preprocessing for skin lesion images using PIL only"""
        
        # Convert to PIL Image for processing
        img_pil = Image.fromarray((img_array * 255).astype(np.uint8))
        
        # Apply slight blur to reduce noise
        blurred = img_pil.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(blurred)
        enhanced = enhancer.enhance(1.2)
        
        # Enhance brightness slightly
        brightness_enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = brightness_enhancer.enhance(1.1)
        
        # Convert back to array
        enhanced_array = np.array(enhanced).astype(np.float32) / 255.0
        
        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        
        normalized = (enhanced_array - mean) / std
        
        return normalized
    
    def validate_image(self, image: Image.Image, model_type: str) -> Tuple[bool, str]:
        """
        Validate uploaded image for medical analysis
        
        Returns:
            (is_valid, error_message)
        """
        
        try:
            # Check image format
            if image.format not in ['JPEG', 'PNG', 'JPG']:
                return False, "Please upload JPEG or PNG images only"
            
            # Check image size
            width, height = image.size
            if width < 100 or height < 100:
                return False, "Image too small. Minimum size: 100x100 pixels"
            
            if width > 2000 or height > 2000:
                return False, "Image too large. Maximum size: 2000x2000 pixels"
            
            # Check file size (approximate)
            img_array = np.array(image)
            estimated_size_mb = img_array.nbytes / (1024 * 1024)
            
            if estimated_size_mb > 10:
                return False, "Image file too large. Maximum size: 10MB"
            
            # Model-specific validations
            if model_type == 'chest_xray':
                return self.validate_chest_xray(image)
            elif model_type == 'skin_lesion':
                return self.validate_skin_lesion(image)
            
            return True, ""
            
        except Exception as e:
            return False, f"Image validation error: {str(e)}"
    
    def validate_chest_xray(self, image: Image.Image) -> Tuple[bool, str]:
        """Validate chest X-ray specific requirements"""
        
        # Convert to grayscale to check if it's likely an X-ray
        gray_image = image.convert('L')
        img_array = np.array(gray_image)
        
        # Check if image has appropriate contrast for X-ray
        contrast = np.std(img_array)
        if contrast < 30:
            return False, "Image appears to have low contrast. Please ensure it's a proper X-ray image."
        
        # Check aspect ratio (X-rays are typically portrait or square)
        width, height = image.size
        aspect_ratio = width / height
        
        if aspect_ratio > 1.5 or aspect_ratio < 0.5:
            return False, "Unusual aspect ratio for chest X-ray. Please check image orientation."
        
        return True, ""
    
    def validate_skin_lesion(self, image: Image.Image) -> Tuple[bool, str]:
        """Validate skin lesion specific requirements"""
        
        # Convert to RGB for analysis
        rgb_image = image.convert('RGB')
        img_array = np.array(rgb_image)
        
        # Check if image has color information (not purely grayscale)
        r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
        
        # Calculate color variance
        color_variance = np.var(r) + np.var(g) + np.var(b)
        
        if color_variance < 1000:
            return False, "Image appears to lack color information. Skin lesion analysis works best with color images."
        
        # Check for extreme brightness or darkness
        brightness = np.mean(img_array)
        
        if brightness < 30:
            return False, "Image too dark. Please ensure proper lighting."
        elif brightness > 225:
            return False, "Image too bright. Please reduce exposure."
        
        return True, ""
    
    def get_image_stats(self, image: Image.Image) -> dict:
        """Get statistical information about the image"""
        
        try:
            img_array = np.array(image)
            
            stats = {
                'size': image.size,
                'mode': image.mode,
                'format': image.format,
                'mean_intensity': np.mean(img_array),
                'std_intensity': np.std(img_array),
                'min_intensity': np.min(img_array),
                'max_intensity': np.max(img_array)
            }
            
            if len(img_array.shape) == 3:
                stats['channels'] = img_array.shape[2]
                stats['mean_per_channel'] = [np.mean(img_array[:,:,i]) for i in range(img_array.shape[2])]
            
            return stats
            
        except Exception as e:
            return {'error': str(e)}

class PatientDataValidator:
    """Validates patient data inputs"""
    
    @staticmethod
    def validate_age(age: int) -> Tuple[bool, str]:
        """Validate patient age"""
        if age < 0 or age > 150:
            return False, "Please enter a valid age between 0 and 150"
        return True, ""
    
    @staticmethod
    def validate_symptoms(symptoms: list) -> Tuple[bool, str]:
        """Validate symptom list"""
        if not symptoms:
            return False, "Please select at least one symptom"
        
        if len(symptoms) > 20:
            return False, "Please select no more than 20 symptoms"
        
        return True, ""
    
    @staticmethod
    def sanitize_text_input(text: str) -> str:
        """Sanitize text input to prevent issues"""
        if not text:
            return ""
        
        # Remove potentially harmful characters
        sanitized = ''.join(char for char in text if char.isalnum() or char.isspace() or char in '.-_')
        
        # Limit length
        return sanitized[:500]