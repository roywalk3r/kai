"""Command sanitization and optimization for better script compatibility."""

import re


def sanitize_apt_command(command: str) -> str:
    """
    Convert apt commands to apt-get for script compatibility.
    
    apt shows warnings when used in scripts:
    "WARNING: apt does not have a stable CLI interface. Use with caution in scripts."
    
    Args:
        command: Shell command that might use apt
        
    Returns:
        Command with apt replaced by apt-get
    """
    # Replace standalone apt with apt-get
    # Match 'apt' as a whole word (not part of another word like 'adapt')
    command = re.sub(r'\bapt\b', 'apt-get', command)
    
    # Add DEBIAN_FRONTEND=noninteractive for update/upgrade commands
    if 'apt-get update' in command or 'apt-get upgrade' in command:
        if 'DEBIAN_FRONTEND' not in command:
            # Add before sudo if present, otherwise at start
            if command.strip().startswith('sudo'):
                command = command.replace('sudo', 'sudo DEBIAN_FRONTEND=noninteractive', 1)
            else:
                command = 'DEBIAN_FRONTEND=noninteractive ' + command
    
    # Add -y flag for install/upgrade if not present
    if 'apt-get install' in command and ' -y' not in command:
        command = command.replace('apt-get install', 'apt-get install -y')
    
    if 'apt-get upgrade' in command and ' -y' not in command:
        command = command.replace('apt-get upgrade', 'apt-get upgrade -y')
    
    return command


def sanitize_command(command: str) -> str:
    """
    Sanitize a command for better script compatibility.
    
    Args:
        command: Shell command to sanitize
        
    Returns:
        Sanitized command
    """
    # Handle apt commands
    if 'apt' in command:
        command = sanitize_apt_command(command)
    
    # Add more sanitization rules here as needed
    
    return command


def get_command_warnings(command: str) -> list:
    """
    Get warnings about a command.
    
    Args:
        command: Shell command to check
        
    Returns:
        List of warning messages
    """
    warnings = []
    
    # Check for apt usage
    if re.search(r'\bapt\b', command) and 'apt-get' not in command:
        warnings.append(
            "Using 'apt' in scripts may show warnings. "
            "Consider using 'apt-get' instead for better compatibility."
        )
    
    # Check for missing -y flag in package operations
    if ('apt-get install' in command or 'yum install' in command) and ' -y' not in command:
        warnings.append(
            "Package installation without -y flag may require user interaction. "
            "Add -y for non-interactive execution."
        )
    
    return warnings
