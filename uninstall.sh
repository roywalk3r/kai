#!/bin/bash
# Uninstaller for Prometheus Terminal Assistant

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔥 Prometheus Terminal Assistant - Uninstaller${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Determine installation location
INSTALL_DIR=""
BIN_DIR=""

if [ -d "/opt/prometheus" ]; then
    INSTALL_DIR="/opt/prometheus"
    BIN_DIR="/usr/local/bin"
    echo -e "${YELLOW}Found system-wide installation${NC}"
    if [ "$EUID" -ne 0 ]; then
        echo -e "${RED}❌ System-wide uninstall requires root privileges${NC}"
        echo "Please run: sudo $0"
        exit 1
    fi
elif [ -d "$HOME/.local/share/prometheus" ]; then
    INSTALL_DIR="$HOME/.local/share/prometheus"
    BIN_DIR="$HOME/.local/bin"
    echo -e "${YELLOW}Found user installation${NC}"
else
    echo -e "${RED}❌ Prometheus installation not found${NC}"
    exit 1
fi

echo ""
echo "This will remove:"
echo "  • $INSTALL_DIR"
echo "  • $BIN_DIR/<alias>"
echo ""
echo -e "${YELLOW}⚠️  Your configuration and history in ~/.prometheus will be preserved${NC}"
echo ""

read -p "Are you sure you want to uninstall Prometheus? [y/N]: " confirm

if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}Uninstall cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}Uninstalling Prometheus...${NC}"

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    echo -e "${GREEN}✓ Removed installation directory${NC}"
fi

# Remove executable
# Remove all prometheus aliases
for file in "$BIN_DIR"/*; do
    if [ -f "$file" ] && grep -q "PROMETHEUS_DIR" "$file" 2>/dev/null; then
        echo "Removing $file..."
        rm -f "$file"
    fi
done
if [ -f "$BIN_DIR/prom" ]; then
    echo "Removing $BIN_DIR/prom..."
    rm -f "$BIN_DIR/prom"
    echo -e "${GREEN}✓ Removed executable${NC}"
fi

echo ""
echo -e "${GREEN}✅ Prometheus has been uninstalled${NC}"
echo ""
echo "To remove your configuration and history:"
echo "  rm -rf ~/.prometheus"
echo ""
echo "To remove Gemini API key from shell config:"
echo "  Edit ~/.bashrc or ~/.zshrc and remove the GEMINI_API_KEY line"
echo ""
