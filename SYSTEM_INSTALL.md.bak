# Kai System Installation Guide

## 🚀 System-Wide Installation

Install Kai once and access it from any terminal session!

---

## 📋 Installation Methods

### Method 1: User Installation (Recommended)

Install for current user only (no sudo required):

```bash
git clone https://github.com/roywalk3r/kai.git
cd kai
chmod +x system-install.sh
./system-install.sh
```

**Installs to:**
- `~/.local/share/kai` - Application files
- `~/.local/bin/kai` - Executable

**Accessible by:** Current user only

---

### Method 2: System-Wide Installation

Install for all users (requires sudo):

```bash
git clone https://github.com/roywalk3r/kai.git
cd kai
chmod +x system-install.sh
sudo ./system-install.sh
```

**Installs to:**
- `/opt/kai` - Application files
- `/usr/local/bin/kai` - Executable

**Accessible by:** All users on the system

---

## 🎯 What Gets Installed

### Files & Directories

```
User Installation:
~/.local/share/kai/          # Application files
├── ai/                      # AI modules
├── core/                    # Core functionality
├── utils/                   # Utilities
├── .venv/                   # Virtual environment
└── main.py                  # Entry point

~/.local/bin/kai             # Executable wrapper
~/.kai/                      # User data (config, history)
```

```
System Installation:
/opt/kai/                    # Application files
/usr/local/bin/kai           # Executable wrapper
~/.kai/                      # User data (per user)
```

---

## ⚙️ Installation Process

The installer will:

1. **Check Requirements**
   - Python 3.8+
   - Ollama (optional)

2. **Copy Files**
   - Application to install directory
   - Create virtual environment
   - Install dependencies

3. **Setup AI Model**
   - Ask if you want to use Gemini
   - Prompt for API key (if yes)
   - Save to shell config
   - Or use Ollama as fallback

4. **Create Executable**
   - Wrapper script in bin directory
   - Auto-loads environment variables
   - Activates virtual environment

5. **Setup Complete**
   - Ready to use from any terminal!

---

## 🔧 Post-Installation

### 1. Reload Shell Config

If you set up Gemini API key:

```bash
source ~/.bashrc  # or ~/.zshrc
```

Or open a new terminal.

### 2. Verify Installation

```bash
kai --version
```

Should show: `Kai Terminal Assistant v1.0.0`

### 3. Test It

```bash
kai
```

You should see the beautiful Kai welcome screen!

---

## 💡 Usage

### Start Kai

```bash
kai
```

### Command-Line Options

```bash
kai --help              # Show help
kai --version           # Show version
kai --dry-run           # Enable preview mode
kai --no-banner         # Skip welcome screen
```

### Access from Anywhere

```bash
# From any directory
cd /tmp
kai

# Works in any terminal session
# Works after reboot
# Works for all users (if system-wide)
```

---

## 🔄 Updating Kai

### User Installation

```bash
cd ~/.local/share/kai
git pull
.venv/bin/pip install -r requirements.txt
```

### System Installation

```bash
cd /opt/kai
sudo git pull
sudo .venv/bin/pip install -r requirements.txt
```

---

## 🗑️ Uninstallation

### Run Uninstaller

```bash
# User installation
cd ~/.local/share/kai
./uninstall.sh

# System installation
cd /opt/kai
sudo ./uninstall.sh
```

### Manual Uninstall

**User Installation:**
```bash
rm -rf ~/.local/share/kai
rm ~/.local/bin/kai
```

**System Installation:**
```bash
sudo rm -rf /opt/kai
sudo rm /usr/local/bin/kai
```

### Remove User Data (Optional)

```bash
rm -rf ~/.kai
```

### Remove API Key from Shell Config

Edit `~/.bashrc` or `~/.zshrc` and remove:
```bash
# Kai - Gemini API Key
export GEMINI_API_KEY="..."
```

---

## 🛠️ Troubleshooting

### "kai: command not found"

**Problem:** `~/.local/bin` not in PATH

**Solution:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:$HOME/.local/bin"

# Reload
source ~/.bashrc
```

### "Permission denied"

**Problem:** Executable not marked as executable

**Solution:**
```bash
chmod +x ~/.local/bin/kai
# or
sudo chmod +x /usr/local/bin/kai
```

### Gemini API Key Not Working

**Problem:** Environment variable not loaded

**Solution:**
```bash
# Check if set
echo $GEMINI_API_KEY

# If empty, reload shell config
source ~/.bashrc

# Or restart terminal
```

### Can't Update

**Problem:** Permission issues

**Solution:**
```bash
# User installation
cd ~/.local/share/kai
git pull

# System installation
cd /opt/kai
sudo git pull
```

---

## 📊 Installation Comparison

| Feature | User Install | System Install |
|---------|-------------|----------------|
| **Requires sudo** | No | Yes |
| **Location** | ~/.local/share | /opt |
| **Accessible by** | Current user | All users |
| **Easy to update** | Yes | Requires sudo |
| **Isolated** | Yes | Shared |
| **Recommended for** | Personal use | Servers, shared systems |

---

## 🎓 Advanced Configuration

### Custom Install Location

Edit `system-install.sh` and change:
```bash
INSTALL_DIR="/your/custom/path"
```

### Multiple Versions

Install different versions:
```bash
# Version 1
./system-install.sh
mv ~/.local/bin/kai ~/.local/bin/kai-v1

# Version 2
git checkout v2.0
./system-install.sh
mv ~/.local/bin/kai ~/.local/bin/kai-v2
```

### Shared Configuration

For system-wide install with shared config:
```bash
sudo mkdir -p /etc/kai
sudo cp ~/.kai/config.json /etc/kai/

# Modify wrapper to use /etc/kai
```

---

## 🔐 Security Considerations

### API Keys

- Stored in user's shell config
- Not accessible by other users
- Can be encrypted with tools like `pass`

### File Permissions

**User Installation:**
- Files owned by user
- Only user can access

**System Installation:**
- Files owned by root
- Readable by all users
- User data in ~/.kai (per user)

### Recommendations

1. **Use user installation** for personal machines
2. **Use system installation** for shared servers
3. **Don't share API keys** between users
4. **Review code** before system-wide install

---

## 📚 Additional Resources

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick start guide
- **GEMINI_SETUP.md** - Gemini configuration
- **TROUBLESHOOTING.md** - Common issues

---

## 🎉 You're All Set!

After installation, Kai is available system-wide:

```bash
# From anywhere
kai

# In any terminal
kai

# After reboot
kai

# For all users (if system-wide)
kai
```

**Enjoy your AI-powered terminal assistant!** 🚀
