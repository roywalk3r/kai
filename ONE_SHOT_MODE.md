# Kai One-Shot Mode

## 🚀 Quick Command Execution

No need to enter interactive mode! Execute commands directly from your shell.

---

## 📋 Usage

### Basic Syntax
```bash
kai "your natural language query"
```

### Examples

#### File Operations
```bash
kai "list my files"
kai "show hidden files"
kai "create a file called notes.txt"
kai "find all python files"
```

#### System Information
```bash
kai "show disk usage"
kai "check memory usage"
kai "what's my IP address"
kai "show system info"
```

#### System Updates
```bash
kai "update my system"
kai "upgrade all packages"
kai "install docker"
```

#### File Management
```bash
kai "create a backup of my documents"
kai "compress the logs folder"
kai "find large files"
kai "delete old log files"
```

#### Network Operations
```bash
kai "download https://example.com/file.zip"
kai "check if port 8080 is open"
kai "show active connections"
```

#### Development
```bash
kai "build the project"
kai "run tests"
kai "install dependencies"
kai "start the server"
```

---

## 🎯 Comparison: Interactive vs One-Shot

### Interactive Mode
```bash
$ kai
╔═══════════════════════════════════╗
║ Welcome to Kai!                   ║
╚═══════════════════════════════════╝

kai ❯ list my files
╔═══════════════════════════════════╗
║ ⚡ Executing                      ║
║ ls -lah                           ║
╚═══════════════════════════════════╝
...

kai ❯ show disk usage
...

kai ❯ exit
```

### One-Shot Mode (NEW!)
```bash
$ kai "list my files"
╔═══════════════════════════════════╗
║ Query                             ║
║ 💬 list my files                  ║
╚═══════════════════════════════════╝

╔═══════════════════════════════════╗
║ ⚡ Executing                      ║
║ ls -lah                           ║
╚═══════════════════════════════════╝
...

$ kai "show disk usage"
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
kai "update my system" --dry-run
```

### In Scripts
```bash
#!/bin/bash
# Automated backup script

kai "create a backup of /var/www"
if [ $? -eq 0 ]; then
    echo "Backup successful!"
    kai "compress the backup folder"
else
    echo "Backup failed!"
    exit 1
fi
```

### Chaining Commands
```bash
# Run multiple one-shot commands
kai "list my files" && kai "show disk usage"

# Conditional execution
kai "find python files" || echo "No Python files found"

# Capture output
FILES=$(kai "list my files")
echo "Found: $FILES"
```

### With Pipes
```bash
# Use kai output in pipes
kai "list my files" | grep ".py"

# Process kai output
kai "show system info" | tee system-report.txt
```

---

## 💡 Tips & Tricks

### 1. Alias for Common Tasks
```bash
# Add to ~/.bashrc or ~/.zshrc
alias kls='kai "list my files"'
alias kdu='kai "show disk usage"'
alias kupdate='kai "update my system"'
```

### 2. Function Wrappers
```bash
# Smart backup function
backup() {
    kai "create a backup of $1"
}

# Usage
backup ~/documents
```

### 3. Cron Jobs
```bash
# Add to crontab
0 2 * * * /usr/local/bin/kai "backup important files" >> /var/log/backup.log 2>&1
```

### 4. Error Handling
```bash
if kai "update my system"; then
    echo "✓ System updated"
    kai "clean package cache"
else
    echo "✗ Update failed"
    exit 1
fi
```

---

## 🎨 Output Modes

### Normal Output
```bash
kai "list my files"
# Shows full UI with panels
```

### Quiet Mode (Coming Soon)
```bash
kai "list my files" --quiet
# Shows only command output
```

### JSON Mode (Coming Soon)
```bash
kai "list my files" --json
# Returns structured JSON
```

---

## 🔐 Safety Features

### Dangerous Commands
One-shot mode has the same safety features as interactive mode:

```bash
$ kai "delete all files"
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
kai "show disk usage"
kai "check memory"
kai "list running processes"
```

### 2. Automated Tasks
```bash
# Daily backup script
kai "backup /home/user/documents to /backup"
kai "compress /backup"
kai "delete backups older than 30 days"
```

### 3. Development Workflow
```bash
kai "install dependencies"
kai "run tests"
kai "build for production"
kai "deploy to server"
```

### 4. System Maintenance
```bash
kai "update my system"
kai "clean package cache"
kai "remove old kernels"
kai "check for errors in logs"
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
kai "list all files"
kai "find files modified today"
kai "show file sizes"
kai "count files in directory"
```

### Text Processing
```bash
kai "search for 'error' in logs"
kai "replace 'old' with 'new' in file.txt"
kai "count lines in file.txt"
kai "show first 10 lines of file.txt"
```

### Network
```bash
kai "check internet connection"
kai "show my public IP"
kai "test connection to google.com"
kai "download file from URL"
```

### System
```bash
kai "show system uptime"
kai "list installed packages"
kai "check disk health"
kai "show CPU usage"
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

**One-shot mode makes Kai even more powerful and flexible!** 🎉

Try it now:
```bash
kai "show me something cool"
```
