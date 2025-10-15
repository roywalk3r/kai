# Kai - Intelligent Terminal Assistant 🤖

Kai is an AI-powered terminal assistant that translates natural language into shell commands and executes them safely. It uses local LLM (via Ollama) to understand your intent and help you navigate the command line with ease.

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

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) with llama3 model installed

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd kai
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and pull the llama3 model:
```bash
# Install Ollama from https://ollama.ai/
ollama pull llama3
```

## Usage

### Basic Usage

Start Kai:
```bash
python main.py
```

Then interact naturally:
```
> list my files
> create a file called notes.txt with "Hello World"
> show me disk usage
> find all python files in this directory
```

### Special Commands

- `exit` or `quit` - Exit Kai
- `terminate` - Stop currently running command
- `history` - Show command history
- `help` - Show help information
- `config` - Show current configuration
- `dry-run on/off` - Toggle dry-run mode

### Configuration

Edit `~/.kai/config.json` to customize:

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

Kai includes multiple safety mechanisms:

1. **Dangerous Command Detection**: Warns before running potentially destructive commands
2. **Long-Running Detection**: Alerts for commands that might take a long time
3. **Auto-Timeout**: Automatically terminates commands after configurable timeout
4. **Confirmation Prompts**: Requires explicit confirmation for risky operations
5. **Dry-Run Mode**: Preview commands without executing them

## Architecture

```
kai/
├── main.py              # Entry point and main loop
├── ai/
│   ├── model.py        # AI model interface and prompt engineering
│   └── context.py      # Context management for better AI responses
├── core/
│   ├── executor.py     # Command execution engine
│   ├── history.py      # Command history management
│   └── config.py       # Configuration management
└── utils/
    ├── safety.py       # Safety checks and validation
    └── ui.py           # UI helpers and formatting
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

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
