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

# Setup AI Model
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo """
   ██╗  ██╗ █████╗ ██╗
    ██║ ██╔╝██╔══██╗██║
    █████╔╝ ███████║██║
    ██╔═██╗ ██╔══██║██║
    ██║  ██╗██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ 🤖 AI Model Setup
"""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Kai supports two AI models:"
echo "  1. Gemini (Google) - Fast, accurate, cloud-based (Recommended)"
echo "  2. Ollama - Local, private, offline"
echo ""

# Check if Gemini API key already exists
if [ -n "$GEMINI_API_KEY" ]; then
    echo "✓ Gemini API key already set"
    echo "  Kai will use Gemini AI (Google)"
else
    echo "Would you like to use Gemini AI? (Recommended)"
    read -p "Enter your choice [Y/n]: " use_gemini
    
    if [[ ! $use_gemini =~ ^[Nn]$ ]]; then
        echo ""
        echo "Great! Let's set up Gemini."
        echo ""
        echo "📝 Get your free API key:"
        echo "   1. Visit: https://aistudio.google.com/apikey"
        echo "   2. Sign in with Google"
        echo "   3. Click 'Create API Key'"
        echo "   4. Copy the key (starts with AIza...)"
        echo ""
        read -p "Enter your Gemini API key (or press Enter to skip): " api_key
        
        if [ -n "$api_key" ]; then
            # Add to shell config
            SHELL_CONFIG=""
            if [ -f "$HOME/.bashrc" ]; then
                SHELL_CONFIG="$HOME/.bashrc"
            elif [ -f "$HOME/.zshrc" ]; then
                SHELL_CONFIG="$HOME/.zshrc"
            fi
            
            if [ -n "$SHELL_CONFIG" ]; then
                echo "" >> "$SHELL_CONFIG"
                echo "# Kai - Gemini API Key" >> "$SHELL_CONFIG"
                echo "export GEMINI_API_KEY=\"$api_key\"" >> "$SHELL_CONFIG"
                
                # Also set for current session
                export GEMINI_API_KEY="$api_key"
                
                echo ""
                echo "✅ Gemini API key saved to $SHELL_CONFIG"
                echo "   Kai will use Gemini AI (Google)"
            else
                echo ""
                echo "⚠️  Could not find shell config file"
                echo "   Please manually add to your shell config:"
                echo "   export GEMINI_API_KEY=\"$api_key\""
            fi
        else
            echo ""
            echo "ℹ️  Skipping Gemini setup"
            echo "   Kai will use Ollama (local AI) by default"
            echo ""
            echo "   To use Gemini later:"
            echo "   1. Get API key: https://aistudio.google.com/apikey"
            echo "   2. export GEMINI_API_KEY=\"your-key-here\""
            echo "   3. Restart Kai"
        fi
    else
        echo ""
        echo "ℹ️  Using Ollama (local AI)"
        echo "   Make sure Ollama is installed and llama3 model is pulled"
        echo ""
        echo "   To use Gemini later, set GEMINI_API_KEY environment variable"
    fi
fi

# Create .kai directory
mkdir -p ~/.kai

echo ""
echo "✅ Installation complete!"
echo ""

# Check if API key was just added
if grep -q "# Kai - Gemini API Key" "$HOME/.bashrc" 2>/dev/null || grep -q "# Kai - Gemini API Key" "$HOME/.zshrc" 2>/dev/null; then
    echo "⚠️  IMPORTANT: Reload your shell configuration to activate Gemini:"
    if [ -f "$HOME/.bashrc" ]; then
        echo "  source ~/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        echo "  source ~/.zshrc"
    fi
    echo ""
    echo "Or open a new terminal window."
    echo ""
fi

echo "To start Kai, run:"
echo ""
echo "Option 1 (Easiest - auto-loads API key):"
echo "  ./start.sh"
echo ""
echo "Option 2 (Manual):"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "Or add an alias to your shell config:"
echo "  alias kai='$(pwd)/start.sh'"
