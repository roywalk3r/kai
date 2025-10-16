# Prometheus - Intelligent Terminal Assistant 🔥

Prometheus is an AI-powered terminal assistant that translates natural language into shell commands and executes them safely. It uses AI (Google Gemini or local Ollama) to understand your intent and help you navigate the command line with ease.

**Note:** During installation, you can set a custom alias (default: `prom`) so you don't have to type "prometheus" every time!

## Features

### Core Features
✨ **Natural Language to Commands**: Describe what you want in plain English
🛡️ **Safety First**: Warns about dangerous or long-running commands
⚡ **Smart Execution**: Auto-timeout for runaway processes
📝 **Command History**: Track and replay previous commands with bash-style `!!` and `!n`
🎨 **Beautiful UI**: Rich terminal interface with colors and formatting
🔧 **Configurable**: Customize behavior via config file
💡 **Context Aware**: Auto-detects Git, Python, Node.js, Docker projects
🔍 **Dry Run Mode**: Preview commands before execution
📚 **Command Suggestions**: Get help with common tasks

### Terminal-First Enhancements
⚡ **Quick Actions**: URL shortener, QR codes, hashing, encoding, world clock
⌨️ **Keyboard Shortcuts**: Edit in $EDITOR (Ctrl+X Ctrl+E), explain last (Alt+E), and more
🔍 **Smart Search**: Fuzzy file search, smart grep, codebase search
📊 **History Analytics**: Usage statistics, most-used commands, success rates
🎯 **Context Commands**: Project-aware suggestions (Git, Python, Node.js, Docker)
🔌 **Plugin System**: Extend functionality with custom plugins
🛠️ **Error Recovery**: AI-powered fix suggestions with `--fix` flag

## Installation

### Quick Install (Recommended)

**System-wide installation with automatic setup:**

```bash
git clone https://github.com/roywalk3r/prometheus.git
cd prometheus
sudo bash system-install.sh
```

During installation, you'll:
1. Be prompted to set a command alias (default: `prom`)
2. Choose your AI model (Gemini or Ollama)
3. Set up your Gemini API key (if using Gemini)

After installation, just type your alias:
```bash
prom "list my files"
```

### Prerequisites

- Python 3.8+
- **Either:**
  - **Google Gemini API Key** (Recommended - Free, Fast) - [Get it here](https://aistudio.google.com/apikey)
  - **OR** [Ollama](https://ollama.ai/) with llama3 model (Local, Private)

### Manual Setup (Development)

1. Clone the repository:
```bash
git clone https://github.com/roywalk3r/prometheus.git
cd prometheus
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up AI model (see [GEMINI_SETUP.md](GEMINI_SETUP.md) for details)

## Usage

### Quick Commands (One-Shot Mode)

Execute commands directly:
```bash
prom "list my files"
prom "update my system"
prom "show disk usage"
prom "find all python files"
```

### Interactive Mode

Start an interactive session:
```bash
prom
```

Then interact naturally:
```
> list my files
> create a file called notes.txt with "Hello World"
> show me disk usage
> find all python files in this directory
```

### Special Commands

**Basic Commands:**
- `exit` or `quit` - Exit Prometheus
- `terminate` - Stop currently running command
- `help` - Show comprehensive help
- `config` - Show/edit configuration

**Quick Actions:**
- `--qr "text"` - Generate QR code
- `--hash "text"` - Generate hash (MD5, SHA1, SHA256, SHA512)
- `--time "Tokyo"` - Show world time
- `--encode base64 "text"` - Encode text
- `--calc "2+2"` - Calculate expressions

**Search & Navigation:**
- `find <pattern>` - Fuzzy file search
- `grep <pattern>` - Search in files
- `search <name>` - Find in codebase
- `analyze` - Analyze project

**Context Commands:**
- `status` - Show quick directory status
- `ref` - Show context-relevant commands
- `stats` - Show history statistics

**History Commands:**
- `history` - Show command history
- `!!` - Repeat last command
- `!n` - Repeat command at index n
- `!git` - Repeat last git command

**Plugin System:**
- `plugin list` - List installed plugins
- `plugin create <name>` - Create plugin template

### Subcommands

**System Management:**
- `prom update` - Update to latest version
- `prom uninstall` - Uninstall from system
- `prom info` - Show system information
- `prom --version` - Show version

**Configuration:**
- `prom config show` - Show current config
- `prom config edit` - Edit config file
- `prom config reset` - Reset to defaults

**History Management:**
- `prom history` - Show command history
- `prom history clear` - Clear history
- `prom history export` - Export history

**Quick Actions (CLI):**
- `prom --fix` - Fix last failed command
- `prom --explain` - Explain last command
- `prom --qr "text"` - Generate QR code
- `prom --hash "text"` - Generate hash
- `prom --time "location"` - Show world time

### Configuration

Edit `~/.prometheus/config.json` to customize:

```json
{
  "timeout_seconds": 20,
  "default_model": "llama3",
  "auto_confirm_safe": false,
  "history_size": 100,
  "color_scheme": "default"
}
```

## Examples

### File Operations
```
> create a backup of my documents folder
> find all files larger than 100MB
> compress the logs directory
```

### System Information
```
> show me system resources
> what's my IP address
> check disk space
```

### Development Tasks
```
> find all TODO comments in python files
> count lines of code in this project
> show git status
```

## Safety Features

Prometheus includes multiple safety mechanisms:

1. **Dangerous Command Detection**: Warns before running potentially destructive commands
2. **Long-Running Detection**: Alerts for commands that might take a long time
3. **Intelligent Timeouts**: Auto-adjusts timeout based on command type
4. **Confirmation Prompts**: Requires explicit confirmation for risky operations
5. **Dry-Run Mode**: Preview commands without executing them
6. **Command Sanitization**: Auto-optimizes commands for script compatibility

## Architecture

```
prometheus/
├── main.py              # Entry point and main loop
├── ai/
│   ├── model.py        # AI model interface (Gemini + Ollama)
│   ├── gemini_model.py # Google Gemini integration
│   └── context.py      # Context management for better AI responses
├── core/
│   ├── executor.py     # Command execution engine
│   ├── history.py      # Command history management
│   ├── config.py       # Configuration management
│   └── plugins.py      # Plugin system (NEW)
└── utils/
    ├── safety.py           # Safety checks and validation
    ├── command_classifier.py  # Intelligent timeout classification
    ├── command_sanitizer.py   # Command optimization
    ├── ui.py               # UI helpers and formatting
    ├── quick_actions.py    # Quick utilities (NEW)
    ├── search.py           # Search & navigation (NEW)
    ├── keyboard.py         # Keyboard shortcuts (NEW)
    ├── smart_history.py    # Enhanced history (NEW)
    └── context_commands.py # Context awareness (NEW)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

Repository: https://github.com/roywalk3r/prometheus

## License

MIT License - See LICENSE file for details

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
systemctl restart ollama  # Linux
```

### Model Not Found
```bash
# Pull the required model
ollama pull llama3
```

### Permission Errors
Make sure you have appropriate permissions for the commands you're trying to run.

## Roadmap

**Completed:**
- [x] Plugin system for custom commands ✅
- [x] Command explanation mode ✅
- [x] Keyboard shortcuts ✅
- [x] Enhanced search capabilities ✅
- [x] Context-aware suggestions ✅

**Planned:**
- [ ] Support for multiple LLM backends (OpenAI, Anthropic, etc.)
- [ ] Multi-language support
- [ ] Web interface
- [ ] Command chaining with pipes
- [ ] Cloud sync for history and config
- [ ] VS Code extension

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [TERMINAL_FEATURES.md](TERMINAL_FEATURES.md) - Complete feature guide
- [GEMINI_SETUP.md](GEMINI_SETUP.md) - Gemini API setup
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Technical details

## Credits

Built with:
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive CLI
- [PyQRCode](https://github.com/mnooner256/pyqrcode) - QR code generation
- [pytz](https://pythonhosted.org/pytz/) - Timezone support
