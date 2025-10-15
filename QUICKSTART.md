# Kai Quick Start Guide

Get up and running with Kai in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed

## Installation

### 1. Install Ollama

```bash
# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# macOS
brew install ollama

# Or download from https://ollama.ai/
```

### 2. Pull the AI Model

```bash
ollama pull llama3
```

### 3. Install Kai

```bash
# Clone or navigate to the Kai directory
cd kai

# Run the installation script
chmod +x install.sh
./install.sh

# Or install manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## First Run

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start Kai
python main.py
```

You should see the Kai banner:

```
╔═══════════════════════════════════════╗
║   🤖 Kai - Terminal Assistant         ║
║   Type 'help' for commands            ║
║   Type 'exit' to quit                 ║
╚═══════════════════════════════════════╝
```

## Try These Commands

### File Operations
```
> list my files
> create a file called test.txt with "Hello World"
> show contents of test.txt
> find all python files
```

### System Information
```
> show disk usage
> what's my IP address
> show system information
```

### Get Help
```
> help              # Show all commands
> examples          # Show example commands
> history           # Show command history
```

## Configuration

Kai stores its configuration in `~/.kai/config.json`. You can modify settings:

```
> config                           # Show current config
> config set timeout_seconds 30    # Set timeout to 30 seconds
> dry-run on                       # Enable preview mode
```

## Safety Features

Kai will warn you before running dangerous commands:

```
> delete all files
⚠️ DANGER: This command contains 'rm -rf' which could be destructive!
Are you SURE you want to run this? [y/N]:
```

## Tips

1. **Use dry-run mode** to preview commands:
   ```
   > dry-run on
   > delete old_file.txt
   $ rm old_file.txt
   Dry-run mode: Command not executed
   ```

2. **Context awareness** - Kai remembers recent commands:
   ```
   > create a file called notes.txt
   > add "Hello" to it
   > show it
   ```

3. **View history** to replay commands:
   ```
   > history 5
   ```

4. **Get suggestions** for common tasks:
   ```
   > examples
   ```

## Troubleshooting

### "Ollama not found"
Make sure Ollama is installed and in your PATH:
```bash
which ollama
ollama --version
```

### "Model not found"
Pull the llama3 model:
```bash
ollama pull llama3
```

### "Command timeout"
Increase the timeout in config:
```
> config set timeout_seconds 60
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Explore more examples with `> examples`

## Creating an Alias

Add this to your `~/.bashrc` or `~/.zshrc` for easy access:

```bash
alias kai='cd /path/to/kai && source .venv/bin/activate && python main.py'
```

Then just type `kai` from anywhere to start!

---

**Need help?** Type `help` in Kai or open an issue on GitHub.
