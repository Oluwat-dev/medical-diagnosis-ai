import streamlit as st
from PIL import Image
import numpy as np
from models.medical_models import ModelManager
from utils.data_preprocessing import MedicalImagePreprocessor
from utils.visualization import MedicalVisualization
import io

def show_chest_xray_page():
    """Display the chest X-ray analysis page"""
    
    st.title("🫁 Chest X-Ray Analysis")
    st.markdown("""
    Upload a chest X-ray image to analyze for potential pneumonia and other respiratory conditions.
    This AI system uses deep learning to assist in medical image interpretation.
    """)
    
    # Medical disclaimer for this specific analysis
    st.error("""
    ⚠️ **IMPORTANT MEDICAL DISCLAIMER**
    
    This chest X-ray analysis tool is for educational and research purposes only.
    - **NOT for clinical diagnosis**: Do not use for actual patient care
    - **Always consult radiologists**: Professional interpretation is essential
    - **Emergency cases**: Seek immediate medical attention for severe symptoms
    """)
    
    # Initialize components
    model_manager = ModelManager()
    preprocessor = MedicalImagePreprocessor()
    visualizer = MedicalVisualization()
    
    # File upload section
    st.header("📤 Upload Chest X-Ray Image")
    
    uploaded_file = st.file_uploader(
        "Choose a chest X-ray image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear chest X-ray image in PNG or JPEG format",
        key="chest_xray_uploader"
    )
    
    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            
            # Display original image
            st.subheader("📸 Uploaded Image")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(image, caption="Original Chest X-Ray", use_column_width=True)
            
            with col2:
                # Image statistics
                img_stats = preprocessor.get_image_stats(image)
                st.write("**Image Properties:**")
                if 'error' not in img_stats:
                    st.write(f"- Size: {img_stats['size'][0]}×{img_stats['size'][1]}")
                    st.write(f"- Format: {img_stats['format']}")
                    st.write(f"- Mode: {img_stats['mode']}")
                    st.write(f"- Mean Intensity: {img_stats['mean_intensity']:.1f}")
            
            # Validate image
            is_valid, error_message = preprocessor.validate_image(image, 'chest_xray')
            
            if not is_valid:
                st.error(f"Image validation failed: {error_message}")
                return
            
            st.success("✅ Image validation passed")
            
            # Analysis options
            st.header("⚙️ Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                show_preprocessing = st.checkbox("Show preprocessing steps", value=False, key="chest_xray_preprocessing")
                confidence_threshold = st.slider(
                    "Confidence threshold for alerts",
                    min_value=0.5,
                    max_value=0.95,
                    value=0.8,
                    step=0.05,
                    help="Threshold for high-confidence predictions",
                    key="chest_xray_confidence"
                )
            
            with col2:
                show_model_info = st.checkbox("Show model information", value=False, key="chest_xray_model_info")
                show_performance = st.checkbox("Show model performance metrics", value=False, key="chest_xray_performance")
            
            # Run analysis button
            if st.button("🔍 Analyze X-Ray", type="primary", use_container_width=True, key="chest_xray_analyze"):
                
                with st.spinner("Preprocessing image..."):
                    # Preprocess the image
                    processed_image = preprocessor.preprocess_image(image, 'chest_xray')
                    
                    if processed_image is None:
                        st.error("Failed to preprocess image")
                        return
                
                # Show preprocessing comparison if requested
                if show_preprocessing:
                    st.subheader("🔄 Image Preprocessing")
                    visualizer.plot_image_preprocessing_comparison(
                        np.array(image), 
                        processed_image
                    )
                
                with st.spinner("Running AI analysis..."):
                    # Make prediction
                    prediction_result = model_manager.predict('chest_xray', processed_image)
                    
                    if prediction_result is None:
                        st.error("Failed to analyze image")
                        return
                
                # Display results
                st.header("📊 Analysis Results")
                
                # Main prediction display
                visualizer.display_diagnostic_summary(prediction_result)
                
                # Confidence visualization
                st.subheader("📈 Prediction Confidence")
                visualizer.create_confidence_meter(
                    prediction_result['confidence'], 
                    confidence_threshold
                )
                
                # Detailed predictions
                st.subheader("📋 Detailed Predictions")
                visualizer.plot_prediction_confidence(
                    prediction_result['predictions'],
                    "Chest X-Ray Analysis Results"
                )
                
                # Clinical interpretation
                st.subheader("🩺 Clinical Interpretation")
                interpret_chest_xray_results(prediction_result, confidence_threshold)
                
                # Recommendations
                st.subheader("💡 Recommendations")
                provide_chest_xray_recommendations(prediction_result)
            
            # Model information section
            if show_model_info:
                st.header("🧠 Model Information")
                
                with st.expander("Model Architecture Details"):
                    model_summary = model_manager.get_model_summary('chest_xray')
                    st.text(model_summary)
                
                model_info = model_manager.model_info['chest_xray']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Model Details:**")
                    st.write(f"- Name: {model_info['name']}")
                    st.write(f"- Input Shape: {model_info['input_shape']}")
                    st.write(f"- Classes: {', '.join(model_info['classes'])}")
                
                with col2:
                    st.write("**Technical Specifications:**")
                    st.write("- Architecture: ResNet50 + Custom Head")
                    st.write("- Training: Transfer Learning")
                    st.write("- Preprocessing: CLAHE + Normalization")
            
            # Performance metrics
            if show_performance:
                st.header("📈 Model Performance")
                performance_metrics = model_manager.evaluate_model_performance('chest_xray')
                
                if performance_metrics:
                    visualizer.plot_model_performance(performance_metrics)
                    
                    st.subheader("Performance Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Accuracy", f"{performance_metrics['accuracy']:.1%}")
                    with col2:
                        st.metric("Precision", f"{performance_metrics['precision']:.1%}")
                    with col3:
                        st.metric("Recall", f"{performance_metrics['recall']:.1%}")
                    with col4:
                        st.metric("F1-Score", f"{performance_metrics['f1_score']:.1%}")
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    else:
        # Show example and instructions when no file is uploaded
        show_chest_xray_instructions()

def interpret_chest_xray_results(prediction_result: dict, confidence_threshold: float):
    """Provide clinical interpretation of chest X-ray results"""
    
    predicted_class = prediction_result['predicted_class']
    confidence = prediction_result['confidence']
    predictions = prediction_result['predictions']
    
    # Interpretation based on prediction
    if predicted_class == 'Pneumonia':
        if confidence >= confidence_threshold:
            st.error(f"""
            **HIGH CONFIDENCE PNEUMONIA DETECTION ({confidence:.1%})**
            
            The AI system has detected patterns consistent with pneumonia in this chest X-ray.
            
            **Key Findings:**
            - Consolidation patterns detected
            - Opacity changes in lung fields
            - High confidence in pneumonia classification
            """)
        else:
            st.warning(f"""
            **POSSIBLE PNEUMONIA DETECTED ({confidence:.1%})**
            
            The AI system suggests possible pneumonia, but with moderate confidence.
            Further evaluation is recommended.
            """)
    
    elif predicted_class == 'Normal':
        if confidence >= confidence_threshold:
            st.success(f"""
            **NORMAL CHEST X-RAY ({confidence:.1%})**
            
            The AI system indicates this appears to be a normal chest X-ray.
            
            **Key Findings:**
            - Clear lung fields
            - No obvious consolidation
            - Normal cardiac silhouette appearance
            """)
        else:
            st.info(f"""
            **LIKELY NORMAL ({confidence:.1%})**
            
            The image appears normal, but confidence is moderate.
            Consider clinical correlation.
            """)
    
    # Additional context
    st.info("""
    **Important Notes:**
    - AI predictions should always be correlated with clinical findings
    - Subtle abnormalities may not be detected by AI
    - False positives and negatives are possible
    - Professional radiological interpretation is essential
    """)

def provide_chest_xray_recommendations(prediction_result: dict):
    """Provide recommendations based on chest X-ray analysis"""
    
    predicted_class = prediction_result['predicted_class']
    confidence = prediction_result['confidence']
    
    recommendations = []
    
    if predicted_class == 'Pneumonia':
        recommendations.extend([
            "🚨 **Immediate Actions:**",
            "- Consult with pulmonologist or emergency physician",
            "- Consider additional imaging (CT chest) if indicated",
            "- Evaluate patient's clinical symptoms and vital signs",
            "- Consider laboratory tests (CBC, blood cultures, sputum)",
            "",
            "🔍 **Further Evaluation:**",
            "- Review patient history and risk factors",
            "- Assess for signs of respiratory distress",
            "- Consider antibiotic therapy if clinically indicated",
            "- Monitor oxygen saturation and respiratory status"
        ])
    
    elif predicted_class == 'Normal':
        recommendations.extend([
            "✅ **Normal Findings Noted:**",
            "- Continue routine clinical care as appropriate",
            "- Correlate with patient symptoms and examination",
            "- Consider other causes if respiratory symptoms persist",
            "",
            "📋 **Clinical Correlation:**",
            "- Normal X-ray doesn't rule out all lung pathology",
            "- Some conditions may not be visible on chest X-ray",
            "- Consider CT or other imaging if clinically indicated"
        ])
    
    # Confidence-based recommendations
    if confidence < 0.7:
        recommendations.extend([
            "",
            "⚠️ **Low Confidence Alert:**",
            "- AI prediction has lower confidence",
            "- Consider repeat imaging with better positioning",
            "- Seek expert radiological opinion",
            "- Do not rely solely on AI interpretation"
        ])
    
    # General recommendations
    recommendations.extend([
        "",
        "🔄 **General Recommendations:**",
        "- Always integrate AI results with clinical assessment",
        "- Consider patient's symptoms, history, and examination",
        "- Follow institutional protocols for imaging interpretation",
        "- Document AI assistance in medical records appropriately"
    ])
    
    for recommendation in recommendations:
        if recommendation.startswith(("🚨", "✅", "⚠️", "🔄")):
            st.markdown(f"**{recommendation}**")
        elif recommendation == "":
            st.write("")
        else:
            st.write(recommendation)

def show_chest_xray_instructions():
    """Show instructions and example for chest X-ray analysis"""
    
    st.header("📋 Instructions")
    
    st.markdown("""
    ### How to Use Chest X-Ray Analysis:
    
    1. **Upload Image**: Select a chest X-ray image file (PNG or JPEG)
    2. **Image Requirements**:
       - Clear, properly positioned chest X-ray
       - Minimum size: 100×100 pixels
       - Maximum size: 2000×2000 pixels
       - File size: Under 10MB
    
    3. **Analysis Options**:
       - Adjust confidence threshold for alerts
       - Enable preprocessing visualization
       - View model performance metrics
    
    4. **Review Results**:
       - Check confidence levels
       - Review detailed predictions
       - Follow clinical recommendations
    
    ### Important Considerations:
    
    - **Image Quality**: Ensure X-rays are clear and properly exposed
    - **Positioning**: Standard PA (posterior-anterior) or AP (anterior-posterior) views work best
    - **Clinical Context**: Always correlate AI results with patient symptoms and examination
    - **Limitations**: AI may miss subtle findings or produce false results
    """)
    
    # Technical specifications
    with st.expander("📐 Technical Specifications"):
        st.markdown("""
        **Model Architecture:**
        - Base: ResNet50 pre-trained on ImageNet
        - Custom classification head for medical imaging
        - Input size: 224×224×3 pixels
        - Output: Binary classification (Normal/Pneumonia)
        
        **Preprocessing Pipeline:**
        - Image resizing and normalization
        - Contrast enhancement using CLAHE
        - ImageNet normalization for transfer learning
        
        **Training Data:**
        - Medical imaging datasets
        - Validated by medical professionals
        - Cross-validation for performance assessment
        """)
    
    # Sample workflow
    with st.expander("🔄 Sample Workflow"):
        st.markdown("""
        **Typical Clinical Workflow:**
        
        1. **Image Acquisition**: Obtain chest X-ray following standard protocols
        2. **AI Analysis**: Upload image for AI-assisted interpretation
        3. **Result Review**: Examine AI predictions and confidence scores
        4. **Clinical Correlation**: Integrate with patient history and examination
        5. **Decision Making**: Make clinical decisions based on complete assessment
        6. **Documentation**: Record AI assistance and final interpretation
        7. **Follow-up**: Plan appropriate next steps based on findings
        """)
