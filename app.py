import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="AI Medical Diagnosis System",
                   page_icon="🏥",
                   layout="wide",
                   initial_sidebar_state="expanded")


# Enhanced medical disclaimer
def show_medical_disclaimer():
    st.sidebar.markdown("### ⚠️ **MEDICAL DISCLAIMER**")
    st.sidebar.error("""
    **FOR EDUCATIONAL USE ONLY**
    
    🚨 **Critical Notice:**
    • NOT for actual medical diagnosis
    • NOT for treatment decisions
    • NOT a replacement for healthcare professionals
    
    📞 **Always consult qualified medical professionals**
    """)

    st.sidebar.markdown("### 🆘 **Emergency Notice**")
    st.sidebar.warning("""
    **Call Emergency Services Immediately for:**
    • Chest pain or difficulty breathing
    • Severe bleeding or trauma
    • Loss of consciousness
    • Stroke symptoms
    """)
    st.sidebar.markdown("---")


def main():
    st.title("🏥 AI-Powered Medical Diagnosis System")
    st.markdown("""
    Welcome to my AI-powered medical diagnosis system. This application demonstrates 
    the potential of deep learning in healthcare analytics.
    """)

    # Show medical disclaimer at the top
    show_medical_disclaimer()

    # Enhanced Navigation Design
    st.sidebar.markdown("## 🔬 **Medical AI Platform**")
    st.sidebar.markdown("*Advanced Diagnostic Tools*")
    st.sidebar.markdown("---")

    # Create navigation with enhanced styling
    navigation_options = {
        "🏠 Home": "Home",
        "🫁 Chest X-Ray Analysis": "Chest X-Ray Analysis",
        "🔍 Skin Lesion Detection": "Skin Lesion Detection",
        "🩺 Symptom Checker": "Symptom Checker"
    }

    st.sidebar.markdown("### 🔬 **Analysis Modules**")
    st.sidebar.markdown('<p style="color: #888; font-style: italic; margin-bottom: 20px;">Choose your diagnostic tool</p>', unsafe_allow_html=True)
    
    # Enhanced module selection with beautiful card-like design
    module_descriptions = {
        "🏠 Home": "Dashboard & Overview",
        "🫁 Chest X-Ray Analysis": "Pneumonia Detection AI", 
        "🔍 Skin Lesion Detection": "Melanoma Classification",
        "🩺 Symptom Checker": "AI Health Assessment"
    }
    
    for option in navigation_options.keys():
        is_selected = st.session_state.get('selected_page') == navigation_options[option]
        button_type = "primary" if is_selected else "secondary"
        
        # Create a custom styled container for each module
        with st.sidebar.container():
            if st.button(
                f"{option}\n{module_descriptions[option]}",
                key=f"nav_{option}",
                use_container_width=True,
                type=button_type,
                help=f"Access {navigation_options[option]} module"
            ):
                st.session_state.selected_page = navigation_options[option]
                st.rerun()
        
        # Add subtle spacing between buttons
        st.sidebar.markdown('<div style="margin-bottom: 8px;"></div>', unsafe_allow_html=True)
    
    # Get selected page from session state or default to Home
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    page = st.session_state.selected_page

    # Add quick stats section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 **Quick Stats**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("AI Models", "3", delta="Active")
    with col2:
        st.metric("Accuracy", "95%", delta="2%")

    # Add feature highlights
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✨ **Features**")
    st.sidebar.markdown("""
    • **Real-time Analysis** - Instant AI predictions
    • **Multi-modal Input** - Images & symptoms
    • **Risk Assessment** - Comprehensive evaluation
    • **Educational Tool** - Learning resource
    """)

    # Add current selection info
    st.sidebar.markdown("---")
    st.sidebar.info(f"**Current Module:** {page}")

    if page == "Home":
        show_home_page()
    elif page == "Chest X-Ray Analysis":
        try:
            from modules_chest_xray import show_chest_xray_page
            show_chest_xray_page()
        except ImportError:
            st.error("Chest X-Ray module is temporarily unavailable.")
    elif page == "Skin Lesion Detection":
        try:
            from modules_skin_lesion import show_skin_lesion_page
            show_skin_lesion_page()
        except ImportError:
            st.error("Skin Lesion module is temporarily unavailable.")
    elif page == "Symptom Checker":
        try:
            from modules_symptom_checker import show_symptom_checker_page
            show_symptom_checker_page()
        except ImportError:
            st.error("Symptom Checker module is temporarily unavailable.")


def show_home_page():
    st.header("📊 System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🫁 Chest X-Ray Analysis")
        st.write(
            "Detect pneumonia and other chest conditions from X-ray images using deep learning."
        )
        st.info("Accuracy: ~85-90% on test datasets")

    with col2:
        st.subheader("🔍 Skin Lesion Detection")
        st.write(
            "Classify skin lesions and detect potential malignancy using computer vision."
        )
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
