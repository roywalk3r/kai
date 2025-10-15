# Kai Installation Guide

## 🚀 Quick Install

```bash
git clone https://github.com/roywalk3r/kai.git
cd kai
chmod +x install.sh
./install.sh
```

---

## 📋 Interactive Setup Flow

When you run `./install.sh`, here's what happens:

### Step 1: System Check
```
🤖 Installing Kai Terminal Assistant...
✓ Found Python 3.13
✓ Found Ollama
✓ Found llama3 model
```

### Step 2: Virtual Environment
```
✓ Virtual environment already exists
Installing dependencies...
```

### Step 3: AI Model Selection (Interactive!)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 AI Model Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Kai supports two AI models:
  1. Gemini (Google) - Fast, accurate, cloud-based (Recommended)
  2. Ollama - Local, private, offline

Would you like to use Gemini AI? (Recommended)
Enter your choice [Y/n]:
```

### Option A: Choose Gemini (Recommended)

**If you press Y or Enter:**
```
Great! Let's set up Gemini.

📝 Get your free API key:
   1. Visit: https://aistudio.google.com/apikey
   2. Sign in with Google
   3. Click 'Create API Key'
   4. Copy the key (starts with AIza...)

Enter your Gemini API key (or press Enter to skip):
```

**After entering your API key:**
```
✅ Gemini API key saved to /home/user/.bashrc
   Kai will use Gemini AI (Google)
```

**The script automatically:**
- Saves API key to your shell config (.bashrc or .zshrc)
- Sets it for current session
- Configures Kai to use Gemini

### Option B: Choose Ollama

**If you press N:**
```
ℹ️  Using Ollama (local AI)
   Make sure Ollama is installed and llama3 model is pulled

   To use Gemini later, set GEMINI_API_KEY environment variable
```

### Option C: Skip Gemini Setup

**If you press Enter when asked for API key:**
```
ℹ️  Skipping Gemini setup
   Kai will use Ollama (local AI) by default

   To use Gemini later:
   1. Get API key: https://aistudio.google.com/apikey
   2. export GEMINI_API_KEY="your-key-here"
   3. Restart Kai
```

### Step 4: Completion
```
✅ Installation complete!

To start Kai, run:
  source .venv/bin/activate
  python main.py

Or add an alias to your shell config:
  alias kai='cd /path/to/kai && source .venv/bin/activate && python main.py'
```

---

## 🎯 What Gets Configured

### If You Choose Gemini:

**Your shell config gets updated:**
```bash
# Added to ~/.bashrc or ~/.zshrc
export GEMINI_API_KEY="your-api-key-here"
```

**Kai configuration:**
- `use_gemini: true` (default)
- API key available in environment
- Automatic fallback to Ollama if needed

### If You Choose Ollama:

**No changes to shell config**

**Kai configuration:**
- Uses Ollama by default
- Can switch to Gemini anytime by setting API key

---

## 🔄 Switching Models Later

### Add Gemini After Installation

```bash
# Get API key from https://aistudio.google.com/apikey

# Add to your shell config
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# Restart Kai
python main.py
```

### Switch to Ollama

```bash
# In Kai
> config set use_gemini false

# Or unset the API key
unset GEMINI_API_KEY
```

---

## 💡 Tips

### 1. API Key Security
- The script saves your API key to shell config
- This is safe for personal use
- Don't commit shell config to public repos

### 2. Multiple Machines
- Get separate API keys for different machines
- Or use the same key (not recommended for production)

### 3. Testing Both Models
```bash
# Try Gemini
export GEMINI_API_KEY="your-key"
python main.py

# Try Ollama
unset GEMINI_API_KEY
python main.py
```

### 4. Verify Setup
```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Should show your key (or empty if not set)
```

---

## 🐛 Troubleshooting

### "Could not find shell config file"

**Problem:** Script can't find .bashrc or .zshrc

**Solution:**
```bash
# Manually add to your shell config
echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

### API Key Not Working

**Problem:** Kai still uses Ollama

**Solution:**
```bash
# Verify API key is set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your-key"

# Restart Kai
python main.py
```

### Want to Change API Key

**Solution:**
```bash
# Edit your shell config
nano ~/.bashrc  # or ~/.zshrc

# Find and update the line:
export GEMINI_API_KEY="new-key-here"

# Reload config
source ~/.bashrc
```

---

## 📚 More Information

- **Gemini Setup:** See [GEMINI_SETUP.md](GEMINI_SETUP.md)
- **Quick Start:** See [QUICKSTART.md](QUICKSTART.md)
- **Full Docs:** See [README.md](README.md)

---

## 🎉 You're Ready!

The installation script makes setup easy:
1. **Interactive** - Asks what you want
2. **Smart** - Configures everything automatically
3. **Flexible** - Easy to change later

Just run `./install.sh` and follow the prompts! 🚀
