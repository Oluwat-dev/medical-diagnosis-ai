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

---

## Local Installation

### Requirements

- **Python 3.9, 3.10, or 3.11** (Python 3.12+ is NOT supported by TensorFlow)
- pip package manager

> Download Python from: https://www.python.org/downloads/

---

### Option 1: Automatic Setup (Recommended)

**Mac / Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```
Double-click setup.bat
```

These scripts will automatically detect your platform, create a virtual environment, and install all dependencies correctly.

---

### Option 2: Manual Setup

#### Step 1 — Create a virtual environment

**Mac / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### Step 2 — Install dependencies

**Windows / Linux / Intel Mac:**
```bash
pip install -r requirements-github.txt
```

**Apple Silicon Mac (M1 / M2 / M3):**
```bash
pip install tensorflow-macos tensorflow-metal
pip install streamlit "pillow>=10.0.0" "numpy>=1.23.5,<2.0.0" "matplotlib>=3.7.0" seaborn plotly pandas scikit-learn "opencv-python>=4.8.0"
```

#### Step 3 — Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `tensorflow` install fails | Make sure you're using Python 3.9–3.11 |
| Apple Silicon errors | Use `tensorflow-macos` instead of `tensorflow` |
| `opencv` errors on Linux | Run `sudo apt-get install libgl1-mesa-glx libglib2.0-0` |
| `ModuleNotFoundError` | Make sure your virtual environment is activated |

---

## Usage

1. **Home Dashboard** — Overview of all diagnostic modules
2. **Chest X-Ray Analysis** — Upload chest X-ray images for pneumonia detection
3. **Skin Lesion Detection** — Analyze skin lesions for potential malignancy
4. **Symptom Checker** — AI-powered symptom analysis and health assessment

---

## File Structure

```
medical-ai-diagnosis/
├── app.py                       # Main Streamlit application
├── modules_chest_xray.py        # Chest X-ray analysis module
├── modules_skin_lesion.py       # Skin lesion detection module
├── modules_symptom_checker.py   # Symptom checker module
├── models/
│   └── medical_models.py        # AI model definitions
├── utils/
│   ├── data_preprocessing.py    # Image preprocessing utilities
│   └── visualization.py        # Visualization functions
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── requirements-github.txt      # Python dependencies (use this one locally)
├── setup.sh                     # Auto-setup script for Mac/Linux
├── setup.bat                    # Auto-setup script for Windows
└── README.md                    # This file
```

---

## Deployment (Streamlit Cloud)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the main file to `app.py`
5. Deploy with one click

---

## Medical Disclaimer

**IMPORTANT**: This system is for educational and research purposes only. It should NOT be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.

---

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: TensorFlow, Keras, scikit-learn
- **Image Processing**: OpenCV, PIL, NumPy
- **Visualization**: Matplotlib, Plotly, Seaborn
- **Data Processing**: Pandas

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
