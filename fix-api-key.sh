#!/bin/bash
# Fix Gemini API Key for Current Shell

echo "🔧 Fixing Gemini API Key Configuration"
echo ""

# Detect current shell
CURRENT_SHELL=$(basename "$SHELL")
echo "Detected shell: $CURRENT_SHELL"
echo ""

# Extract API key from any config file
API_KEY=""
if [ -f "$HOME/.bashrc" ]; then
    API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.bashrc" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
fi

if [ -z "$API_KEY" ] && [ -f "$HOME/.zshrc" ]; then
    API_KEY=$(grep "export GEMINI_API_KEY" "$HOME/.zshrc" 2>/dev/null | sed 's/.*GEMINI_API_KEY="\(.*\)"/\1/' | tail -1)
fi

if [ -z "$API_KEY" ]; then
    echo "❌ No GEMINI_API_KEY found in shell configs"
    echo ""
    echo "Please run the installer again or manually add:"
    echo "  export GEMINI_API_KEY=\"your-api-key-here\""
    exit 1
fi

echo "✓ Found API key: ${API_KEY:0:20}..."
echo ""

# Determine target config file
if [ "$CURRENT_SHELL" = "zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
elif [ "$CURRENT_SHELL" = "bash" ]; then
    CONFIG_FILE="$HOME/.bashrc"
else
    CONFIG_FILE="$HOME/.profile"
fi

echo "Target config: $CONFIG_FILE"
echo ""

# Check if already exists in target file
if grep -q "export GEMINI_API_KEY" "$CONFIG_FILE" 2>/dev/null; then
    echo "✓ API key already in $CONFIG_FILE"
else
    echo "Adding API key to $CONFIG_FILE..."
    echo "" >> "$CONFIG_FILE"
    echo "# Prometheus - Gemini API Key" >> "$CONFIG_FILE"
    echo "export GEMINI_API_KEY=\"$API_KEY\"" >> "$CONFIG_FILE"
    echo "✓ Added to $CONFIG_FILE"
fi

echo ""
echo "✅ Configuration updated!"
echo ""
echo "Next steps:"
echo "  1. Reload your shell config:"
echo "     source $CONFIG_FILE"
echo ""
echo "  2. Test Prometheus:"
echo "     prom"
echo ""
echo "You should see: 🤖 Using Gemini AI (Google)"
