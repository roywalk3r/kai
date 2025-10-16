# Prometheus One-Shot Mode

## 🚀 Quick Command Execution

No need to enter interactive mode! Execute commands directly from your shell.

---

## 📋 Usage

### Basic Syntax
```bash
prometheus "your natural language query"
```

### Examples

#### File Operations
```bash
prometheus "list my files"
prometheus "show hidden files"
prometheus "create a file called notes.txt"
prometheus "find all python files"
```

#### System Information
```bash
prometheus "show disk usage"
prometheus "check memory usage"
prometheus "what's my IP address"
prometheus "show system info"
```

#### System Updates
```bash
prometheus "update my system"
prometheus "upgrade all packages"
prometheus "install docker"
```

#### File Management
```bash
prometheus "create a backup of my documents"
prometheus "compress the logs folder"
prometheus "find large files"
prometheus "delete old log files"
```

#### Network Operations
```bash
prometheus "download https://example.com/file.zip"
prometheus "check if port 8080 is open"
prometheus "show active connections"
```

#### Development
```bash
prometheus "build the project"
prometheus "run tests"
prometheus "install dependencies"
prometheus "start the server"
```

---

## 🎯 Comparison: Interactive vs One-Shot

### Interactive Mode
```bash
$ prometheus
╔═══════════════════════════════════╗
║ Welcome to Prometheus!                   ║
╚═══════════════════════════════════╝

prometheus ❯ list my files
╔═══════════════════════════════════╗
║ ⚡ Executing                      ║
║ ls -lah                           ║
╚═══════════════════════════════════╝
...

prometheus ❯ show disk usage
...

prometheus ❯ exit
```

### One-Shot Mode (NEW!)
```bash
$ prometheus "list my files"
╔═══════════════════════════════════╗
║ Query                             ║
║ 💬 list my files                  ║
╚═══════════════════════════════════╝

╔═══════════════════════════════════╗
║ ⚡ Executing                      ║
║ ls -lah                           ║
╚═══════════════════════════════════╝
...

$ prometheus "show disk usage"
...
```

**Benefits:**
- ✅ Faster - No interactive session
- ✅ Scriptable - Use in shell scripts
- ✅ Chainable - Combine with other commands
- ✅ Exit codes - Proper success/failure codes

---

## 🔧 Advanced Usage

### With Dry-Run
Preview what will be executed:
```bash
prometheus "update my system" --dry-run
```

### In Scripts
```bash
#!/bin/bash
# Automated backup script

prometheus "create a backup of /var/www"
if [ $? -eq 0 ]; then
    echo "Backup successful!"
    prometheus "compress the backup folder"
else
    echo "Backup failed!"
    exit 1
fi
```

### Chaining Commands
```bash
# Run multiple one-shot commands
prometheus "list my files" && prometheus "show disk usage"

# Conditional execution
prometheus "find python files" || echo "No Python files found"

# Capture output
FILES=$(prometheus "list my files")
echo "Found: $FILES"
```

### With Pipes
```bash
# Use prometheus output in pipes
prometheus "list my files" | grep ".py"

# Process prometheus output
prometheus "show system info" | tee system-report.txt
```

---

## 💡 Tips & Tricks

### 1. Alias for Common Tasks
```bash
# Add to ~/.bashrc or ~/.zshrc
alias kls='prometheus "list my files"'
alias kdu='prometheus "show disk usage"'
alias kupdate='prometheus "update my system"'
```

### 2. Function Wrappers
```bash
# Smart backup function
backup() {
    prometheus "create a backup of $1"
}

# Usage
backup ~/documents
```

### 3. Cron Jobs
```bash
# Add to crontab
0 2 * * * /usr/local/bin/prometheus "backup important files" >> /var/log/backup.log 2>&1
```

### 4. Error Handling
```bash
if prometheus "update my system"; then
    echo "✓ System updated"
    prometheus "clean package cache"
else
    echo "✗ Update failed"
    exit 1
fi
```

---

## 🎨 Output Modes

### Normal Output
```bash
prometheus "list my files"
# Shows full UI with panels
```

### Quiet Mode (Coming Soon)
```bash
prometheus "list my files" --quiet
# Shows only command output
```

### JSON Mode (Coming Soon)
```bash
prometheus "list my files" --json
# Returns structured JSON
```

---

## 🔐 Safety Features

### Dangerous Commands
One-shot mode has the same safety features as interactive mode:

```bash
$ prometheus "delete all files"
╔═══════════════════════════════════╗
║ ⚠️  Warning                       ║
║ ⚠️  DANGER!                       ║
║                                   ║
║ This command uses 'rm -rf'        ║
║                                   ║
║ This command could be destructive!║
╚═══════════════════════════════════╝
Are you SURE you want to run this? [y/N]:
```

### Confirmation Prompts
- Dangerous commands require confirmation
- Use `--yes` flag to auto-confirm (coming soon)
- Use `--dry-run` to preview safely

---

## 📊 Use Cases

### 1. Quick System Checks
```bash
prometheus "show disk usage"
prometheus "check memory"
prometheus "list running processes"
```

### 2. Automated Tasks
```bash
# Daily backup script
prometheus "backup /home/user/documents to /backup"
prometheus "compress /backup"
prometheus "delete backups older than 30 days"
```

### 3. Development Workflow
```bash
prometheus "install dependencies"
prometheus "run tests"
prometheus "build for production"
prometheus "deploy to server"
```

### 4. System Maintenance
```bash
prometheus "update my system"
prometheus "clean package cache"
prometheus "remove old kernels"
prometheus "check for errors in logs"
```

---

## 🆚 When to Use Each Mode

### Use Interactive Mode When:
- Exploring and experimenting
- Running multiple related commands
- Need conversation context
- Learning new commands

### Use One-Shot Mode When:
- Quick single tasks
- Scripting and automation
- CI/CD pipelines
- Cron jobs
- Command-line workflows

---

## 🚀 Examples by Category

### File Operations
```bash
prometheus "list all files"
prometheus "find files modified today"
prometheus "show file sizes"
prometheus "count files in directory"
```

### Text Processing
```bash
prometheus "search for 'error' in logs"
prometheus "replace 'old' with 'new' in file.txt"
prometheus "count lines in file.txt"
prometheus "show first 10 lines of file.txt"
```

### Network
```bash
prometheus "check internet connection"
prometheus "show my public IP"
prometheus "test connection to google.com"
prometheus "download file from URL"
```

### System
```bash
prometheus "show system uptime"
prometheus "list installed packages"
prometheus "check disk health"
prometheus "show CPU usage"
```

---

## 🎓 Best Practices

1. **Quote your queries** - Always use quotes for multi-word queries
2. **Be specific** - Clear queries get better results
3. **Check first** - Use `--dry-run` for destructive operations
4. **Handle errors** - Check exit codes in scripts
5. **Use aliases** - Create shortcuts for common tasks

---

## 🔮 Coming Soon

- `--yes` flag for auto-confirmation
- `--quiet` mode for minimal output
- `--json` output format
- `--timeout` custom timeout
- Multiple queries in one call

---

**One-shot mode makes Prometheus even more powerful and flexible!** 🎉

Try it now:
```bash
prometheus "show me something cool"
```
