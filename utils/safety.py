"""Safety checks and validation for commands."""

import re
from typing import Tuple, Optional

# Commands that are likely long-running or risky
LONG_RUNNING_KEYWORDS = [
    "ping", "find /", "sleep", "dd", "cat /dev", "yes", 
    "tail -f", "watch", "while true", "for i in"
]

DANGEROUS_KEYWORDS = [
    "rm -rf", "rm -fr", ":(){", "mkfs", "shutdown", "reboot",
    "dd if=", "chmod -R 777", "> /dev/sda", "mv / ", "format",
    "fdisk", "parted", "wipefs"
]

# Commands that modify system state but are generally safe
MODIFY_KEYWORDS = [
    "apt install", "yum install", "pacman -S", "brew install",
    "pip install", "npm install", "cargo install"
]

# Commands that are always safe
SAFE_COMMANDS = [
    "ls", "pwd", "echo", "cat", "grep", "find", "which", "whereis",
    "date", "cal", "uptime", "whoami", "hostname", "uname",
    "df", "du", "free", "top", "ps", "history", "man", "help"
]

class SafetyLevel:
    """Safety levels for commands."""
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
    LONG_RUNNING = "long_running"

def check_command_safety(command: str) -> Tuple[str, Optional[str]]:
    """
    Check if a command is safe to run.
    
    Returns:
        Tuple of (safety_level, warning_message)
    """
    command_lower = command.lower().strip()
    
    # Check if it's a known safe command
    first_word = command_lower.split()[0] if command_lower else ""
    if first_word in SAFE_COMMANDS:
        return SafetyLevel.SAFE, None
    
    # Check for dangerous patterns
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in command_lower:
            return SafetyLevel.DANGEROUS, f"⚠️  DANGER: This command contains '{keyword}' which could be destructive!"
    
    # Check for long-running patterns
    for keyword in LONG_RUNNING_KEYWORDS:
        if keyword in command_lower:
            return SafetyLevel.LONG_RUNNING, f"⏳ This command might take a long time (contains '{keyword}')"
    
    # Check for modification patterns
    for keyword in MODIFY_KEYWORDS:
        if keyword in command_lower:
            return SafetyLevel.CAUTION, f"⚡ This command will modify your system ('{keyword}')"
    
    # Check for pipe to shell
    if re.search(r'\|\s*sh|\|\s*bash|\|\s*zsh', command_lower):
        return SafetyLevel.DANGEROUS, "⚠️  DANGER: Piping to shell can be dangerous!"
    
    # Check for sudo
    if command_lower.startswith('sudo'):
        return SafetyLevel.CAUTION, "⚡ This command requires elevated privileges"
    
    return SafetyLevel.SAFE, None

def validate_command(command: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that a command is properly formed.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not command or not command.strip():
        return False, "Empty command"
    
    # Check for unmatched quotes
    single_quotes = command.count("'")
    double_quotes = command.count('"')
    
    if single_quotes % 2 != 0:
        return False, "Unmatched single quote"
    
    if double_quotes % 2 != 0:
        return False, "Unmatched double quote"
    
    # Check for unmatched parentheses
    if command.count('(') != command.count(')'):
        return False, "Unmatched parentheses"
    
    # Check for unmatched brackets
    if command.count('[') != command.count(']'):
        return False, "Unmatched brackets"
    
    # Check for unmatched braces
    if command.count('{') != command.count('}'):
        return False, "Unmatched braces"
    
    return True, None

def is_interactive_command(command: str) -> bool:
    """Check if a command is interactive and shouldn't be run automatically."""
    interactive_commands = [
        "nano", "vim", "vi", "emacs", "less", "more", "top", "htop",
        "man", "ssh", "ftp", "telnet", "mysql", "psql", "mongo"
    ]
    
    first_word = command.strip().split()[0] if command.strip() else ""
    return first_word in interactive_commands

def sanitize_command(command: str) -> str:
    """Sanitize a command by removing potentially harmful elements."""
    # Remove leading/trailing whitespace
    command = command.strip()
    
    # Remove multiple spaces
    command = re.sub(r'\s+', ' ', command)
    
    return command
