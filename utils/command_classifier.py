"""Command classification for timeout and safety detection."""

import re
from typing import Tuple

# Commands that typically take a long time
LONG_RUNNING_COMMANDS = {
    # Package management
    'apt', 'apt-get', 'yum', 'dnf', 'pacman', 'zypper', 'brew',
    # System updates
    'update', 'upgrade', 'dist-upgrade', 'full-upgrade',
    # Compilation and builds
    'make', 'cmake', 'gcc', 'g++', 'cargo', 'npm', 'yarn', 'pip',
    'mvn', 'gradle', 'ant', 'bazel',
    # Downloads
    'wget', 'curl', 'git clone', 'rsync', 'scp',
    # Database operations
    'mysqldump', 'pg_dump', 'mongodump',
    # Compression
    'tar', 'zip', 'unzip', 'gzip', 'bzip2', '7z',
    # Docker
    'docker build', 'docker pull', 'docker-compose',
    # System scans
    'find', 'locate', 'updatedb', 'clamscan',
}

# Keywords that indicate long operations
LONG_OPERATION_KEYWORDS = [
    'install', 'update', 'upgrade', 'download', 'clone', 'build',
    'compile', 'backup', 'restore', 'scan', 'search', 'index',
    'compress', 'decompress', 'extract', 'sync', 'copy', 'move',
    'convert', 'encode', 'decode', 'render', 'process'
]

# Commands that are typically quick
QUICK_COMMANDS = {
    'ls', 'cd', 'pwd', 'echo', 'cat', 'head', 'tail', 'wc',
    'date', 'whoami', 'hostname', 'uname', 'which', 'type',
    'alias', 'export', 'env', 'printenv', 'id', 'groups',
    'df', 'du', 'free', 'uptime', 'ps', 'kill', 'killall',
    'mkdir', 'rmdir', 'touch', 'rm', 'mv', 'cp', 'ln',
    'chmod', 'chown', 'chgrp', 'grep', 'sed', 'awk', 'cut',
    'sort', 'uniq', 'diff', 'cmp', 'file', 'stat'
}


def classify_command_timeout(command: str) -> Tuple[str, int]:
    """
    Classify a command and return appropriate timeout.
    
    Args:
        command: Shell command to classify
        
    Returns:
        Tuple of (classification, timeout_seconds)
        Classifications: 'quick', 'normal', 'long'
    """
    from core.config import get_config
    config = get_config()
    
    command_lower = command.lower()
    
    # Extract the base command (first word)
    base_cmd = command.split()[0] if command.split() else ''
    base_cmd_lower = base_cmd.lower()
    
    # Check for long-running commands
    for long_cmd in LONG_RUNNING_COMMANDS:
        if long_cmd in command_lower:
            return ('long', config.get('long_timeout', 1800))
    
    # Check for long operation keywords
    for keyword in LONG_OPERATION_KEYWORDS:
        if keyword in command_lower:
            return ('long', config.get('long_timeout', 1800))
    
    # Check for quick commands
    if base_cmd_lower in QUICK_COMMANDS:
        return ('quick', config.get('short_timeout', 30))
    
    # Check for piped commands (might be slower)
    if '|' in command or '&&' in command or ';' in command:
        return ('normal', config.get('timeout_seconds', 300))
    
    # Default to normal timeout
    return ('normal', config.get('timeout_seconds', 300))


def is_long_running_command(command: str) -> bool:
    """
    Check if a command is likely to be long-running.
    
    Args:
        command: Shell command to check
        
    Returns:
        True if command is likely long-running
    """
    classification, _ = classify_command_timeout(command)
    return classification == 'long'


def get_command_timeout(command: str) -> int:
    """
    Get appropriate timeout for a command.
    
    Args:
        command: Shell command
        
    Returns:
        Timeout in seconds
    """
    _, timeout = classify_command_timeout(command)
    return timeout


def format_timeout_message(timeout: int) -> str:
    """
    Format timeout duration for display.
    
    Args:
        timeout: Timeout in seconds
        
    Returns:
        Formatted string (e.g., "5 minutes", "30 seconds")
    """
    if timeout >= 3600:
        hours = timeout // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"
    elif timeout >= 60:
        minutes = timeout // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        return f"{timeout} second{'s' if timeout > 1 else ''}"
