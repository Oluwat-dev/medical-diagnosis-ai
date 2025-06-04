import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, applications
import numpy as np
import os
from typing import Dict, List, Tuple, Optional
import streamlit as st

class ModelManager:
    """Manages medical AI models for diagnosis"""
    
    def __init__(self):
        self.models = {}
        self.model_info = {
            'chest_xray': {
                'name': 'Chest X-Ray Pneumonia Detection',
                'classes': ['Normal', 'Pneumonia'],
                'input_shape': (224, 224, 3),
                'description': 'Detects pneumonia from chest X-ray images'
            },
            'skin_lesion': {
                'name': 'Skin Lesion Classification',
                'classes': ['Benign', 'Malignant'],
                'input_shape': (224, 224, 3),
                'description': 'Classifies skin lesions as benign or malignant'
            }
        }
    
    def create_chest_xray_model(self) -> keras.Model:
        """Create a chest X-ray classification model using transfer learning"""
        
        # Use ResNet50 as base model
        base_model = applications.ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=self.model_info['chest_xray']['input_shape']
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification head
        model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.5),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(len(self.model_info['chest_xray']['classes']), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def create_skin_lesion_model(self) -> keras.Model:
        """Create a skin lesion classification model using transfer learning"""
        
        # Use EfficientNetB0 as base model
        base_model = applications.EfficientNetB0(
            weights='imagenet',
            include_top=False,
            input_shape=self.model_info['skin_lesion']['input_shape']
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom classification head
        model = keras.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.6),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.4),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(len(self.model_info['skin_lesion']['classes']), activation='softmax')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def get_model(self, model_type: str) -> keras.Model:
        """Get or create a model of specified type"""
        
        if model_type not in self.models:
            if model_type == 'chest_xray':
                self.models[model_type] = self.create_chest_xray_model()
            elif model_type == 'skin_lesion':
                self.models[model_type] = self.create_skin_lesion_model()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
        
        return self.models[model_type]
    
    def predict(self, model_type: str, image: np.ndarray) -> Dict:
        """Make prediction using specified model"""
        
        try:
            model = self.get_model(model_type)
            
            # Preprocess image
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Make prediction
            predictions = model.predict(image, verbose=0)
            
            # Get class probabilities
            class_names = self.model_info[model_type]['classes']
            probabilities = predictions[0]
            
            # Create result dictionary
            result = {
                'predictions': {
                    class_names[i]: float(prob) 
                    for i, prob in enumerate(probabilities)
                },
                'predicted_class': class_names[np.argmax(probabilities)],
                'confidence': float(np.max(probabilities)),
                'model_info': self.model_info[model_type]
            }
            
            return result
            
        except Exception as e:
            st.error(f"Prediction error: {str(e)}")
            return None
    
    def get_model_summary(self, model_type: str) -> str:
        """Get model architecture summary"""
        
        try:
            model = self.get_model(model_type)
            
            # Capture model summary
            summary_list = []
            model.summary(print_fn=lambda x: summary_list.append(x))
            
            return '\n'.join(summary_list)
            
        except Exception as e:
            return f"Error getting model summary: {str(e)}"
    
    def evaluate_model_performance(self, model_type: str) -> Dict:
        """Get model performance metrics (simulated for demo)"""
        
        # In a real application, these would be calculated from validation data
        performance_metrics = {
            'chest_xray': {
                'accuracy': 0.87,
                'precision': 0.85,
                'recall': 0.89,
                'f1_score': 0.87,
                'auc_roc': 0.92,
                'validation_samples': 1000
            },
            'skin_lesion': {
                'accuracy': 0.82,
                'precision': 0.80,
                'recall': 0.84,
                'f1_score': 0.82,
                'auc_roc': 0.88,
                'validation_samples': 800
            }
        }
        
        return performance_metrics.get(model_type, {})

class MedicalSymptomAnalyzer:
    """Rule-based symptom analysis system"""
    
    def __init__(self):
        self.symptom_conditions = {
            # Respiratory symptoms
            'cough': ['Common Cold', 'Flu', 'Bronchitis', 'Pneumonia', 'COVID-19'],
            'fever': ['Flu', 'Infection', 'COVID-19', 'Pneumonia'],
            'shortness_of_breath': ['Asthma', 'COPD', 'Pneumonia', 'Heart Disease', 'COVID-19'],
            'chest_pain': ['Heart Disease', 'Pneumonia', 'Anxiety', 'Muscle Strain'],
            
            # Gastrointestinal symptoms
            'nausea': ['Food Poisoning', 'Gastritis', 'Pregnancy', 'Migraine'],
            'vomiting': ['Food Poisoning', 'Gastritis', 'Migraine', 'Appendicitis'],
            'diarrhea': ['Food Poisoning', 'IBS', 'Infection', 'Stress'],
            'stomach_pain': ['Gastritis', 'Appendicitis', 'IBS', 'Food Poisoning'],
            
            # Neurological symptoms
            'headache': ['Tension Headache', 'Migraine', 'Dehydration', 'Stress'],
            'dizziness': ['Dehydration', 'Low Blood Pressure', 'Inner Ear Problem'],
            'fatigue': ['Anemia', 'Depression', 'Sleep Disorder', 'Thyroid Disease'],
            
            # Skin symptoms
            'rash': ['Allergy', 'Eczema', 'Contact Dermatitis', 'Infection'],
            'itching': ['Allergy', 'Dry Skin', 'Eczema', 'Infection']
        }
        
        self.severity_indicators = {
            'high': ['chest_pain', 'shortness_of_breath', 'severe_headache', 'high_fever'],
            'medium': ['persistent_cough', 'vomiting', 'severe_stomach_pain'],
            'low': ['mild_headache', 'fatigue', 'mild_cough', 'rash']
        }
    
    def analyze_symptoms(self, symptoms: List[str]) -> Dict:
        """Analyze list of symptoms and return possible conditions"""
        
        if not symptoms:
            return {'error': 'No symptoms provided'}
        
        # Count condition occurrences
        condition_scores = {}
        
        for symptom in symptoms:
            if symptom in self.symptom_conditions:
                for condition in self.symptom_conditions[symptom]:
                    condition_scores[condition] = condition_scores.get(condition, 0) + 1
        
        # Sort conditions by score
        sorted_conditions = sorted(
            condition_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Determine severity
        severity = 'low'
        for symptom in symptoms:
            if symptom in self.severity_indicators['high']:
                severity = 'high'
                break
            elif symptom in self.severity_indicators['medium']:
                severity = 'medium'
        
        # Generate recommendations
        recommendations = self.generate_recommendations(severity, symptoms)
        
        return {
            'possible_conditions': sorted_conditions[:5],  # Top 5 conditions
            'severity': severity,
            'recommendations': recommendations,
            'total_symptoms': len(symptoms),
            'matched_symptoms': len([s for s in symptoms if s in self.symptom_conditions])
        }
    
    def generate_recommendations(self, severity: str, symptoms: List[str]) -> List[str]:
        """Generate medical recommendations based on severity and symptoms"""
        
        recommendations = []
        
        if severity == 'high':
            recommendations.extend([
                "🚨 Seek immediate medical attention",
                "Consider visiting emergency room if severe",
                "Do not delay medical consultation"
            ])
        elif severity == 'medium':
            recommendations.extend([
                "Schedule appointment with healthcare provider",
                "Monitor symptoms closely",
                "Seek medical advice within 24-48 hours"
            ])
        else:
            recommendations.extend([
                "Monitor symptoms for changes",
                "Consider over-the-counter remedies if appropriate",
                "Consult healthcare provider if symptoms persist"
            ])
        
        # Add general recommendations
        recommendations.extend([
            "Stay hydrated and get adequate rest",
            "Keep a symptom diary",
            "Avoid self-medication without professional guidance"
        ])
        
        return recommendations
