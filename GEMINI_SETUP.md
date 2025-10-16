# Gemini AI Setup Guide

## 🚀 Quick Start

Prometheus now supports **Google Gemini AI** as the primary AI model! It's faster, more accurate, and works from anywhere.

---

## 📋 Prerequisites

1. **Google AI Studio Account** (Free)
2. **API Key** (Get it in 2 minutes)
3. **Internet Connection**

---

## 🔑 Getting Your Gemini API Key

### Step 1: Go to Google AI Studio
Visit: https://aistudio.google.com/apikey

### Step 2: Sign In
- Use your Google account
- Accept the terms of service

### Step 3: Create API Key
- Click **"Get API Key"** or **"Create API Key"**
- Select **"Create API key in new project"**
- Copy the API key (starts with `AIza...`)

### Step 4: Save Your API Key
**⚠️ Important:** Keep this key secret! Don't share it or commit it to git.

---

## ⚙️ Configuration

### Option 1: Environment Variable (Recommended)

#### Linux/Mac (Temporary - current session only):
```bash
export GEMINI_API_KEY="your-api-key-here"
```

#### Linux/Mac (Permanent - add to ~/.bashrc or ~/.zshrc):
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your-api-key-here
```

#### Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

#### Windows (Permanent):
1. Search for "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "User variables", click "New"
4. Variable name: `GEMINI_API_KEY`
5. Variable value: `your-api-key-here`
6. Click OK

### Option 2: .env File (Alternative)

Create a `.env` file in the Prometheus directory:
```bash
GEMINI_API_KEY=your-api-key-here
```

Then load it before starting Prometheus:
```bash
source .env
python main.py
```

---

## 🎯 Verification

### Check if Gemini is Active

Start Prometheus and look for:
```
🤖 Using Gemini AI (Google)
```

If you see:
```
🤖 Using Ollama (Local AI)
💡 Tip: Set GEMINI_API_KEY environment variable to use Gemini
```

Then Gemini is not configured yet.

### Test Gemini

```bash
# Check if API key is set
echo $GEMINI_API_KEY

# Should show your API key (not empty)
```

---

## 🔄 Switching Between Models

### Use Gemini (Default)
```
> config set use_gemini true
```

### Use Ollama
```
> config set use_gemini false
```

### Check Current Model
```
> config
```

Look for `use_gemini: true` or `use_gemini: false`

---

## 💡 Why Use Gemini?

### Advantages
✅ **Faster responses** - Cloud-based, no local processing
✅ **More accurate** - Latest Google AI technology
✅ **Always available** - No need to install Ollama
✅ **Better understanding** - Improved natural language processing
✅ **Free tier** - Generous free quota for personal use

### When to Use Ollama Instead
- 🔒 **Privacy concerns** - Keep everything local
- 🌐 **No internet** - Work offline
- 💰 **API limits** - Exceeded free quota
- 🎯 **Specific models** - Need a particular Ollama model

---

## 📊 Model Comparison

| Feature | Gemini | Ollama |
|---------|--------|--------|
| **Speed** | ⚡⚡⚡ Fast | ⚡⚡ Medium |
| **Accuracy** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Setup** | Easy (API key) | Medium (install) |
| **Internet** | Required | Not required |
| **Privacy** | Cloud-based | Local |
| **Cost** | Free tier | Free |
| **Models** | Gemini 2.0 Flash | llama3, etc. |

---

## 🛠️ Troubleshooting

### "No AI model available"

**Problem:** Neither Gemini nor Ollama is configured.

**Solution:**
1. Set GEMINI_API_KEY environment variable, OR
2. Install Ollama and pull llama3 model

### "Gemini error: API key not valid"

**Problem:** Invalid or expired API key.

**Solution:**
1. Go to https://aistudio.google.com/apikey
2. Create a new API key
3. Update your GEMINI_API_KEY environment variable

### "Gemini error: Quota exceeded"

**Problem:** You've exceeded the free tier limit.

**Solution:**
1. Wait for quota to reset (usually daily)
2. Switch to Ollama: `> config set use_gemini false`
3. Or upgrade to paid tier (if needed)

### Gemini not being used

**Problem:** API key not detected.

**Solution:**
```bash
# Check if set
echo $GEMINI_API_KEY

# If empty, set it
export GEMINI_API_KEY="your-key-here"

# Restart Prometheus
python main.py
```

---

## 🔐 Security Best Practices

### ✅ DO:
- Store API key in environment variables
- Use `.env` file (add to `.gitignore`)
- Keep API key secret
- Rotate keys periodically
- Use separate keys for different projects

### ❌ DON'T:
- Hardcode API key in source code
- Commit API key to git
- Share API key publicly
- Use same key for production and testing
- Store in plain text files

---

## 📈 Usage Limits

### Free Tier (as of 2024)
- **Requests per minute:** 15
- **Requests per day:** 1,500
- **Tokens per minute:** 1 million

This is more than enough for personal use!

### Monitoring Usage
Visit: https://aistudio.google.com/

---

## 🎓 Advanced Configuration

### Change Gemini Model

Edit `~/.prometheus/config.json`:
```json
{
  "use_gemini": true,
  "gemini_model": "gemini-2.0-flash-exp"
}
```

Available models:
- `gemini-2.0-flash-exp` (Recommended - Fast & Smart)
- `gemini-1.5-pro` (More powerful, slower)
- `gemini-1.5-flash` (Balanced)

### Disable Gemini Temporarily

```bash
# In Prometheus
> config set use_gemini false

# Restart Prometheus to use Ollama
```

---

## 🚀 Complete Setup Example

```bash
# 1. Get API key from https://aistudio.google.com/apikey

# 2. Set environment variable
export GEMINI_API_KEY="AIzaSyD..."

# 3. Install google-genai package
pip install google-genai

# 4. Start Prometheus
python main.py

# 5. Verify
# You should see: "🤖 Using Gemini AI (Google)"

# 6. Test it!
> list my files
> create a test file
> show system info
```

---

## 📞 Support

### Getting Help
- Check error messages in Prometheus
- Review this guide
- Visit Google AI Studio docs: https://ai.google.dev/

### Common Issues
1. **API key not working** → Regenerate key
2. **Quota exceeded** → Switch to Ollama temporarily
3. **Network errors** → Check internet connection

---

## 🎉 You're All Set!

Once configured, Prometheus will automatically use Gemini for all AI requests. Enjoy faster, smarter command generation!

**Need to switch back to Ollama?** Just run:
```
> config set use_gemini false
```

---

**Happy commanding with Gemini! 🚀**
