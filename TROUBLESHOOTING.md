# Kai Troubleshooting Guide

## Common Issues and Solutions

### AI Not Generating Commands

**Problem**: AI responds with text instead of generating a command

**Example**:
```
> add a welcome text to it
I'm ready to assist you!  ❌ (Should generate: echo "Welcome!" >> file.txt)
```

**Solutions**:
1. **Be more explicit** - Use action verbs clearly:
   ```
   > append "welcome" to test.txt
   > write "hello" to the file
   ```

2. **Restart Kai** - The improved prompts will take effect:
   ```bash
   # Exit and restart
   > exit
   $ python main.py
   ```

3. **Check Ollama** - Ensure the AI model is responding:
   ```bash
   ollama list
   ollama run llama3 "test"
   ```

---

### Wrong Command Generated

**Problem**: AI generates incorrect or case-sensitive commands

**Example**:
```
> remove the hello from test.txt
$ sed -i 's/Hello//g' test.txt  ❌ (Wrong case)
```

**Solutions**:
1. **Be specific about case**:
   ```
   > remove all lines containing "hello" from test.txt
   > replace "hello" with "hi" case-insensitive in test.txt
   ```

2. **Use dry-run to preview**:
   ```
   > dry-run on
   > remove hello from test.txt
   $ sed -i '/hello/d' test.txt  ✓ (Preview before running)
   > dry-run off
   ```

3. **Manually correct** - If you see the wrong command, just type the correct one:
   ```
   > sed -i '/hello/d' test.txt
   ```

---

### File Not Found Errors

**Problem**: Command tries to access non-existent file

**Example**:
```
> what is inside the test file
$ cat output.txt  ❌ (Wrong filename)
cat: output.txt: No such file or directory
```

**Solutions**:
1. **Use exact filenames**:
   ```
   > show contents of test.txt
   > what is inside test.txt
   ```

2. **Check what files exist**:
   ```
   > list files in current directory
   ```

3. **Use context** - Reference previous commands:
   ```
   > create a file called myfile.txt
   > show it  ✓ (Kai remembers "myfile.txt")
   ```

---

### Context Not Working

**Problem**: AI doesn't remember previous commands

**Example**:
```
> create notes.txt
> add text to it  ❌ (Doesn't know what "it" is)
```

**Solutions**:
1. **Check history**:
   ```
   > history
   ```

2. **Be explicit first time**, then use context:
   ```
   > create a file called notes.txt
   > add "hello" to notes.txt  ✓ (Explicit)
   > add "world" to it          ✓ (Now context works)
   ```

3. **Restart if context is lost**:
   ```
   > exit
   $ python main.py
   ```

---

### Command Timeout

**Problem**: Command takes too long and gets killed

**Example**:
```
> find all files in /
⏰ Process killed after 20s timeout.
```

**Solutions**:
1. **Increase timeout**:
   ```
   > config set timeout_seconds 60
   ```

2. **Limit scope**:
   ```
   > find all files in current directory
   > find python files in /home/user
   ```

3. **Use dry-run first**:
   ```
   > dry-run on
   > find all files in /
   $ find / -type f  ✓ (See command before running)
   ```

---

### Dangerous Command Warnings

**Problem**: Kai warns about dangerous commands

**Example**:
```
> delete all files
⚠️ DANGER: This command contains 'rm -rf' which could be destructive!
```

**Solutions**:
1. **This is intentional!** - Kai is protecting you
2. **Review the command** carefully before confirming
3. **Use dry-run** to see what would happen:
   ```
   > dry-run on
   > delete old_file.txt
   ```
4. **Be specific** to avoid false positives:
   ```
   > delete the file named old.txt
   ```

---

### Ollama Connection Issues

**Problem**: Cannot connect to Ollama

**Example**:
```
Ollama not found. Please install Ollama and the llama3 model.
```

**Solutions**:
1. **Check if Ollama is running**:
   ```bash
   ollama list
   ```

2. **Start Ollama** (if needed):
   ```bash
   # Linux
   systemctl start ollama
   
   # Or just run
   ollama serve
   ```

3. **Verify model**:
   ```bash
   ollama pull llama3
   ollama list
   ```

4. **Check configuration**:
   ```
   > config
   # Look for ollama_host setting
   ```

---

### Installation Issues

**Problem**: Dependencies not installing

**Example**:
```
error: externally-managed-environment
```

**Solutions**:
1. **Use virtual environment** (already set up):
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Recreate venv if corrupted**:
   ```bash
   rm -rf .venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run installation script**:
   ```bash
   ./install.sh
   ```

---

### Import Errors

**Problem**: Python import errors when starting

**Example**:
```
ImportError: No module named 'rich'
```

**Solutions**:
1. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   .venv/bin/pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   .venv/bin/python verify.py
   ```

---

### History Not Saving

**Problem**: Command history doesn't persist

**Solutions**:
1. **Check ~/.kai directory**:
   ```bash
   ls -la ~/.kai/
   ```

2. **Check permissions**:
   ```bash
   chmod 755 ~/.kai
   ```

3. **Manually create directory**:
   ```bash
   mkdir -p ~/.kai
   ```

---

### Configuration Not Persisting

**Problem**: Config changes don't save

**Solutions**:
1. **Check config file**:
   ```bash
   cat ~/.kai/config.json
   ```

2. **Set and verify**:
   ```
   > config set timeout_seconds 30
   > config
   # Verify the change is shown
   ```

3. **Check permissions**:
   ```bash
   chmod 644 ~/.kai/config.json
   ```

---

## Performance Issues

### Slow AI Responses

**Problem**: AI takes too long to respond

**Solutions**:
1. **Check Ollama performance**:
   ```bash
   ollama run llama3 "test"
   ```

2. **Use smaller model** (if available):
   ```
   > config set default_model llama3:8b
   ```

3. **Increase timeout**:
   ```
   > config set timeout_seconds 45
   ```

---

## Getting More Help

### Debug Mode

Enable verbose output:
```
> config set log_level DEBUG
```

### Check Logs

View Kai's behavior:
```
> history 20
```

### Verify Installation

Run verification:
```bash
.venv/bin/python verify.py
```

### Test AI Directly

Test Ollama:
```bash
ollama run llama3 "translate to command: list my files"
```

---

## Best Practices

### 1. Use Clear Language
✅ Good: "create a file called test.txt with hello"
❌ Bad: "make test.txt have hello"

### 2. Be Specific
✅ Good: "remove lines containing 'error' from log.txt"
❌ Bad: "clean the log"

### 3. Use Dry-Run for Testing
```
> dry-run on
> dangerous command here
> dry-run off
```

### 4. Check History
```
> history 5  # See what worked before
```

### 5. Use Examples
```
> examples  # Get ideas for commands
```

---

## Still Having Issues?

1. **Read the documentation**:
   - `README.md` - Complete guide
   - `QUICKSTART.md` - Setup help
   - `QUICK_REFERENCE.md` - Command reference

2. **Verify installation**:
   ```bash
   .venv/bin/python verify.py
   ```

3. **Check GitHub issues** (if open source)

4. **Restart Kai**:
   ```
   > exit
   $ python main.py
   ```

---

**Remember**: Kai is designed to be safe. If it warns you about a command, take it seriously!
