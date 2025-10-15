#!/bin/bash
# Installation script for Kai terminal assistant

set -e

echo "🤖 Installing Kai Terminal Assistant..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed."
    echo "Please install Ollama from https://ollama.ai/"
    echo "Then run: ollama pull llama3"
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Found Ollama"
    
    # Check if llama3 model is available
    if ! ollama list | grep -q llama3; then
        echo "⚠️  llama3 model not found"
        read -p "Pull llama3 model now? [Y/n] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            echo "Pulling llama3 model..."
            ollama pull llama3
        fi
    else
        echo "✓ Found llama3 model"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Install dependencies using venv's pip directly
echo "Installing dependencies..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Create .kai directory
mkdir -p ~/.kai

echo ""
echo "✅ Installation complete!"
echo ""
echo "To start Kai, run:"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or add an alias to your shell config:"
echo "  alias kai='cd $(pwd) && source .venv/bin/activate && python main.py'"
