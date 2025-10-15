import subprocess
import re
from typing import Dict, Optional
from ai.context import get_system_context, get_conversation_context
from utils.safety import check_command_safety, is_interactive_command, sanitize_command, SafetyLevel
from core.config import get_config

def ask_ai(prompt: str) -> Dict[str, any]:
    """
    Ask the AI to interpret a user prompt and generate a command or response.
    
    Args:
        prompt: User's natural language request
        
    Returns:
        Dictionary with intent, command/message, and optional warning
    """
    config = get_config()
    sys_context = get_system_context()
    conv_context = get_conversation_context()
    
    # Update system context
    sys_context.update_cwd()
    
    # Build enhanced system prompt with context
    system_prompt = f"""You are Kai, an intelligent terminal assistant.
Your job is to translate user requests into valid, *non-interactive* shell commands.

{sys_context.get_context_string()}

{conv_context.get_context_string()}

CRITICAL RULES:
1. ALWAYS respond with RUN:<command> if the user wants to DO something
2. Use simple one-line commands (avoid interactive editors)
3. If a filename isn't specified and one is needed, use 'output.txt' by default
4. For append operations, use >>. For create/overwrite, use >
5. Never use interactive commands like nano, vim, less, top, htop, or man
6. Use non-interactive equivalents (echo, cat, sed, awk, grep, etc.)
7. Only explain if the user asks "what", "how", "why" questions without wanting action
8. For file operations, consider the current directory: {sys_context.cwd}
9. Prefer safe, reversible operations when possible
10. If the user refers to "the file" or "it", use context from recent commands
11. For sed operations, use case-insensitive flag when appropriate: sed -i 's/pattern/replacement/gi'
12. When adding text to files, ALWAYS use echo with >>

EXAMPLES:
User: list my files
You: RUN:ls -lah

User: create a file called notes.txt with "Hello World"
You: RUN:echo "Hello World" > notes.txt

User: add "Goodbye" to it
You: RUN:echo "Goodbye" >> notes.txt

User: add a welcome text to test.txt
You: RUN:echo "Welcome!" >> test.txt

User: show disk usage
You: RUN:df -h

User: find all python files
You: RUN:find . -name "*.py" -type f

User: what is my IP address
You: RUN:hostname -I

User: compress the logs folder
You: RUN:tar -czf logs.tar.gz logs/

User: show me system info
You: RUN:uname -a && free -h && df -h

User: remove the hello from test.txt
You: RUN:sed -i '/hello/d' test.txt

User: replace hello with hi in test.txt
You: RUN:sed -i 's/hello/hi/gi' test.txt

User: what does ls do
You: The 'ls' command lists directory contents. Use 'ls -la' to see all files with details.

REMEMBER: If user says "add", "append", "write", "create", "delete", "remove", "replace", "change" - they want ACTION, so respond with RUN:<command>!
"""

    model = config.get("default_model", "llama3")
    cmd = ["ollama", "run", model, f"{system_prompt}\n\nUser: {prompt}"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout.strip()
        
        if result.returncode != 0:
            return {
                "intent": "error",
                "message": f"AI model error: {result.stderr or 'Unknown error'}"
            }
    except subprocess.TimeoutExpired:
        return {
            "intent": "error",
            "message": "AI request timed out. Please try again."
        }
    except FileNotFoundError:
        return {
            "intent": "error",
            "message": "Ollama not found. Please install Ollama and the llama3 model."
        }
    except Exception as e:
        return {
            "intent": "error",
            "message": f"Error communicating with AI: {str(e)}"
        }

    # Parse response
    match = re.search(r'RUN:\s*(.+?)(?:\n|$)', output, re.IGNORECASE)
    if match:
        command = sanitize_command(match.group(1))
        
        # Check if command is interactive
        if is_interactive_command(command):
            return {
                "intent": "explain",
                "message": f"Cannot run interactive command '{command}'. Please use a non-interactive alternative."
            }
        
        # Check command safety
        safety_level, warning = check_command_safety(command)
        
        return {
            "intent": "run",
            "command": command,
            "warning": warning,
            "safety_level": safety_level
        }

    # No command found, return explanation
    return {"intent": "explain", "message": output}