# Kai Demo Script

This document provides a step-by-step demo of Kai's features.

## Prerequisites

Make sure Kai is installed and running:
```bash
source .venv/bin/activate
python main.py
```

## Demo Flow

### 1. Basic Commands

```
> help
```
Shows the help menu with all available commands.

```
> examples
```
Displays categorized command examples.

### 2. File Operations

```
> list my files
```
Expected: `ls -lah`

```
> create a file called demo.txt with "Hello Kai"
```
Expected: `echo "Hello Kai" > demo.txt`

```
> show contents of demo.txt
```
Expected: `cat demo.txt`

```
> add "This is a demo" to demo.txt
```
Expected: `echo "This is a demo" >> demo.txt`

```
> show it
```
Expected: `cat demo.txt` (context-aware!)

### 3. System Information

```
> show disk usage
```
Expected: `df -h`

```
> what's my IP address
```
Expected: `hostname -I` or similar

```
> show system information
```
Expected: `uname -a && free -h && df -h`

### 4. Search and Find

```
> find all python files
```
Expected: `find . -name "*.py" -type f`

```
> count lines in demo.txt
```
Expected: `wc -l demo.txt`

### 5. Safety Features

```
> delete all files in this directory
```
Expected: Warning about dangerous command, requires confirmation

```
> dry-run on
```
Enables preview mode

```
> delete demo.txt
```
Expected: Shows command but doesn't execute (dry-run mode)

```
> dry-run off
```
Disables preview mode

### 6. History

```
> history
```
Shows recent commands

```
> history 5
```
Shows last 5 commands

### 7. Configuration

```
> config
```
Shows current configuration

```
> config set timeout_seconds 30
```
Changes timeout to 30 seconds

### 8. Context Awareness

```
> create a file called test.txt
```
Expected: `echo "" > test.txt` or similar

```
> add "line 1" to it
```
Expected: `echo "line 1" >> test.txt` (remembers test.txt!)

```
> show the file
```
Expected: `cat test.txt`

### 9. Error Handling

```
> run an invalid command that doesn't exist
```
Shows how Kai handles AI errors

```
> what is the meaning of life
```
Expected: Explanation instead of command (AI knows when not to run commands)

### 10. Cleanup

```
> delete demo.txt
```
Confirm and delete

```
> delete test.txt
```
Confirm and delete

```
> clear-history
```
Clears command history (requires confirmation)

```
> exit
```
Exits Kai

## Advanced Demo

### Long-running Command Protection

```
> ping google.com
```
Expected: Warning about long-running command

### Interactive Command Blocking

```
> open nano to edit a file
```
Expected: Kai refuses to run interactive commands

### Batch Operations

```
> create three files named file1.txt, file2.txt, and file3.txt
```
Shows how AI handles complex requests

### Git Operations (if in a git repo)

```
> show git status
```
Expected: `git status`

```
> show recent commits
```
Expected: `git log -n 10` or similar

## Tips for Demo

1. **Show the banner** - Point out the clean UI
2. **Demonstrate safety** - Try a dangerous command to show warnings
3. **Show context awareness** - Use "it" and "the file" to show memory
4. **Display history** - Show how commands are tracked
5. **Toggle dry-run** - Demonstrate preview mode
6. **Show help system** - Comprehensive documentation
7. **Configuration** - Runtime changes without restart
8. **Error handling** - Show graceful failures

## Expected Outcomes

- ✅ Natural language is correctly translated to commands
- ✅ Dangerous commands trigger warnings
- ✅ Context is maintained across commands
- ✅ History is tracked and searchable
- ✅ Configuration changes work immediately
- ✅ UI is clean and informative
- ✅ Errors are handled gracefully

## Talking Points

1. **Local AI** - No cloud dependencies, privacy-focused
2. **Safety First** - Multiple layers of protection
3. **Context Aware** - Remembers recent commands and files
4. **Configurable** - Customize behavior to your needs
5. **Beautiful UI** - Rich terminal interface
6. **Well Documented** - Comprehensive help and examples
7. **Extensible** - Modular architecture for future enhancements
8. **Production Ready** - Error handling, tests, proper packaging
