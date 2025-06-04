import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class MedicalVisualization:
    """Creates visualizations for medical diagnosis results"""
    
    def __init__(self):
        # Set style for matplotlib
        plt.style.use('default')
        sns.set_palette("husl")
    
    def plot_prediction_confidence(self, predictions: Dict[str, float], title: str = "Prediction Confidence") -> None:
        """
        Create a bar chart showing prediction probabilities
        
        Args:
            predictions: Dictionary with class names as keys and probabilities as values
            title: Chart title
        """
        
        if not predictions:
            st.error("No prediction data to visualize")
            return
        
        # Create plotly bar chart
        classes = list(predictions.keys())
        probabilities = list(predictions.values())
        
        # Create color scale based on probability
        colors = ['#ff6b6b' if prob < 0.5 else '#51cf66' for prob in probabilities]
        
        fig = go.Figure(data=[
            go.Bar(
                x=classes,
                y=probabilities,
                marker_color=colors,
                text=[f'{prob:.1%}' for prob in probabilities],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Diagnosis",
            yaxis_title="Confidence",
            yaxis=dict(range=[0, 1], tickformat='.0%'),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def plot_model_performance(self, performance_metrics: Dict) -> None:
        """
        Create visualizations for model performance metrics
        
        Args:
            performance_metrics: Dictionary containing model performance data
        """
        
        if not performance_metrics:
            st.error("No performance data available")
            return
        
        # Create subplot with multiple metrics
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        positions = [(1,1), (1,2), (2,1), (2,2)]
        
        for metric, (row, col) in zip(metrics, positions):
            if metric in performance_metrics:
                value = performance_metrics[metric]
                
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number",
                        value=value,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': metric.replace('_', ' ').title()},
                        gauge={
                            'axis': {'range': [None, 1]},
                            'bar': {'color': self.get_performance_color(value)},
                            'steps': [
                                {'range': [0, 0.5], 'color': "lightgray"},
                                {'range': [0.5, 0.8], 'color': "yellow"},
                                {'range': [0.8, 1], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 0.9
                            }
                        }
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(height=600, title_text="Model Performance Metrics")
        st.plotly_chart(fig, use_container_width=True)
    
    def get_performance_color(self, value: float) -> str:
        """Get color based on performance value"""
        if value >= 0.8:
            return "green"
        elif value >= 0.6:
            return "orange"
        else:
            return "red"
    
    def plot_symptom_analysis(self, symptom_results: Dict) -> None:
        """
        Visualize symptom analysis results
        
        Args:
            symptom_results: Results from symptom analysis
        """
        
        if 'possible_conditions' not in symptom_results:
            st.error("No symptom analysis data to visualize")
            return
        
        conditions_data = symptom_results['possible_conditions']
        
        if not conditions_data:
            st.info("No matching conditions found")
            return
        
        # Extract conditions and scores
        conditions = [item[0] for item in conditions_data]
        scores = [item[1] for item in conditions_data]
        
        # Create horizontal bar chart
        fig = go.Figure(data=[
            go.Bar(
                y=conditions,
                x=scores,
                orientation='h',
                marker_color='lightblue',
                text=scores,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Possible Conditions Based on Symptoms",
            xaxis_title="Symptom Match Score",
            yaxis_title="Condition",
            height=max(400, len(conditions) * 50),
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add severity indicator
        severity = symptom_results.get('severity', 'unknown')
        severity_colors = {
            'low': 'green',
            'medium': 'orange', 
            'high': 'red'
        }
        
        st.markdown(f"""
        <div style="padding: 10px; border-left: 4px solid {severity_colors.get(severity, 'gray')}; 
                    background-color: #f0f0f0; margin: 10px 0;">
            <strong>Severity Level: {severity.upper()}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    def create_confidence_meter(self, confidence: float, threshold: float = 0.8) -> None:
        """
        Create a confidence meter visualization
        
        Args:
            confidence: Confidence score (0-1)
            threshold: Threshold for high confidence
        """
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = confidence,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Prediction Confidence"},
            delta = {'reference': threshold},
            gauge = {
                'axis': {'range': [None, 1]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.5], 'color': "lightgray"},
                    {'range': [0.5, threshold], 'color': "yellow"},
                    {'range': [threshold, 1], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': threshold
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add interpretation
        if confidence >= threshold:
            st.success(f"High confidence prediction ({confidence:.1%})")
        elif confidence >= 0.6:
            st.warning(f"Moderate confidence prediction ({confidence:.1%})")
        else:
            st.error(f"Low confidence prediction ({confidence:.1%}) - Results may be unreliable")
    
    def plot_image_preprocessing_comparison(self, original_image, processed_image):
        """Show before/after image preprocessing"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Original image
        ax1.imshow(original_image)
        ax1.set_title("Original Image")
        ax1.axis('off')
        
        # Processed image
        # Handle different image formats for display
        if processed_image.shape[-1] == 3:
            # RGB image
            display_image = processed_image
            # Denormalize if needed (assuming ImageNet normalization)
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            display_image = (display_image * std + mean)
            display_image = np.clip(display_image, 0, 1)
        else:
            display_image = processed_image
        
        ax2.imshow(display_image)
        ax2.set_title("Preprocessed Image")
        ax2.axis('off')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    def create_risk_assessment_chart(self, risk_factors: Dict[str, float]):
        """Create a risk assessment visualization"""
        
        if not risk_factors:
            st.info("No risk factors to display")
            return
        
        # Create radar chart for risk factors
        categories = list(risk_factors.keys())
        values = list(risk_factors.values())
        
        # Close the radar chart
        categories += [categories[0]]
        values += [values[0]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Risk Assessment',
            line_color='red'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Risk Factor Assessment"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_diagnostic_summary(self, diagnosis_data: Dict):
        """Display a comprehensive diagnostic summary"""
        
        st.subheader("📋 Diagnostic Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'predicted_class' in diagnosis_data:
                st.metric(
                    label="Primary Diagnosis",
                    value=diagnosis_data['predicted_class']
                )
        
        with col2:
            if 'confidence' in diagnosis_data:
                st.metric(
                    label="Confidence Level",
                    value=f"{diagnosis_data['confidence']:.1%}"
                )
        
        with col3:
            if 'model_info' in diagnosis_data and 'name' in diagnosis_data['model_info']:
                st.metric(
                    label="Model Used",
                    value=diagnosis_data['model_info']['name'][:20] + "..."
                )
        
        # Additional details in expandable section
        with st.expander("Detailed Analysis"):
            if 'predictions' in diagnosis_data:
                st.write("**All Predictions:**")
                for condition, probability in diagnosis_data['predictions'].items():
                    st.write(f"- {condition}: {probability:.1%}")
            
            if 'model_info' in diagnosis_data:
                st.write("**Model Information:**")
                model_info = diagnosis_data['model_info']
                if 'description' in model_info:
                    st.write(f"- Description: {model_info['description']}")
                if 'classes' in model_info:
                    st.write(f"- Classes: {', '.join(model_info['classes'])}")
