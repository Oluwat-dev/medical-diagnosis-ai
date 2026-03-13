#!/bin/bash

echo "======================================"
echo " AI Medical Diagnosis System - Setup"
echo "======================================"

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "Detected Python $PYTHON_VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]); then
    echo "ERROR: Python 3.9, 3.10, or 3.11 is required."
    echo "Please install a supported version from https://www.python.org/downloads/"
    exit 1
fi

if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 12 ]; then
    echo "WARNING: Python 3.12+ is not supported by TensorFlow."
    echo "Please use Python 3.9, 3.10, or 3.11."
    exit 1
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

ARCH=$(uname -m)
OS=$(uname -s)

if [ "$OS" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
    echo ""
    echo "Detected Apple Silicon Mac (M1/M2/M3)"
    echo "Installing TensorFlow for Apple Silicon..."
    pip install tensorflow-macos tensorflow-metal
    echo "Installing remaining dependencies..."
    pip install streamlit "pillow>=10.0.0" "numpy>=1.23.5,<2.0.0" "matplotlib>=3.7.0" \
        "seaborn>=0.12.0" "plotly>=5.0.0" "pandas>=2.0.0" "scikit-learn>=1.3.0" \
        "opencv-python>=4.8.0"
else
    echo ""
    if [ "$OS" = "Linux" ]; then
        echo "Installing system libraries for OpenCV..."
        if command -v apt-get &>/dev/null; then
            sudo apt-get install -y libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 2>/dev/null || \
            sudo apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 2>/dev/null || \
            echo "Note: Could not install system libraries automatically. If opencv fails, run: sudo apt-get install libgl1"
        fi
    fi
    echo "Installing all dependencies..."
    pip install -r requirements-github.txt
fi

echo ""
echo "======================================"
echo " Setup complete!"
echo " Run the app with:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo "======================================"
