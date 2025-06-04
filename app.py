import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# Page configuration
st.set_page_config(
    page_title="AI Medical Diagnosis System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Medical disclaimer
def show_medical_disclaimer():
    st.sidebar.markdown("---")
    st.sidebar.warning("""
    ⚠️ **MEDICAL DISCLAIMER**
    
    This AI system is for educational and demonstration purposes only. 
    It should NOT be used for actual medical diagnosis or treatment decisions.
    
    Always consult qualified healthcare professionals for medical advice.
    """)

def main():
    st.title("🏥 AI-Powered Medical Diagnosis System")
    st.markdown("""
    Welcome to our AI-powered medical diagnosis system. This application demonstrates 
    the potential of deep learning in healthcare analytics.
    """)
    
    # Show medical disclaimer
    show_medical_disclaimer()
    
    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose Analysis Type",
        ["Home", "Chest X-Ray Analysis", "Skin Lesion Detection", "Symptom Checker"],
        key="main_navigation"
    )
    
    if page == "Home":
        show_home_page()
    elif page == "Chest X-Ray Analysis":
        from pages.chest_xray import show_chest_xray_page
        show_chest_xray_page()
    elif page == "Skin Lesion Detection":
        from pages.skin_lesion import show_skin_lesion_page
        show_skin_lesion_page()
    elif page == "Symptom Checker":
        from pages.symptom_checker import show_symptom_checker_page
        show_symptom_checker_page()

def show_home_page():
    st.header("📊 System Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🫁 Chest X-Ray Analysis")
        st.write("Detect pneumonia and other chest conditions from X-ray images using deep learning.")
        st.info("Accuracy: ~85-90% on test datasets")
    
    with col2:
        st.subheader("🔍 Skin Lesion Detection")
        st.write("Classify skin lesions and detect potential malignancy using computer vision.")
        st.info("Trained on dermatology datasets")
    
    with col3:
        st.subheader("🩺 Symptom Checker")
        st.write("Analyze symptoms and provide preliminary health insights.")
        st.info("Rule-based + ML hybrid approach")
    
    st.markdown("---")
    
    # Model information
    st.header("🧠 Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Technology Stack")
        st.markdown("""
        - **Framework**: TensorFlow/Keras
        - **Architecture**: Convolutional Neural Networks (CNNs)
        - **Approach**: Transfer Learning with pre-trained models
        - **Interface**: Streamlit Web Application
        """)
    
    with col2:
        st.subheader("Model Performance")
        st.markdown("""
        - **Training Data**: Medical imaging datasets
        - **Validation**: Cross-validation and holdout testing
        - **Metrics**: Accuracy, Precision, Recall, F1-Score
        - **Confidence Scoring**: Probabilistic outputs
        """)
    
    # Important notes
    st.markdown("---")
    st.header("⚠️ Important Notes")
    st.error("""
    **CRITICAL DISCLAIMER**: This system is designed for educational and research purposes only.
    
    - **NOT for clinical use**: Do not use for actual medical diagnosis
    - **Limitations**: AI models can make errors and have biases
    - **Always consult professionals**: Seek qualified medical advice
    - **Data privacy**: Do not upload real patient data without proper authorization
    """)
    
    # System status
    st.markdown("---")
    st.header("🔧 System Status")
    
    try:
        # Check TensorFlow availability
        tf_version = tf.__version__
        st.success(f"✅ TensorFlow {tf_version} loaded successfully")
        
        # Check model availability
        from models.medical_models import ModelManager
        model_manager = ModelManager()
        st.success("✅ Model management system initialized")
        
    except Exception as e:
        st.error(f"❌ System initialization error: {str(e)}")

if __name__ == "__main__":
    main()
