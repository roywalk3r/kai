# Kai Quick Reference Card

## 🚀 Starting Kai

```bash
# Activate virtual environment
source .venv/bin/activate

# Start Kai
python main.py

# Or create an alias (add to ~/.bashrc or ~/.zshrc)
alias kai='cd /path/to/kai && source .venv/bin/activate && python main.py'
```

## 💬 Basic Commands

```
> list my files                    # Natural language
> create a file called test.txt    # File operations
> show disk usage                  # System info
> find all python files            # Search
```

## 🎮 Special Commands

| Command | Description |
|---------|-------------|
| `help` or `?` | Show help menu |
| `examples` | Show command examples |
| `history` | Show recent commands |
| `history 5` | Show last 5 commands |
| `clear-history` | Clear command history |
| `config` | Show configuration |
| `config set <key> <value>` | Set config value |
| `dry-run on` | Enable preview mode |
| `dry-run off` | Disable preview mode |
| `terminate` | Kill running process |
| `clear` or `cls` | Clear screen |
| `exit` or `quit` | Exit Kai |

## ⚙️ Configuration Options

```
> config set timeout_seconds 30        # Set timeout
> config set dry_run true              # Enable dry-run
> config set history_size 200          # Set history size
```

**Available Options:**
- `timeout_seconds` (default: 20)
- `default_model` (default: llama3)
- `auto_confirm_safe` (default: false)
- `history_size` (default: 100)
- `dry_run` (default: false)

## 🛡️ Safety Features

Kai will warn you about:
- ⚠️ **Dangerous commands** (rm -rf, dd, mkfs, etc.)
- ⏳ **Long-running commands** (ping, find /, sleep, etc.)
- 🚫 **Interactive commands** (nano, vim, top, etc.)

## 📝 Example Usage

### File Operations
```
> create a backup of my documents
> compress the logs folder
> find files larger than 100MB
> show contents of config.json
```

### System Information
```
> show system resources
> what's my IP address
> check disk space
> show running processes
```

### Development
```
> find all TODO comments in python files
> count lines of code
> show git status
> list files modified today
```

## 🎯 Tips & Tricks

1. **Use context** - Kai remembers recent commands:
   ```
   > create a file called notes.txt
   > add "Hello" to it              # "it" refers to notes.txt
   > show it                         # Shows notes.txt
   ```

2. **Preview commands** with dry-run:
   ```
   > dry-run on
   > delete old_file.txt             # Shows command but doesn't run
   > dry-run off
   ```

3. **View history** to replay commands:
   ```
   > history 10                      # Show last 10 commands
   ```

4. **Get suggestions** when stuck:
   ```
   > examples                        # Show categorized examples
   ```

## 🔧 Troubleshooting

### Ollama not found
```bash
# Install Ollama from https://ollama.ai/
# Then pull the model
ollama pull llama3
```

### Command timeout
```
> config set timeout_seconds 60     # Increase timeout
```

### Dependencies missing
```bash
.venv/bin/pip install -r requirements.txt
```

### Verify installation
```bash
.venv/bin/python verify.py
```

## 📚 More Help

- Type `help` in Kai for full command list
- Type `examples` for command examples
- Read `README.md` for complete documentation
- Read `QUICKSTART.md` for setup guide

## 🎓 Keyboard Shortcuts

- **↑/↓** - Navigate command history
- **Tab** - Auto-complete (when available)
- **Ctrl+C** - Cancel current input
- **Ctrl+D** - Exit Kai

## 📁 File Locations

- **Config**: `~/.kai/config.json`
- **History**: `~/.kai/history.json`
- **Prompt History**: `~/.kai/prompt_history`

---

**Version**: 1.0.0
**Status**: Production Ready ✅

For complete documentation, see README.md
