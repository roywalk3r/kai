#!/bin/bash
# Quick start script for Kai

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load environment variables from shell configs
# Try to get GEMINI_API_KEY from shell config files
if [ -z "$GEMINI_API_KEY" ]; then
    # Check bash config
    if [ -f "$HOME/.bashrc" ]; then
        export GEMINI_API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.bashrc" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
    fi
    
    # Check zsh config if still not found
    if [ -z "$GEMINI_API_KEY" ] && [ -f "$HOME/.zshrc" ]; then
        export GEMINI_API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.zshrc" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
    fi
    
    # Check bash profile
    if [ -z "$GEMINI_API_KEY" ] && [ -f "$HOME/.bash_profile" ]; then
        export GEMINI_API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.bash_profile" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
    fi
    
    # Check profile
    if [ -z "$GEMINI_API_KEY" ] && [ -f "$HOME/.profile" ]; then
        export GEMINI_API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.profile" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
    fi
fi

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Start Kai
python "$SCRIPT_DIR/main.py"
