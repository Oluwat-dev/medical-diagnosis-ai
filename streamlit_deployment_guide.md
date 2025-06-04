# Deploy AI Medical Diagnosis System on Streamlit Cloud

## Quick Deployment Steps

### 1. Create GitHub Repository
1. Go to GitHub.com and create a new repository
2. Name it: `ai-medical-diagnosis`
3. Make it public
4. Don't initialize with README

### 2. Upload Your Code
Upload all these files to your GitHub repository:
- `app.py` (main application)
- `requirements-github.txt` (dependencies)
- `.streamlit/config.toml` (configuration)
- All folders: `models/`, `pages/`, `utils/`
- Documentation: `README.md`, `LICENSE`

### 3. Deploy on Streamlit Cloud
1. Go to **share.streamlit.io**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Configure:
   - Repository: `your-username/ai-medical-diagnosis`
   - Branch: `main`
   - Main file path: `app.py`
   - Advanced: Use `requirements-github.txt`

### 4. Launch
- Click **"Deploy!"**
- Wait 3-5 minutes for build
- Your app will be live at: `https://your-app-name.streamlit.app`

## What Will Be Deployed

Your live medical diagnosis system will include:
- Chest X-Ray pneumonia detection
- Skin lesion malignancy classification
- AI symptom checker with risk assessment
- Professional medical disclaimers
- Responsive navigation interface

## Requirements File Content
The `requirements-github.txt` contains:
```
tensorflow>=2.15.0
streamlit>=1.28.0
pillow>=10.0.0
numpy>=1.23.5,<2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.0.0
pandas>=2.0.0
scikit-learn>=1.3.0
```

## Configuration File
The `.streamlit/config.toml` contains:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

Your app is cloud-compatible with no OpenCV dependencies and proper matplotlib backend configuration.