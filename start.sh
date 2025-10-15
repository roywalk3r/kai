#!/bin/bash
# Quick start script for Kai

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Load shell config to get environment variables
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
elif [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc"
fi

# Activate virtual environment
source "$SCRIPT_DIR/.venv/bin/activate"

# Start Kai
python "$SCRIPT_DIR/main.py"
