#!/bin/bash

# Detect OS type
OS_TYPE=$(uname)

# Determine activate command based on OS
if [[ "$OS_TYPE" == "Linux" || "$OS_TYPE" == "Darwin" ]]; then
    ACTIVATE_CMD="source venv/bin/activate"  # Mac/Linux
elif [[ "$OS_TYPE" == "MINGW"* || "$OS_TYPE" == "CYGWIN"* || "$OS_TYPE" == "MSYS"* ]]; then
    ACTIVATE_CMD="source venv/Scripts/activate"  # Windows (Git Bash, Cygwin)
else
    echo "❌ Unsupported OS. Exiting..."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Exiting..."
    exit 1
fi

# Check if venv exists, if not, create it
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv || python -m venv venv  # Try both python3 and python
    echo "✅ Virtual environment created."
else
    echo "⚡ Virtual environment 'venv' already exists. Skipping creation."
fi

# Activate the virtual environment
echo "🚀 Activating virtual environment..."
eval "$ACTIVATE_CMD"

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Run main.py
echo "▶ Running main.py..."
python main.py

# Deactivate virtual environment after script execution
deactivate
echo "🛑 Virtual environment deactivated."
