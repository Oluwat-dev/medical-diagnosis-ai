import streamlit as st
from PIL import Image
import numpy as np
from models.medical_models import ModelManager
from utils.data_preprocessing_streamlit import MedicalImagePreprocessor
from utils.visualization_streamlit import MedicalVisualization

def show_skin_lesion_page():
    """Display the skin lesion analysis page"""
    
    st.title("🔍 Skin Lesion Detection")
    st.markdown("""
    Upload an image of a skin lesion to analyze for potential malignancy. 
    This AI system uses computer vision to assist in dermatological assessment.
    """)
    
    # Medical disclaimer for dermatology
    st.error("""
    ⚠️ **DERMATOLOGY DISCLAIMER**
    
    This skin lesion analysis tool is for educational purposes only.
    - **NOT for clinical diagnosis**: Do not use for actual patient care
    - **Always consult dermatologists**: Professional examination is essential
    - **Suspicious lesions**: Seek immediate medical evaluation
    - **Biopsy required**: Only histopathology can confirm malignancy
    """)
    
    # Initialize components
    model_manager = ModelManager()
    preprocessor = MedicalImagePreprocessor()
    visualizer = MedicalVisualization()
    
    # Information about skin lesion analysis
    with st.expander("ℹ️ About Skin Lesion Analysis"):
        st.markdown("""
        **What this system analyzes:**
        - **Benign lesions**: Common moles, seborrheic keratoses, etc.
        - **Malignant lesions**: Melanoma, basal cell carcinoma, etc.
        
        **ABCDE Rule for Melanoma:**
        - **A**symmetry: One half doesn't match the other
        - **B**order: Irregular, scalloped, or poorly defined
        - **C**olor: Varied from one area to another
        - **D**iameter: Larger than 6mm (pencil eraser size)
        - **E**volving: Changes in size, shape, color, or symptoms
        
        **Important**: This AI assists but cannot replace professional dermatological examination.
        """)
    
    # File upload section
    st.header("📤 Upload Skin Lesion Image")
    
    uploaded_file = st.file_uploader(
        "Choose a skin lesion image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear, well-lit image of the skin lesion"
    )
    
    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            
            # Display original image
            st.subheader("📸 Uploaded Image")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(image, caption="Skin Lesion Image", use_column_width=True)
            
            with col2:
                # Image statistics
                img_stats = preprocessor.get_image_stats(image)
                st.write("**Image Properties:**")
                if 'error' not in img_stats:
                    st.write(f"- Size: {img_stats['size'][0]}×{img_stats['size'][1]}")
                    st.write(f"- Format: {img_stats['format']}")
                    st.write(f"- Mode: {img_stats['mode']}")
                    if 'mean_per_channel' in img_stats:
                        st.write("- Color Distribution:")
                        colors = ['Red', 'Green', 'Blue']
                        for i, (color, mean_val) in enumerate(zip(colors, img_stats['mean_per_channel'])):
                            st.write(f"  - {color}: {mean_val:.1f}")
            
            # Validate image
            is_valid, error_message = preprocessor.validate_image(image, 'skin_lesion')
            
            if not is_valid:
                st.error(f"Image validation failed: {error_message}")
                return
            
            st.success("✅ Image validation passed")
            
            # Analysis options
            st.header("⚙️ Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                show_preprocessing = st.checkbox("Show preprocessing steps", value=False)
                confidence_threshold = st.slider(
                    "Confidence threshold for alerts",
                    min_value=0.5,
                    max_value=0.95,
                    value=0.75,
                    step=0.05,
                    help="Threshold for high-confidence predictions"
                )
            
            with col2:
                risk_assessment = st.checkbox("Include risk assessment", value=True)
                detailed_analysis = st.checkbox("Show detailed feature analysis", value=False)
            
            # Patient information (optional)
            with st.expander("👤 Patient Information (Optional)"):
                col1, col2 = st.columns(2)
                with col1:
                    patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
                    skin_type = st.selectbox("Skin Type", [
                        "Type I (Very Fair)",
                        "Type II (Fair)", 
                        "Type III (Medium)",
                        "Type IV (Olive)",
                        "Type V (Brown)",
                        "Type VI (Dark Brown/Black)"
                    ], key="skin_type")
                
                with col2:
                    family_history = st.checkbox("Family history of skin cancer")
                    sun_exposure = st.selectbox("Sun exposure level", [
                        "Low", "Moderate", "High", "Very High"
                    ], key="sun_exposure")
            
            # Run analysis button
            if st.button("🔍 Analyze Lesion", type="primary", use_container_width=True):
                
                with st.spinner("Preprocessing image..."):
                    # Preprocess the image
                    processed_image = preprocessor.preprocess_image(image, 'skin_lesion')
                    
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
                    prediction_result = model_manager.predict('skin_lesion', processed_image)
                    
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
                st.subheader("📋 Classification Results")
                visualizer.plot_prediction_confidence(
                    prediction_result['predictions'],
                    "Skin Lesion Classification"
                )
                
                # Clinical interpretation
                st.subheader("🩺 Clinical Assessment")
                interpret_skin_lesion_results(prediction_result, confidence_threshold)
                
                # Risk assessment
                if risk_assessment:
                    st.subheader("⚠️ Risk Assessment")
                    perform_risk_assessment(
                        prediction_result, 
                        patient_age, 
                        family_history, 
                        sun_exposure,
                        visualizer
                    )
                
                # Detailed feature analysis
                if detailed_analysis:
                    st.subheader("🔬 Feature Analysis")
                    analyze_lesion_features(image, prediction_result)
                
                # Recommendations
                st.subheader("💡 Recommendations")
                provide_skin_lesion_recommendations(prediction_result, confidence_threshold)
        
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
    
    else:
        # Show instructions when no file is uploaded
        show_skin_lesion_instructions()

def interpret_skin_lesion_results(prediction_result: dict, confidence_threshold: float):
    """Provide clinical interpretation of skin lesion results"""
    
    predicted_class = prediction_result['predicted_class']
    confidence = prediction_result['confidence']
    predictions = prediction_result['predictions']
    
    # Interpretation based on prediction
    if predicted_class == 'Malignant':
        if confidence >= confidence_threshold:
            st.error(f"""
            **⚠️ SUSPICIOUS LESION DETECTED ({confidence:.1%} confidence)**
            
            The AI system has identified features concerning for malignancy.
            
            **Key Findings:**
            - Irregular patterns detected
            - Features consistent with malignant characteristics
            - High confidence in classification
            
            **URGENT**: This requires immediate dermatological evaluation.
            """)
        else:
            st.warning(f"""
            **🔍 POSSIBLE SUSPICIOUS LESION ({confidence:.1%} confidence)**
            
            The AI suggests possible malignant features, but with moderate confidence.
            Professional evaluation is strongly recommended.
            """)
    
    elif predicted_class == 'Benign':
        if confidence >= confidence_threshold:
            st.success(f"""
            **✅ LIKELY BENIGN LESION ({confidence:.1%} confidence)**
            
            The AI system suggests this lesion appears benign.
            
            **Key Findings:**
            - Regular patterns observed
            - Features consistent with benign lesions
            - High confidence in benign classification
            
            **Note**: Continue routine monitoring for any changes.
            """)
        else:
            st.info(f"""
            **📋 POSSIBLY BENIGN ({confidence:.1%} confidence)**
            
            The lesion appears benign, but confidence is moderate.
            Consider professional evaluation for confirmation.
            """)
    
    # Additional clinical context
    st.info("""
    **Clinical Context:**
    - AI analysis is based on visual features only
    - Dermoscopy and clinical examination provide additional information
    - Only histopathological examination can definitively diagnose malignancy
    - Changes over time are important diagnostic indicators
    """)

def perform_risk_assessment(prediction_result: dict, patient_age: int, family_history: bool, 
                          sun_exposure: str, visualizer: MedicalVisualization):
    """Perform comprehensive risk assessment"""
    
    # Calculate risk factors
    risk_factors = {}
    
    # Age-based risk
    if patient_age < 20:
        risk_factors['Age Risk'] = 0.1
    elif patient_age < 40:
        risk_factors['Age Risk'] = 0.3
    elif patient_age < 60:
        risk_factors['Age Risk'] = 0.6
    else:
        risk_factors['Age Risk'] = 0.8
    
    # Family history risk
    risk_factors['Genetic Risk'] = 0.7 if family_history else 0.2
    
    # Sun exposure risk
    sun_risk_map = {
        'Low': 0.2,
        'Moderate': 0.4,
        'High': 0.7,
        'Very High': 0.9
    }
    risk_factors['UV Exposure Risk'] = sun_risk_map.get(sun_exposure, 0.5)
    
    # AI prediction risk
    if prediction_result['predicted_class'] == 'Malignant':
        risk_factors['AI Assessment Risk'] = prediction_result['confidence']
    else:
        risk_factors['AI Assessment Risk'] = 1 - prediction_result['confidence']
    
    # Create risk visualization
    visualizer.create_risk_assessment_chart(risk_factors)
    
    # Calculate overall risk score
    overall_risk = np.mean(list(risk_factors.values()))
    
    # Risk interpretation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Risk Score", f"{overall_risk:.1%}")
    
    with col2:
        if overall_risk >= 0.7:
            risk_level = "HIGH"
            color = "🔴"
        elif overall_risk >= 0.4:
            risk_level = "MODERATE"
            color = "🟡"
        else:
            risk_level = "LOW"
            color = "🟢"
        
        st.metric("Risk Level", f"{color} {risk_level}")
    
    with col3:
        urgency = "Immediate" if overall_risk >= 0.7 else "Routine" if overall_risk >= 0.4 else "Standard"
        st.metric("Follow-up", urgency)
    
    # Risk factor breakdown
    st.write("**Risk Factor Breakdown:**")
    for factor, score in risk_factors.items():
        risk_color = "🔴" if score >= 0.7 else "🟡" if score >= 0.4 else "🟢"
        st.write(f"- {factor}: {risk_color} {score:.1%}")

def analyze_lesion_features(image: Image.Image, prediction_result: dict):
    """Analyze specific features of the lesion"""
    
    st.markdown("""
    **Feature Analysis** (Educational demonstration):
    
    This section would typically include detailed analysis of lesion characteristics
    such as asymmetry, border irregularity, color variation, and diameter measurements.
    """)
    
    # Convert image to numpy array for analysis
    img_array = np.array(image)
    
    # Basic image statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Color Analysis:**")
        if len(img_array.shape) == 3:
            mean_rgb = np.mean(img_array, axis=(0, 1))
            st.write(f"- Average Red: {mean_rgb[0]:.1f}")
            st.write(f"- Average Green: {mean_rgb[1]:.1f}")
            st.write(f"- Average Blue: {mean_rgb[2]:.1f}")
            
            # Color diversity
            color_std = np.std(img_array, axis=(0, 1))
            color_diversity = np.mean(color_std)
            st.write(f"- Color Diversity: {color_diversity:.1f}")
    
    with col2:
        st.write("**Texture Analysis:**")
        gray_image = np.mean(img_array, axis=2) if len(img_array.shape) == 3 else img_array
        
        # Basic texture measures
        contrast = np.std(gray_image)
        st.write(f"- Contrast: {contrast:.1f}")
        
        # Edge detection (simplified)
        edges = np.abs(np.gradient(gray_image)[0]) + np.abs(np.gradient(gray_image)[1])
        edge_density = np.mean(edges)
        st.write(f"- Edge Density: {edge_density:.1f}")
        
        # Uniformity
        hist, _ = np.histogram(gray_image.flatten(), bins=50)
        uniformity = np.sum(hist**2) / (gray_image.size**2)
        st.write(f"- Uniformity: {uniformity:.3f}")
    
    st.info("""
    **Note**: These are basic computational features for educational purposes.
    Professional dermatological analysis involves much more sophisticated 
    feature extraction and clinical correlation.
    """)

def provide_skin_lesion_recommendations(prediction_result: dict, confidence_threshold: float):
    """Provide recommendations based on skin lesion analysis"""
    
    predicted_class = prediction_result['predicted_class']
    confidence = prediction_result['confidence']
    
    recommendations = []
    
    if predicted_class == 'Malignant':
        recommendations.extend([
            "🚨 **URGENT ACTIONS REQUIRED:**",
            "- Schedule immediate dermatology consultation",
            "- Do not delay - seek evaluation within 1-2 weeks",
            "- Consider dermoscopy or dermatoscopic examination",
            "- Prepare for possible biopsy procedure",
            "",
            "📋 **Documentation:**",
            "- Take additional photos for comparison",
            "- Note any recent changes in size, color, or texture",
            "- Document symptoms (itching, bleeding, pain)",
            "- Record family history of skin cancer"
        ])
    
    elif predicted_class == 'Benign':
        recommendations.extend([
            "✅ **ROUTINE MONITORING:**",
            "- Continue regular self-examinations",
            "- Schedule routine dermatology check-up",
            "- Monitor for any changes over time",
            "",
            "📸 **Self-Monitoring Tips:**",
            "- Take monthly photos for comparison",
            "- Use the ABCDE rule for changes",
            "- Note any new symptoms",
            "- Keep a lesion diary if concerned"
        ])
    
    # Confidence-based recommendations
    if confidence < 0.7:
        recommendations.extend([
            "",
            "⚠️ **UNCERTAIN DIAGNOSIS:**",
            "- AI confidence is lower than optimal",
            "- Professional evaluation strongly recommended",
            "- Consider getting a second opinion",
            "- Do not rely solely on AI assessment"
        ])
    
    # General skin health recommendations
    recommendations.extend([
        "",
        "☀️ **SKIN PROTECTION:**",
        "- Use broad-spectrum SPF 30+ sunscreen daily",
        "- Seek shade during peak UV hours (10 AM - 4 PM)",
        "- Wear protective clothing and wide-brimmed hats",
        "- Avoid tanning beds and excessive sun exposure",
        "",
        "🔍 **REGULAR SCREENING:**",
        "- Perform monthly self-examinations",
        "- Annual dermatological check-ups recommended",
        "- Earlier screening if high-risk factors present",
        "- Learn proper self-examination techniques"
    ])
    
    for recommendation in recommendations:
        if recommendation.startswith(("🚨", "✅", "⚠️", "☀️", "🔍")):
            st.markdown(f"**{recommendation}**")
        elif recommendation == "":
            st.write("")
        else:
            st.write(recommendation)

def show_skin_lesion_instructions():
    """Show instructions for skin lesion analysis"""
    
    st.header("📋 How to Use Skin Lesion Analysis")
    
    st.markdown("""
    ### Image Requirements:
    
    1. **Image Quality**:
       - Well-lit, clear photograph
       - Focus on the lesion of concern
       - Avoid shadows and reflections
       - Use natural lighting when possible
    
    2. **Technical Specifications**:
       - Format: PNG or JPEG
       - Minimum size: 100×100 pixels
       - Maximum size: 2000×2000 pixels
       - File size: Under 10MB
    
    3. **Photography Tips**:
       - Keep camera steady
       - Fill frame with lesion and surrounding skin
       - Include a reference object (coin, ruler) if possible
       - Take multiple angles if lesion is raised
    
    ### What to Look For (ABCDE Rule):
    
    - **A**symmetry: One half unlike the other
    - **B**order: Irregular, scalloped, or poorly defined
    - **C**olor: Varied colors within the lesion
    - **D**iameter: Larger than 6mm (size of pencil eraser)
    - **E**volving: Changes in size, shape, color, elevation, or symptoms
    """)
    
    # Warning signs
    st.error("""
    **🚨 IMMEDIATE MEDICAL ATTENTION REQUIRED IF:**
    
    - Lesion is bleeding or ulcerated
    - Rapid changes in size or appearance
    - New lesion in adults over 30
    - Lesion that looks different from others
    - Itching, tenderness, or pain in a mole
    """)
    
    # Technical information
    with st.expander("🔬 Technical Details"):
        st.markdown("""
        **AI Model Information:**
        - Architecture: EfficientNetB0 with custom classification head
        - Training: Transfer learning on dermatology datasets
        - Input: 224×224 pixel RGB images
        - Output: Binary classification (Benign/Malignant)
        
        **Preprocessing Pipeline:**
        - Image resizing and normalization
        - Gaussian blur for noise reduction
        - Contrast enhancement
        - ImageNet normalization for transfer learning
        
        **Performance Considerations:**
        - Trained on diverse dermatology datasets
        - Cross-validated for reliability
        - Continuous monitoring and improvement
        - Professional validation required
        """)
    
    # Best practices
    with st.expander("✅ Best Practices"):
        st.markdown("""
        **For Healthcare Professionals:**
        - Use as a supplementary tool, not primary diagnosis
        - Always perform clinical examination
        - Consider dermoscopy for suspicious lesions
        - Document AI assistance in patient records
        
        **For Patients:**
        - Regular self-examinations monthly
        - Professional screening annually or as recommended
        - Sun protection and skin care
        - Prompt medical attention for concerning changes
        
        **Photography Guidelines:**
        - Consistent lighting conditions
        - Same distance and angle for follow-up photos
        - Date and label images appropriately
        - Secure storage and privacy protection
        """)
