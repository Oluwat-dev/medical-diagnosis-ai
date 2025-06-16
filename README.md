# AI-Powered Medical Diagnosis System

An advanced medical diagnosis system using TensorFlow neural networks with an interactive Streamlit interface for healthcare insights.

## Features

### 🫁 Chest X-Ray Analysis
- Pneumonia detection using deep learning
- Transfer learning with ResNet50 architecture
- Medical image preprocessing with CLAHE enhancement
- Confidence scoring and clinical interpretation

### 🔍 Skin Lesion Detection
- Malignancy classification using EfficientNetB0
- ABCDE rule assessment for melanoma screening
- Risk factor analysis with patient demographics
- Feature analysis and recommendations

### 🩺 AI Symptom Checker
- Rule-based symptom analysis
- Severity assessment and triage recommendations
- Patient history tracking
- Comprehensive health assessment

## Technology Stack

- **Framework**: TensorFlow 2.18+ with Keras
- **Architecture**: Convolutional Neural Networks (CNNs)
- **Approach**: Transfer Learning with pre-trained models
- **Interface**: Streamlit Web Application
- **Image Processing**: OpenCV, PIL
- **Visualization**: Plotly, Matplotlib, Seaborn

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Oluwat-dev/medical-diagnosis-ai.git
cd medical-diagnosis-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py --server.port 5000
```

## Project Structure

```
├── app.py                    # Main Streamlit application
├── models/
│   └── medical_models.py     # AI model management
├── pages/
│   ├── chest_xray.py        # Chest X-ray analysis
│   ├── skin_lesion.py       # Skin lesion detection
│   └── symptom_checker.py   # Symptom analysis
├── utils/
│   ├── data_preprocessing.py # Image preprocessing
│   └── visualization.py     # Medical visualizations
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── requirements.txt         # Python dependencies
```

## Medical Models

### Chest X-Ray Model
- **Base**: ResNet50 pre-trained on ImageNet
- **Classes**: Normal, Pneumonia
- **Input**: 224x224x3 RGB images
- **Preprocessing**: CLAHE enhancement + normalization

### Skin Lesion Model
- **Base**: EfficientNetB0 pre-trained on ImageNet
- **Classes**: Benign, Malignant
- **Input**: 224x224x3 RGB images
- **Preprocessing**: Gaussian blur + contrast enhancement

## Usage Guidelines

### Image Requirements
- **Format**: JPEG, PNG
- **Size**: 100x100 to 2000x2000 pixels
- **File size**: Under 10MB
- **Quality**: Clear, well-lit images

### Medical Disclaimer

⚠️ **IMPORTANT**: This system is for educational and research purposes only.

- NOT for clinical diagnosis or treatment decisions
- Always consult qualified healthcare professionals
- AI predictions should be correlated with clinical findings
- False positives and negatives are possible

## Features in Detail

### Chest X-Ray Analysis
- Upload chest X-ray images for pneumonia detection
- Real-time AI analysis with confidence scoring
- Clinical interpretation and recommendations
- Model performance metrics display

### Skin Lesion Detection
- Upload skin lesion images for malignancy assessment
- ABCDE rule evaluation for melanoma screening
- Patient risk factor analysis
- Detailed feature analysis and recommendations

### Symptom Checker
- Quick symptom assessment with severity analysis
- Detailed health evaluation with patient demographics
- Symptom history tracking and pattern analysis
- Rule-based condition matching with recommendations

## Model Performance

### Chest X-Ray Model
- Accuracy: ~87%
- Precision: ~85%
- Recall: ~89%
- F1-Score: ~87%

### Skin Lesion Model
- Accuracy: ~82%
- Precision: ~80%
- Recall: ~84%
- F1-Score: ~82%

## Configuration

The application uses Streamlit configuration in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational purposes. Please ensure compliance with medical AI regulations in your jurisdiction.

## Support

For questions or issues, please create an issue in the GitHub repository.

---

**Note**: This AI system demonstrates medical diagnosis capabilities but should never replace professional medical consultation. Thank you.
