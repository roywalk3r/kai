#!/bin/bash
# System-wide installation script for Kai Terminal Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🤖 Kai Terminal Assistant - System Installer${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if running with sudo for system-wide install
INSTALL_DIR="$HOME/.local/share/kai"
BIN_DIR="$HOME/.local/bin"
SYSTEM_INSTALL=false

if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Running as root. Installing system-wide...${NC}"
    INSTALL_DIR="/opt/kai"
    BIN_DIR="/usr/local/bin"
    SYSTEM_INSTALL=true
else
    echo -e "${GREEN}Installing for current user...${NC}"
    echo -e "${YELLOW}Tip: Run with sudo for system-wide installation${NC}"
fi

echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"

# Check if Ollama is installed (optional)
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Found Ollama${NC}"
    
    # Check if llama3 model is available
    if ollama list | grep -q llama3; then
        echo -e "${GREEN}✓ Found llama3 model${NC}"
    else
        echo -e "${YELLOW}⚠️  llama3 model not found${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found (optional - can use Gemini instead)${NC}"
fi

echo ""

# Create installation directory
echo -e "${CYAN}Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy files to installation directory
echo -e "${CYAN}Copying files...${NC}"
cp -r . "$INSTALL_DIR/"

# Create virtual environment in installation directory
echo -e "${CYAN}Creating virtual environment...${NC}"
cd "$INSTALL_DIR"
python3 -m venv .venv

# Install dependencies
echo -e "${CYAN}Installing dependencies...${NC}"
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

# Create executable wrapper script
echo -e "${CYAN}Creating executable wrapper...${NC}"
cat > "$BIN_DIR/kai" << 'WRAPPER_EOF'
#!/bin/bash
# Kai Terminal Assistant Wrapper

# Get the directory where Kai is installed
if [ -d "/opt/kai" ]; then
    KAI_DIR="/opt/kai"
else
    KAI_DIR="$HOME/.local/share/kai"
fi

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

# Activate virtual environment and run Kai
source "$KAI_DIR/.venv/bin/activate"
python "$KAI_DIR/main.py" "$@"
WRAPPER_EOF

chmod +x "$BIN_DIR/kai"

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🤖 AI Model Setup${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Kai supports two AI models:"
echo "  1. Gemini (Google) - Fast, accurate, cloud-based (Recommended)"
echo "  2. Ollama - Local, private, offline"
echo ""

# Check if Gemini API key already exists
if [ -n "$GEMINI_API_KEY" ]; then
    echo -e "${GREEN}✓ Gemini API key already set${NC}"
    echo "  Kai will use Gemini AI (Google)"
else
    read -p "Would you like to use Gemini AI? [Y/n]: " use_gemini
    
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
            # Determine which shell config to use
            SHELL_CONFIG=""
            if [ -f "$HOME/.bashrc" ]; then
                SHELL_CONFIG="$HOME/.bashrc"
            elif [ -f "$HOME/.zshrc" ]; then
                SHELL_CONFIG="$HOME/.zshrc"
            fi
            
            if [ -n "$SHELL_CONFIG" ]; then
                # Check if already exists
                if grep -q "GEMINI_API_KEY" "$SHELL_CONFIG"; then
                    echo -e "${YELLOW}⚠️  GEMINI_API_KEY already exists in $SHELL_CONFIG${NC}"
                    read -p "Update it? [y/N]: " update_key
                    if [[ $update_key =~ ^[Yy]$ ]]; then
                        # Update existing key
                        if [[ "$OSTYPE" == "darwin"* ]]; then
                            sed -i '' "/GEMINI_API_KEY/d" "$SHELL_CONFIG"
                        else
                            sed -i "/GEMINI_API_KEY/d" "$SHELL_CONFIG"
                        fi
                        echo "" >> "$SHELL_CONFIG"
                        echo "# Kai - Gemini API Key" >> "$SHELL_CONFIG"
                        echo "export GEMINI_API_KEY=\"$api_key\"" >> "$SHELL_CONFIG"
                        echo -e "${GREEN}✅ Gemini API key updated in $SHELL_CONFIG${NC}"
                    fi
                else
                    echo "" >> "$SHELL_CONFIG"
                    echo "# Kai - Gemini API Key" >> "$SHELL_CONFIG"
                    echo "export GEMINI_API_KEY=\"$api_key\"" >> "$SHELL_CONFIG"
                    echo -e "${GREEN}✅ Gemini API key saved to $SHELL_CONFIG${NC}"
                fi
                
                # Also set for current session
                export GEMINI_API_KEY="$api_key"
                
                echo "   Kai will use Gemini AI (Google)"
            else
                echo -e "${YELLOW}⚠️  Could not find shell config file${NC}"
                echo "   Please manually add to your shell config:"
                echo "   export GEMINI_API_KEY=\"$api_key\""
            fi
        else
            echo ""
            echo -e "${YELLOW}ℹ️  Skipping Gemini setup${NC}"
            echo "   Kai will use Ollama (local AI) by default"
        fi
    else
        echo ""
        echo -e "${YELLOW}ℹ️  Using Ollama (local AI)${NC}"
        echo "   Make sure Ollama is installed and llama3 model is pulled"
    fi
fi

# Create .kai directory for user data
mkdir -p "$HOME/.kai"

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📍 Installation Details:"
echo "   • Installed to: $INSTALL_DIR"
echo "   • Executable: $BIN_DIR/kai"
if [ "$SYSTEM_INSTALL" = true ]; then
    echo "   • Type: System-wide (all users)"
else
    echo "   • Type: User-only"
fi
echo ""

# Check if BIN_DIR is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠️  IMPORTANT: Add $BIN_DIR to your PATH${NC}"
    echo ""
    echo "Add this to your shell config (~/.bashrc or ~/.zshrc):"
    echo "   export PATH=\"\$PATH:$BIN_DIR\""
    echo ""
fi

# Remind to reload shell config if API key was added
if grep -q "# Kai - Gemini API Key" "$HOME/.bashrc" 2>/dev/null || grep -q "# Kai - Gemini API Key" "$HOME/.zshrc" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  IMPORTANT: Reload your shell configuration:${NC}"
    if [ -f "$HOME/.bashrc" ]; then
        echo "   source ~/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        echo "   source ~/.zshrc"
    fi
    echo ""
    echo "Or open a new terminal window."
    echo ""
fi

echo "🚀 To start Kai, simply type:"
echo -e "   ${CYAN}kai${NC}"
echo ""
echo "📚 For help, type:"
echo -e "   ${CYAN}kai --help${NC}"
echo ""
echo "🎉 Enjoy your AI-powered terminal assistant!"
echo ""
