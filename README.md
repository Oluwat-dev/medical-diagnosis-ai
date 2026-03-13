# AI Medical Diagnosis System

An advanced AI-powered medical diagnosis system leveraging cutting-edge machine learning technologies to provide comprehensive healthcare insights through an intuitive and user-friendly interface.

## Features

- **Multi-modal Diagnostic Modules**
  - Chest X-Ray Analysis (Pneumonia Detection)
  - Skin Lesion Detection (Melanoma Classification)
  - AI Symptom Checker (Health Assessment)

- **Advanced AI Models**
  - TensorFlow neural networks
  - Transfer learning with pre-trained models
  - Real-time image analysis

- **User-Friendly Interface**
  - Streamlit web application
  - Responsive design
  - Interactive visualizations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medical-ai-diagnosis.git
cd medical-ai-diagnosis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py --server.port 5000
```

## Usage

1. **Home Dashboard**: Overview of all diagnostic modules
2. **Chest X-Ray Analysis**: Upload chest X-ray images for pneumonia detection
3. **Skin Lesion Detection**: Analyze skin lesions for potential malignancy
4. **Symptom Checker**: AI-powered symptom analysis and health assessment

## File Structure

```
medical-ai-diagnosis/
├── app.py                      # Main Streamlit application
├── modules_chest_xray.py       # Chest X-ray analysis module
├── modules_skin_lesion.py      # Skin lesion detection module
├── modules_symptom_checker.py  # Symptom checker module
├── models/
│   └── medical_models.py       # AI model definitions
├── utils/
│   ├── data_preprocessing.py   # Image preprocessing utilities
│   └── visualization.py       # Visualization functions
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── requirements.txt           # Python dependencies
├── packages.txt              # System dependencies for deployment
└── README.md                 # This file
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

### Local Development

```bash
streamlit run app.py --server.port 5000
```

## Medical Disclaimer

⚠️ **IMPORTANT**: This system is for educational and research purposes only. It should NOT be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: TensorFlow, Keras
- **Image Processing**: PIL, NumPy
- **Visualization**: Matplotlib, Plotly, Seaborn
- **Data Processing**: Pandas

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on GitHub.