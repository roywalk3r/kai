# Prometheus Quick Start Guide

Get up and running with Prometheus in 5 minutes!

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

### 3. Install Prometheus

```bash
# Clone the repository
git clone https://github.com/roywalk3r/prometheus.git
cd prometheus

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

# Start Prometheus
python main.py
```

You should see the Prometheus banner:

```
    🔥 PROMETHEUS 🔥
    ━━━━━━━━━━━━━━━━━━━
    
    ⚡ IGNITE YOUR TERMINAL ⚡
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

Prometheus stores its configuration in `~/.prometheus/config.json`. You can modify settings:

```
> config                           # Show current config
> config set timeout_seconds 30    # Set timeout to 30 seconds
> dry-run on                       # Enable preview mode
```

## Safety Features

Prometheus will warn you before running dangerous commands:

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

2. **Context awareness** - Prometheus remembers recent commands:
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
alias prom='cd /path/to/prometheus && source .venv/bin/activate && python main.py'
```

Then just type `prom` from anywhere to start!

---

**Need help?** Type `help` in Prometheus or open an issue on GitHub.
