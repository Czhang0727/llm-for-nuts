#!/bin/bash

# LLM Learning Project Setup Script

echo "Setting up LLM Learning Project..."

# Check if Homebrew is installed, install if not
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "Homebrew found. Proceeding with installation..."
fi

# Install Python 3.12 and Jupyter Notebook using Homebrew (Mac)
echo "Installing Python 3.12..."
brew install python@3.12

echo "Installing Jupyter notebook..."
brew install jupyter

# Create virtual environment with Python 3.12
echo "Creating virtual environment with Python 3.12..."
python3.12 -m venv llm-for-nuts-venv

# Activate virtual environment
echo "Activating virtual environment..."
source llm-for-nuts-venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Register the virtual environment as a Jupyter kernel
echo "Registering virtual environment as Jupyter kernel..."
python3.12 -m ipykernel install --user --name=llm-for-nuts --display-name="LLM for Nuts (Python 3.12)"

# Create notebooks directory if it doesn't exist
echo "Creating notebooks directory..."
mkdir -p notebooks

echo "Setup complete!"
echo "To activate the virtual environment in the future, run: source llm-for-nuts-venv/bin/activate"
echo "To start Jupyter notebook, run: jupyter notebook"
