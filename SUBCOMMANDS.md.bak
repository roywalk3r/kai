# Kai Subcommands Guide

## 🎯 Available Subcommands

Kai now supports powerful subcommands for managing the application!

---

## 📋 Command Reference

### `kai update`
Update Kai to the latest version from git.

```bash
kai update
```

**What it does:**
- Pulls latest code from git repository
- Updates Python dependencies
- Preserves your configuration

**Example:**
```bash
$ kai update
╔═══════════════════════════════════╗
║ Updating Kai...                   ║
╚═══════════════════════════════════╝
✓ Updated from git
Already up to date.
✓ Dependencies updated
✅ Kai updated successfully!
```

---

### `kai uninstall`
Uninstall Kai from your system.

```bash
kai uninstall
```

**What it does:**
- Removes Kai installation
- Removes executable from PATH
- Preserves ~/.kai configuration (optional)

**Example:**
```bash
$ kai uninstall
╔═══════════════════════════════════╗
║ ⚠️  Uninstalling Kai              ║
║                                   ║
║ This will remove Kai from your    ║
║ system.                           ║
║ Your configuration in ~/.kai will ║
║ be preserved.                     ║
╚═══════════════════════════════════╝
Are you sure? [y/N]:
```

---

### `kai config`
Manage Kai configuration.

#### Show Configuration
```bash
kai config
kai config show
```

**Output:**
```
╔═══════════════════════════════════╗
║ Configuration                     ║
║                                   ║
║ Configuration File:               ║
║ ~/.kai/config.json                ║
║                                   ║
║ Commands:                         ║
║ kai config show   - Show config   ║
║ kai config edit   - Edit config   ║
║ kai config reset  - Reset defaults║
╚═══════════════════════════════════╝
```

#### Edit Configuration
```bash
kai config edit
```

Opens config file in your default editor ($EDITOR or nano).

#### Reset Configuration
```bash
kai config reset
```

Resets all settings to defaults.

**Example:**
```bash
$ kai config show
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Setting           ┃ Value         ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ timeout_seconds   │ 20            │
│ default_model     │ llama3        │
│ use_gemini        │ true          │
│ dry_run           │ false         │
│ history_size      │ 100           │
└───────────────────┴───────────────┘
```

---

### `kai history`
Manage command history.

#### Show History
```bash
kai history
```

Shows last 20 commands from history.

**Example:**
```bash
$ kai history
┏━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ # ┃ Query              ┃ Command        ┃ Success┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1 │ list my files      │ ls -lah        │ ✓      │
│ 2 │ show disk usage    │ df -h          │ ✓      │
│ 3 │ create test file   │ touch test.txt │ ✓      │
└───┴────────────────────┴────────────────┴────────┘
```

#### Clear History
```bash
kai history clear
```

Clears all command history.

#### Export History
```bash
kai history export [filename]
```

Exports history to JSON file.

**Example:**
```bash
$ kai history export my_commands.json
✓ History exported to my_commands.json
```

---

### `kai info`
Show system information.

```bash
kai info
```

**Example:**
```bash
$ kai info
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Version           │ 1.0.0                       │
│ Install Location  │ ~/.local/share/kai          │
│ Config Directory  │ ~/.kai                      │
│ Python Version    │ 3.13.7                      │
│ Platform          │ Linux-6.1.0-kali9-amd64     │
│ AI Model          │ Gemini (Google)             │
└───────────────────┴─────────────────────────────┘
```

---

## 🎓 Usage Examples

### Update Workflow
```bash
# Check current version
kai --version

# Update to latest
kai update

# Verify update
kai info
```

### Configuration Management
```bash
# View current config
kai config show

# Edit config
kai config edit

# Reset if needed
kai config reset
```

### History Management
```bash
# View recent commands
kai history

# Export for backup
kai history export backup.json

# Clear old history
kai history clear
```

### System Maintenance
```bash
# Check system info
kai info

# Update Kai
kai update

# Uninstall if needed
kai uninstall
```

---

## 🔧 Advanced Usage

### Combining with Other Commands

```bash
# Update and restart
kai update && kai

# Show config and edit
kai config show && kai config edit

# Export history with timestamp
kai history export "history_$(date +%Y%m%d).json"
```

### Scripting

```bash
#!/bin/bash
# Auto-update script

echo "Updating Kai..."
kai update

if [ $? -eq 0 ]; then
    echo "Update successful!"
    kai info
else
    echo "Update failed!"
    exit 1
fi
```

---

## 💡 Tips

### 1. Regular Updates
```bash
# Add to crontab for weekly updates
0 0 * * 0 kai update
```

### 2. Backup Configuration
```bash
# Before reset
cp ~/.kai/config.json ~/.kai/config.backup.json
kai config reset
```

### 3. Export History Regularly
```bash
# Monthly backup
kai history export "history_$(date +%Y%m).json"
```

### 4. Check Info After Install
```bash
# Verify installation
kai info
```

---

## 🎯 Quick Reference

| Command | Description |
|---------|-------------|
| `kai` | Start interactive mode |
| `kai update` | Update to latest version |
| `kai uninstall` | Remove Kai |
| `kai config` | Show config options |
| `kai config show` | Display configuration |
| `kai config edit` | Edit config file |
| `kai config reset` | Reset to defaults |
| `kai history` | Show command history |
| `kai history clear` | Clear history |
| `kai history export` | Export history |
| `kai info` | Show system info |
| `kai --version` | Show version |
| `kai --help` | Show help |

---

## 🚀 Coming Soon

Future subcommands:
- `kai plugin` - Manage plugins
- `kai theme` - Change color themes
- `kai backup` - Backup/restore config
- `kai doctor` - Diagnose issues
- `kai stats` - Usage statistics

---

**Manage Kai like a pro!** 🎉
