# Deployment Guide

## GitHub Repository Setup

### 1. Create GitHub Repository

1. Create a new repository on GitHub
2. Clone to your local machine:
```bash
git clone https://github.com/yourusername/medical-ai-diagnosis.git
cd medical-ai-diagnosis
```

### 2. Upload Project Files

Copy all project files to your repository:
- `app.py` - Main application
- `modules_chest_xray.py` - Chest X-ray module
- `modules_skin_lesion.py` - Skin lesion module  
- `modules_symptom_checker.py` - Symptom checker module
- `models/medical_models.py` - AI models
- `utils/data_preprocessing.py` - Image preprocessing
- `utils/visualization.py` - Visualization functions
- `.streamlit/config.toml` - Streamlit configuration
- `requirements.txt` - Python dependencies
- `packages.txt` - System dependencies
- `README.md` - Documentation

### 3. Commit and Push

```bash
git add .
git commit -m "Initial commit: AI Medical Diagnosis System"
git push origin main
```

## Streamlit Cloud Deployment

### 1. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Configure deployment:
   - **Repository**: your-username/medical-ai-diagnosis
   - **Branch**: main
   - **Main file path**: app.py
5. Click "Deploy"

### 2. Configuration Files

The deployment includes:
- `requirements.txt` - Python package dependencies
- `packages.txt` - System-level dependencies (if needed)
- `.streamlit/config.toml` - Streamlit server configuration

### 3. Environment Variables

No external API keys are required for basic functionality. The system uses:
- TensorFlow for AI models
- PIL for image processing
- Streamlit for web interface

## Local Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/medical-ai-diagnosis.git
cd medical-ai-diagnosis

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py --server.port 5000
```

### Development Server

The application will be available at:
- Local: http://localhost:5000
- Network: http://0.0.0.0:5000

## File Structure

```
medical-ai-diagnosis/
├── app.py                      # Main Streamlit application
├── modules_chest_xray.py       # Chest X-ray analysis
├── modules_skin_lesion.py      # Skin lesion detection
├── modules_symptom_checker.py  # Symptom checker
├── models/
│   └── medical_models.py       # AI model definitions
├── utils/
│   ├── data_preprocessing.py   # Image preprocessing
│   └── visualization.py       # Visualization functions
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── requirements.txt           # Python dependencies
├── packages.txt              # System dependencies
├── README.md                 # Project documentation
└── DEPLOYMENT.md             # This deployment guide
```

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   - Ensure all files are in correct directories
   - Check Python path and imports

2. **Package Installation Issues**
   - Verify requirements.txt contains all dependencies
   - Use compatible package versions

3. **Streamlit Configuration**
   - Check .streamlit/config.toml settings
   - Ensure port configuration is correct

### Performance Optimization

- Use caching for model loading
- Optimize image preprocessing
- Configure appropriate server settings

## Security Considerations

- No sensitive data is stored in the application
- All processing happens locally or on Streamlit Cloud
- Medical disclaimers are prominently displayed
- Educational use only warnings are included

## Support

For deployment issues:
1. Check Streamlit Cloud logs
2. Verify all files are committed to repository
3. Review configuration files
4. Check GitHub repository permissions