# 🚀 Prometheus Advanced Features Guide

Complete guide to all Phase 2 & 3 advanced features.

---

## 📋 Table of Contents

1. [Alias System](#alias-system)
2. [Response Caching](#response-caching)
3. [Health Check](#health-check)
4. [Template System](#template-system)
5. [Workflow Automation](#workflow-automation)
6. [Remote Execution](#remote-execution)
7. [Session Memory](#session-memory)
8. [Interactive History](#interactive-history)
9. [Command Chaining](#command-chaining)
10. [Enhanced Error Recovery](#enhanced-error-recovery)

---

## 🔖 Alias System

Create custom shortcuts for frequently used commands.

### Commands

```bash
# List all aliases
prom
> alias

# Add an alias
> alias add gs git status
> alias add deploy ./deploy.sh
> alias add ll ls -alh

# Use an alias
> gs
# Expands to: git status

# Remove an alias
> alias remove gs

# Import from shell
> alias import
# Imports from ~/.bashrc or ~/.zshrc
```

### Built-in Aliases

- **Git:** `gs`, `ga`, `gc`, `gp`, `gl`, `gd`, `gco`, `gb`, `glog`
- **Docker:** `dp`, `dpa`, `di`, `dex`, `dlog`, `dstop`, `drm`
- **System:** `ll`, `la`, `ports`, `psg`, `myip`, `cpu`, `mem`, `disk`
- **Python:** `py`, `pip`, `venv`, `pyserver`

### Examples

```bash
# Create deployment alias
> alias add deploy "git pull && npm install && npm run build"

# Use it
> deploy
→ git pull && npm install && npm run build

# Create complex alias
> alias add backup "tar -czf backup_$(date +%Y%m%d).tar.gz documents/"
```

---

## ⚡ Response Caching

10x faster responses for repeated queries.

### Features

- **Automatic Caching**: AI responses cached by query + context
- **TTL**: 60-minute default expiration
- **Context-Aware**: Different cache per directory
- **Smart**: Avoids caching time-sensitive queries

### Commands

```bash
# View cache statistics
> cache stats

# Output:
# ┌─ Cache Statistics ─┐
# │ Cache Hits:    15   │
# │ Cache Misses:  5    │
# │ Hit Rate:      75%  │
# │ Cached Entries: 12  │
# └──────────────────────┘

# Clear cache
> cache clear

# Clean expired entries
> cache clean
```

###Benefits

```bash
# First query (miss)
> list files sorted by size
⏱️  Response time: 1.2s

# Second identical query (hit)
> list files sorted by size
⚡ (cached response)
⏱️  Response time: 0.01s  # 120x faster!
```

---

## 🏥 Health Check

Comprehensive system diagnostics.

### Command

```bash
> doctor

# Output:
┌─ Prometheus Health Check ─┐
│ Check               Status │
├────────────────────────────┤
│ Python Version       ✓     │
│ Dependencies         ✓     │
│ Configuration        ✓     │
│ History              ✓     │
│ AI Backend           ✓     │
│ Ollama               ✓     │
│ Git                  ✓     │
│ Disk Space           ⚠     │
│ Memory               ✓     │
│ Network              ✓     │
└────────────────────────────┘

# Recommendations:
1. Free up disk space (only 2GB free)
```

### Checks

- ✅ Python 3.8+ installed
- ✅ All dependencies present
- ✅ Valid configuration file
- ✅ API keys configured
- ✅ Ollama available
- ✅ Git installed
- ✅ Sufficient disk space (>5GB)
- ✅ Adequate memory (>1GB)
- ✅ Network connectivity
- ✅ Shell integration
- ✅ Terminal capabilities

---

## 📝 Template System

Save and reuse command sequences.

### Built-in Templates

| Template | Description | Parameters |
|----------|-------------|------------|
| `backup` | Backup directory | `source_dir`, `backup_name` |
| `git-workflow` | Git add, commit, push | `message`, `branch` |
| `python-project` | Init Python project | `project_name`, `packages` |
| `docker-cleanup` | Clean Docker resources | None |
| `web-server` | Start HTTP server | `port` |
| `find-large-files` | Find large files | `directory`, `size`, `limit` |
| `system-info` | System information | None |

### Commands

```bash
# List templates
> template list

# Show template details
> template show backup

# Use a template
> template use backup source_dir=~/documents backup_name=docs_backup

# Creates command:
# tar -czf docs_backup_20251017.tar.gz ~/documents/
```

### Create Custom Template

```bash
# Create workflow template
> template create deploy

# Edit ~/.prometheus/templates.json
{
  "deploy": {
    "name": "deploy",
    "description": "Deploy application",
    "commands": [
      "git pull origin ${branch}",
      "npm install",
      "npm run build",
      "pm2 restart ${app_name}"
    ],
    "parameters": {
      "branch": "Branch to deploy",
      "app_name": "PM2 app name"
    }
  }
}

# Use it
> template use deploy branch=main app_name=my-app
```

---

## 🔄 Workflow Automation

Multi-step command sequences with conditions.

### Built-in Workflows

| Workflow | Steps | Description |
|----------|-------|-------------|
| `deploy` | 4 | Pull, install, test, deploy |
| `backup-project` | 3 | Create backup archive |
| `system-update` | 3 | Update and clean system |
| `docker-rebuild` | 4 | Rebuild Docker containers |

### Commands

```bash
# List workflows
> workflow list

# Show workflow details
> workflow show deploy

# Run workflow
> workflow run deploy

# Output:
# Running workflow 'deploy'...
# ✓ Pull code
# ✓ Install dependencies
# ✓ Run tests
# ✓ Deploy
# ✅ Workflow completed successfully!
```

### Create Workflow (YAML)

Create `~/.prometheus/workflows/my-workflow.yaml`:

```yaml
name: ci-pipeline
description: CI/CD pipeline
category: deployment

variables:
  branch: main
  environment: production

steps:
  - name: Checkout code
    command: git checkout ${branch}
    
  - name: Install dependencies
    command: npm install
    timeout: 600
    
  - name: Run tests
    command: npm test
    condition: always
    retry: 2
    continue_on_error: false
    
  - name: Build
    command: npm run build
    condition: on_success
    
  - name: Deploy
    command: ./deploy.sh ${environment}
    condition: on_success
    timeout: 1800
    
  - name: Rollback on failure
    command: ./rollback.sh
    condition: on_failure
```

Load it:

```bash
> workflow import ~/.prometheus/workflows/my-workflow.yaml
```

### Step Conditions

- `always` - Always execute
- `on_success` - Execute if previous step succeeded
- `on_failure` - Execute if previous step failed

---

## 🌐 Remote Execution

Execute commands on remote servers via SSH.

### Setup

```bash
# Add remote host
> remote add server1 user@hostname.com

# With custom port
> remote add server2 user@hostname.com --port 2222

# With SSH key
> remote add server3 user@hostname.com --key ~/.ssh/id_rsa
```

### Commands

```bash
# List configured hosts
> remote list

# Test connection
> remote test server1

# Execute command
> remote exec server1 "df -h"

# Execute on multiple hosts
> remote exec server1,server2,server3 "uptime"

# Output:
# Executing on 3 hosts...
# ┌─ Execution Results ─┐
# │ Host     │ Status │
# ├──────────┼────────┤
# │ server1  │  ✓     │
# │ server2  │  ✓     │
# │ server3  │  ✗     │
# └───────────────────────┘
```

### Copy Files

```bash
# Copy local file to remote
> remote copy server1 /local/file.txt /remote/path/

# Copy from multiple hosts
> remote download server1 /remote/log.txt ./logs/
```

### Use with Workflows

```yaml
name: deploy-to-production
steps:
  - name: Deploy to server 1
    command: remote exec server1 "./deploy.sh"
    
  - name: Deploy to server 2
    command: remote exec server2 "./deploy.sh"
    condition: on_success
    
  - name: Verify deployment
    command: remote exec server1,server2 "curl localhost:8080/health"
```

---

## 🧠 Session Memory

Context-aware AI that remembers your session.

### Features

- Remembers last 10 query-response exchanges
- Tracks file/path references
- Stores variables
- Maintains command history (last 20)
- Persists between restarts (optional)

### Commands

```bash
# Show session info
> session info

# Output:
# Session ID: 20251017_093000
# Duration: 0:15:32
# Directory: /home/user/projects

# Session Statistics:
# ├─ Exchanges:        25
# ├─ Commands:         18
# ├─ Success Rate:     94%
# ├─ Files Referenced: 8
# └─ Variables Set:    3

# Clear session context
> session clear
```

### Context References

The AI remembers context:

```bash
> find config files
# Found: config.json, config.yaml

> open the second one
# AI knows "the second one" = config.yaml
# Opens: config.yaml

> edit it
# AI knows "it" = config.yaml
# Command: nano config.yaml
```

### Variables

```bash
# Set variable in session
> remember that my-app is the project name
# AI stores: project_name = my-app

# Later...
> deploy my-app
# AI uses stored variable
```

---

## 📊 Interactive History

Rich UI for browsing command history.

### Commands

```bash
# Launch interactive browser
> history ui

# ┌─ Command History Browser ─┐
# │                            │
# │ [✓] 09:15 | git status     │
# │ [✗] 09:16 | npm install    │
# │ [✓] 09:20 | git commit     │
# │                            │
# │ Controls:                  │
# │ ↑↓ Navigate                │
# │ Enter - Run                │
# │ F - Fix Failed             │
# │ E - Explain                │
# │ Q - Quit                   │
# └────────────────────────────┘

# Show only failed commands
> history failed

# Analyze patterns
> history analysis

# Output:
# ┌─ History Analysis ─┐
# │ Total Commands: 247        │
# │ Unique Commands: 45        │
# │ Success Rate: 94%          │
# │ Peak Hour: 15:00           │
# │                            │
# │ Most Used Commands:        │
# │  1. git (45 times)         │
# │  2. ls (32 times)          │
# │  3. cd (28 times)          │
# └────────────────────────────┘
```

### History Table

```bash
# Show recent history
> history

# ┌─ Command History ─┐
# │ #  │ Time  │ Status │ Command          │
# ├────┼───────┼────────┼──────────────────┤
# │ 1  │ 09:15 │   ✓    │ git status       │
# │ 2  │ 09:16 │   ✗    │ npm install      │
# │ 3  │ 09:20 │   ✓    │ git commit -m... │
# └───────────────────────────────────────────┘
```

---

## 🔗 Command Chaining

Combine multiple commands with operators.

### Operators

- `|` - Pipe: Pass output to next command
- `&&` - AND: Run next if previous succeeds
- `||` - OR: Run next if previous fails
- `;` - Sequential: Run next regardless
- `&` - Background: Run in background

### Examples

```bash
# Pipe output
> find config.json | cat
# Finds file, then displays contents

# Conditional execution
> git pull && npm install && npm test
# Each step runs only if previous succeeds

# Error handling
> npm test || echo "Tests failed!"
# Runs echo only if tests fail

# Sequential
> git add . ; git status
# Both run regardless of first result

# Combined
> git pull && npm install || npm ci && npm test
```

### With Natural Language

```bash
> list python files and count them
# AI generates: find . -name "*.py" | wc -l

> compile code and if it works run tests
# AI generates: gcc main.c -o main && ./main && pytest
```

---

## 🔧 Enhanced Error Recovery

AI-powered error analysis and fix suggestions.

### Automatic Analysis

```bash
> tar documents/
# Error: documents: Cannot stat: No such file or directory

# 💡 Suggestions:
#  1. Check if the file path is correct (case-sensitive)
#  2. Use 'find' or 'locate' to find the file
#  3. Verify the file exists: ls -la documents
#  4. Check current directory: pwd
#
# Run 'prom --fix' for AI-powered fix
```

### Error Patterns

The system recognizes common errors:

| Error Type | Detects | Suggests |
|------------|---------|----------|
| File not found | "no such file" | Check path, use find |
| Permission denied | "permission denied" | Use sudo, check permissions |
| Command not found | "command not found" | Install package, check PATH |
| Port in use | "address already in use" | Find process, kill, change port |
| Disk full | "no space left" | Clean cache, remove logs |
| Connection failed | "connection refused" | Check service, firewall |
| Module not found | "no module named" | pip install, check venv |

### AI-Powered Fix

```bash
# Command fails
> install docker
# Error: E: Unable to locate package docker

# Get AI fix
> --fix

# AI suggests:
# Try: sudo apt-get install -y docker.io
# Execute? [y/n]
```

### Error History

```bash
# View error history
> history failed

# Analyze error patterns
> history analysis

# Shows which commands fail most often
```

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Health & Diagnostics
doctor                # System health check
cache stats           # Cache performance
session info          # Session statistics

# Productivity
alias                 # Custom shortcuts
template list         # Reusable workflows
workflow list         # Multi-step automation

# Advanced
remote list           # Remote servers
history ui            # Interactive browser
--fix                 # AI error recovery
```

### Keyboard Shortcuts

- `Ctrl+R` - Search history
- `Ctrl+L` - Clear screen
- `Alt+E` - Explain last command
- `Alt+H` - Show help

### Files & Directories

```
~/.prometheus/
├── aliases.json          # Custom aliases
├── templates.json        # Command templates
├── workflows/            # Workflow definitions
├── remote_hosts.json     # SSH hosts
├── session_context.json  # Session memory
├── cache/                # Response cache
└── plugins/              # Custom plugins
```

---

## 💡 Pro Tips

### 1. Combine Features

```bash
# Create alias for workflow
> alias add deploy "workflow run deploy"

# Use template in workflow
# Define workflow step that uses template

# Cache template results
# Templates are cached automatically
```

### 2. Error Recovery Workflow

```bash
# Try command
> risky command

# If fails, use automatic suggestions
# Suggestions appear automatically

# Or get AI fix
> --fix

# Or check history
> history failed
```

### 3. Remote Deployment

```bash
# Setup once
> remote add prod user@prod-server.com
> workflow create deploy-prod

# Deploy with one command
> workflow run deploy-prod
```

### 4. Session Productivity

```bash
# Start session
> session info

# Work...
> find important files
> edit the third one
> commit changes

# Session remembers context throughout
```

---

## 🔍 Troubleshooting

### Cache Issues

```bash
# Clear if stale
> cache clear

# Check hit rate
> cache stats
# Low hit rate? Queries might be too variable
```

### Remote Connection

```bash
# Test connection
> remote test server1

# Check SSH config
cat ~/.ssh/config

# Verify keys
ssh-add -l
```

### Workflow Failures

```bash
# Check workflow definition
> workflow show my-workflow

# Run with dry-run
> dry-run on
> workflow run my-workflow

# Check logs
> history failed
```

### Session Context

```bash
# Clear if confused
> session clear

# Check what's stored
> session info
```

---

## 📚 Additional Resources

- **Main Features:** [TERMINAL_FEATURES.md](TERMINAL_FEATURES.md)
- **Implementation:** [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
- **Demos:** [NEW_FEATURES_DEMO.md](NEW_FEATURES_DEMO.md)
- **Installation:** [INSTALL_NEW_FEATURES.md](INSTALL_NEW_FEATURES.md)

---

**🔥 Master these features to become a Prometheus power user! 🔥**
