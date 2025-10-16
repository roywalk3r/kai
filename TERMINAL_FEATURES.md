# 🖥️ Prometheus Terminal Features

Complete guide to all terminal-first features in Prometheus.

## Table of Contents
- [Quick Actions](#quick-actions)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Smart History](#smart-history)
- [Search & Navigation](#search--navigation)
- [Context Awareness](#context-awareness)
- [Plugin System](#plugin-system)
- [Command-Line Flags](#command-line-flags)

---

## Quick Actions

Fast utilities accessible from command line or interactive mode.

### URL Shortener
```bash
# In interactive mode
--shorten https://very-long-url.com

# Command line
prom --shorten "https://very-long-url.com"
```

### QR Code Generator
```bash
# Generate QR code (ASCII art in terminal)
--qr "https://example.com"
--qr "Hello World"

# Command line
prom --qr "Your text here"
```

### Hash Generator
```bash
# Generate all hashes (MD5, SHA1, SHA256, SHA512)
--hash "text to hash"

# Command line
prom --hash "sensitive data"
```

### Text Encoding/Decoding
```bash
# Encode text
--encode base64 "Hello World"
--encode hex "secret"
--encode url "text with spaces"

# Decode text
--decode base64 "SGVsbG8gV29ybGQ="
--decode hex "48656c6c6f"

# Command line
prom --encode base64 "Hello World"
```

### World Clock
```bash
# Show multiple timezones
--time

# Specific location
--time "New York"
--time "Tokyo"
--time "London"

# Command line
prom --time
prom --time "Paris"
```

### Calculator
```bash
# Calculate expressions
--calc "2 + 2"
--calc "100 * 3.14"
--calc "2 ** 10"
```

---

## Keyboard Shortcuts

Enhanced terminal experience with powerful shortcuts.

### Basic Navigation
- **Ctrl+Space** - Trigger auto-completion
- **Ctrl+L** - Clear screen but keep current command
- **Ctrl+D** - Exit Prometheus
- **Ctrl+C** - Cancel current input

### Command Editing
- **Ctrl+X Ctrl+E** - Open current command in $EDITOR
- **Alt+E** - Explain the last command
- **Ctrl+R** - Search command history (fuzzy search)

### Help & Information
- **Alt+H** - Show keyboard shortcuts quick reference

### Example Workflow
```
1. Type: list files
2. Press Ctrl+X Ctrl+E to edit in nano/vim
3. Make changes, save, exit
4. Command executes with your edits
```

---

## Smart History

Bash-style history with AI enhancements.

### Bang Commands
```bash
# Repeat last command
!!

# Repeat command n ago
!-2   # 2 commands ago
!-5   # 5 commands ago

# Repeat specific command by index
!10   # Command at index 10

# Repeat last command starting with...
!git  # Last git command
!ls   # Last ls command
```

### History Statistics
```bash
# Show usage statistics
stats

# View recent commands
history
history 20

# Clear history
clear-history
```

### Statistics Include
- Total commands executed
- Success/failure rate
- Most used commands
- Usage patterns by time

---

## Search & Navigation

Fast file and code navigation.

### File Search
```bash
# Fuzzy find files
find main
find config.json
find *.py

# Results show up to 50 matches
```

### Content Search
```bash
# Search in files (smart grep)
grep "function_name"
grep "TODO"
grep "import"

# Uses ripgrep if available, falls back to grep
```

### Code Search
```bash
# Find functions/classes in codebase
search MyClass
search handle_request
search UserModel

# Searches common code file extensions
# .py, .js, .java, .cpp, .go, .rs, etc.
```

### Project Analysis
```bash
# Analyze current directory
analyze

# Shows:
# - Project type (Git, Python, Node.js, Docker)
# - File counts by extension
# - Total size
# - Git info (if applicable)
```

---

## Context Awareness

Prometheus understands your project and suggests relevant commands.

### Quick Status
```bash
# Show context-aware status
status

# Displays:
# - Current directory
# - Git status (if in repo)
# - Python environment (if Python project)
# - Node.js version (if Node project)
# - Docker containers (if Docker project)
```

### Context Reference
```bash
# Show relevant commands for current directory
ref
reference

# Examples:
# - Git repo → shows git commands
# - Python project → shows pip, pytest, etc.
# - Node.js project → shows npm commands
# - Docker project → shows docker commands
```

### Auto-Detection
Prometheus automatically detects:
- ✅ Git repositories
- ✅ Python projects (requirements.txt, setup.py)
- ✅ Node.js projects (package.json)
- ✅ Rust projects (Cargo.toml)
- ✅ Go projects (go.mod)
- ✅ Docker projects (Dockerfile, docker-compose.yml)
- ✅ Makefiles

---

## Plugin System

Extend Prometheus with custom functionality.

### List Plugins
```bash
plugin list
```

### Create Plugin
```bash
# Create a plugin template
plugin create my-plugin

# Opens ~/.prometheus/plugins/my-plugin.py
```

### Plugin Template
```python
from core.plugins import Plugin

class PrometheusPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "My Plugin"
        self.version = "1.0.0"
        self.description = "Custom functionality"
        self.author = "Your Name"
    
    def initialize(self):
        # Register commands
        self.register_command("mycommand", self.handle_mycommand)
    
    def handle_mycommand(self, args):
        print(f"My command executed with: {args}")
```

### Install/Uninstall
```bash
# Install plugin (from file or URL)
plugin install git-helper

# Uninstall plugin
plugin uninstall git-helper
```

---

## Command-Line Flags

One-shot execution without entering interactive mode.

### Quick Actions
```bash
# Shorten URL
prom --shorten "https://long-url.com"

# Generate QR code
prom --qr "Hello World"

# Hash text
prom --hash "my secret"

# Encode/decode
prom --encode base64 "text"

# World time
prom --time "Tokyo"
```

### Error Recovery
```bash
# Fix last failed command
prom --fix

# Explains last command
prom --explain
```

### Natural Language
```bash
# One-shot queries
prom "list my files"
prom "show disk usage"
prom "find python files"
```

### System Commands
```bash
# Update Prometheus
prom update

# Show info
prom info

# Manage config
prom config show
prom config edit
prom config reset

# Manage history
prom history
prom history clear
prom history export
```

---

## Advanced Usage Examples

### Workflow 1: Quick Status Check
```bash
prom status              # Check current context
prom ref                 # See relevant commands
prom "git status"        # Execute suggested command
```

### Workflow 2: Code Search & Edit
```bash
prom find "config"       # Find config files
prom search "UserModel"  # Find in code
prom "edit user.py"      # Open in editor
```

### Workflow 3: Error Recovery
```bash
prom "install docker"    # Command fails
prom --fix              # AI suggests fix
# Executes: sudo apt-get install -y docker.io
```

### Workflow 4: History Navigation
```bash
prom stats              # See most used commands
prom !!                 # Repeat last
prom !git               # Repeat last git command
```

---

## Tips & Tricks

### 1. Command Aliases
Add to your `.bashrc` or `.zshrc`:
```bash
alias p='prom'
alias pf='prom --fix'
alias pe='prom --explain'
```

### 2. Quick Reference
Keep this in terminal:
```bash
# Always-on context
prom status

# Quick command lookup
prom ref
```

### 3. Dry-Run Mode
Test commands safely:
```bash
prom dry-run on
prom "delete old logs"  # Shows command, doesn't execute
prom dry-run off
```

### 4. Custom Plugins
Create project-specific commands:
```bash
prom plugin create deploy
# Edit plugin to add deployment logic
# Use: deploy production
```

---

## Keyboard Cheat Sheet

```
╔════════════════════════════════════════════════╗
║          PROMETHEUS KEYBOARD SHORTCUTS         ║
╠════════════════════════════════════════════════╣
║ Ctrl+Space      │ Auto-complete               ║
║ Ctrl+X Ctrl+E   │ Edit in $EDITOR             ║
║ Alt+E           │ Explain last command        ║
║ Ctrl+L          │ Clear screen                ║
║ Alt+H           │ Show shortcuts              ║
║ Ctrl+R          │ Search history              ║
║ Ctrl+D          │ Exit                        ║
║ Ctrl+C          │ Cancel                      ║
╚════════════════════════════════════════════════╝
```

---

## Quick Command Reference

```
╔════════════════════════════════════════════════╗
║         PROMETHEUS QUICK COMMANDS              ║
╠════════════════════════════════════════════════╣
║ status          │ Show context status         ║
║ ref             │ Context commands            ║
║ stats           │ History statistics          ║
║ analyze         │ Analyze project             ║
║ find <pattern>  │ Find files                  ║
║ grep <pattern>  │ Search in files             ║
║ search <name>   │ Find in codebase            ║
║ !!              │ Repeat last command         ║
║ !git            │ Repeat last git command     ║
║ plugin list     │ List plugins                ║
╚════════════════════════════════════════════════╝
```

---

## Performance Tips

1. **Use Context Commands** - `status` and `ref` are instant
2. **Limit Search Scope** - Use specific patterns in `find` and `grep`
3. **Cache History** - `stats` pre-calculates common patterns
4. **Plugin Loading** - Only installed plugins are loaded

---

## Troubleshooting

### QR Codes Not Displaying
```bash
# Install dependencies
pip install pyqrcode pypng
```

### Keyboard Shortcuts Not Working
- Check terminal emulator supports key bindings
- Try alternative shortcuts (e.g., Esc+E instead of Alt+E)

### Plugins Not Loading
```bash
# Check plugin directory
ls ~/.prometheus/plugins/

# Check plugin syntax
python -m py_compile ~/.prometheus/plugins/myplugin.py
```

---

**Need more help?** Type `help` in Prometheus or visit the [GitHub repository](https://github.com/roywalk3r/prometheus).
