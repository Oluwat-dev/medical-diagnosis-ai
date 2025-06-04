# Deployment Guide

## GitHub Deployment

### Prerequisites
- GitHub account
- Git installed locally
- Python 3.11+ environment

### Steps to Deploy

1. **Create a new repository on GitHub**
   - Go to github.com and create a new repository
   - Name it: `medical-diagnosis-ai`
   - Make it public or private as preferred
   - Don't initialize with README (we already have one)

2. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: AI Medical Diagnosis System"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/medical-diagnosis-ai.git
   git push -u origin main
   ```

3. **Set up for collaboration**
   - Add collaborators in repository settings
   - Set up branch protection rules
   - Configure issue templates

## Streamlit Cloud Deployment

### Option 1: Streamlit Community Cloud (Recommended)

1. **Connect to GitHub**
   - Go to share.streamlit.io
   - Sign in with GitHub
   - Click "New app"

2. **Configure deployment**
   - Repository: `YOUR_USERNAME/medical-diagnosis-ai`
   - Branch: `main`
   - Main file path: `app.py`

3. **Advanced settings**
   - Python version: 3.11
   - Requirements file: `requirements-github.txt`

4. **Deploy**
   - Click "Deploy!"
   - Wait for build to complete
   - App will be available at: `https://YOUR_APP_NAME.streamlit.app`

### Option 2: Local Deployment

1. **Clone repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/medical-diagnosis-ai.git
   cd medical-diagnosis-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-github.txt
   ```

3. **Run application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Docker Deployment (Optional)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-github.txt .
RUN pip install -r requirements-github.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and run
```bash
docker build -t medical-diagnosis-ai .
docker run -p 8501:8501 medical-diagnosis-ai
```

## Environment Variables

For production deployment, consider these environment variables:

```bash
STREAMLIT_SERVER_PORT=5000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Security Considerations

1. **Medical Data Privacy**
   - Never store uploaded medical images
   - Implement user session isolation
   - Add SSL/TLS for production

2. **Model Security**
   - Validate all inputs
   - Implement rate limiting
   - Monitor for adversarial inputs

3. **Compliance**
   - Ensure HIPAA compliance if handling real patient data
   - Add appropriate disclaimers
   - Implement audit logging

## Monitoring and Maintenance

1. **Application Monitoring**
   - Set up health checks
   - Monitor resource usage
   - Track error rates

2. **Model Performance**
   - Monitor prediction accuracy
   - Track model drift
   - Update models regularly

3. **User Analytics**
   - Track usage patterns
   - Monitor user feedback
   - Analyze feature adoption

## Troubleshooting

### Common Issues

1. **TensorFlow Installation**
   ```bash
   # If TensorFlow fails to install
   pip install tensorflow-cpu
   ```

2. **Memory Issues**
   ```bash
   # Increase memory limits
   export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
   ```

3. **Port Conflicts**
   ```bash
   # Use different port
   streamlit run app.py --server.port 8502
   ```

### Support

- Check GitHub Issues for common problems
- Review Streamlit documentation
- Contact repository maintainers