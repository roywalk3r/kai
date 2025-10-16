# Prometheus - Intelligent Terminal Assistant 🔥

Prometheus is an AI-powered terminal assistant that translates natural language into shell commands and executes them safely. It uses AI (Google Gemini or local Ollama) to understand your intent and help you navigate the command line with ease.

**Note:** During installation, you can set a custom alias (default: `prom`) so you don't have to type "prometheus" every time!

## Features

✨ **Natural Language to Commands**: Describe what you want in plain English
🛡️ **Safety First**: Warns about dangerous or long-running commands
⚡ **Smart Execution**: Auto-timeout for runaway processes
📝 **Command History**: Track and replay previous commands
🎨 **Beautiful UI**: Rich terminal interface with colors and formatting
🔧 **Configurable**: Customize behavior via config file
💡 **Context Aware**: Remembers your working directory and environment
🔍 **Dry Run Mode**: Preview commands before execution
📚 **Command Suggestions**: Get help with common tasks

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

- `exit` or `quit` - Exit Prometheus
- `terminate` - Stop currently running command
- `history` - Show command history
- `help` - Show help information
- `config` - Show current configuration

### Subcommands

- `prom update` - Update to latest version
- `prom uninstall` - Uninstall from system
- `prom config` - Manage configuration
- `prom history` - Manage command history
- `prom --version` - Show version

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
│   └── config.py       # Configuration management
└── utils/
    ├── safety.py       # Safety checks and validation
    ├── command_classifier.py  # Intelligent timeout classification
    ├── command_sanitizer.py   # Command optimization
    └── ui.py           # UI helpers and formatting
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

- [ ] Support for multiple LLM backends (OpenAI, Anthropic, etc.)
- [ ] Plugin system for custom commands
- [ ] Command aliasing and shortcuts
- [ ] Multi-language support
- [ ] Web interface
- [ ] Command explanation mode
- [ ] Integration with popular CLI tools

## Credits

Built with:
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Interactive CLI
