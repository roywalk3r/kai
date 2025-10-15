#!/bin/bash
# Uninstaller for Kai Terminal Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🤖 Kai Terminal Assistant - Uninstaller${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Determine installation location
INSTALL_DIR=""
BIN_DIR=""

if [ -d "/opt/kai" ]; then
    INSTALL_DIR="/opt/kai"
    BIN_DIR="/usr/local/bin"
    echo -e "${YELLOW}Found system-wide installation${NC}"
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ System-wide uninstall requires root privileges${NC}"
        echo "Please run: sudo $0"
        exit 1
    fi
elif [ -d "$HOME/.local/share/kai" ]; then
    INSTALL_DIR="$HOME/.local/share/kai"
    BIN_DIR="$HOME/.local/bin"
    echo -e "${YELLOW}Found user installation${NC}"
else
    echo -e "${RED}❌ Kai installation not found${NC}"
    exit 1
fi

echo ""
echo "This will remove:"
echo "  • $INSTALL_DIR"
echo "  • $BIN_DIR/kai"
echo ""
echo -e "${YELLOW}⚠️  Your configuration and history in ~/.kai will be preserved${NC}"
echo ""

read -p "Are you sure you want to uninstall Kai? [y/N]: " confirm

if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}Uninstalling Kai...${NC}"

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓ Removed installation directory${NC}"
fi

# Remove executable
if [ -f "$BIN_DIR/kai" ]; then
    echo "Removing $BIN_DIR/kai..."
    rm -f "$BIN_DIR/kai"
    echo -e "${GREEN}✓ Removed executable${NC}"
fi

echo ""
echo -e "${GREEN}✅ Kai has been uninstalled${NC}"
echo ""
echo "To remove your configuration and history:"
echo "  rm -rf ~/.kai"
echo ""
echo "To remove Gemini API key from shell config:"
echo "  Edit ~/.bashrc or ~/.zshrc and remove the GEMINI_API_KEY line"
echo ""
