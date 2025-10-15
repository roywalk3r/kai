"""Smart error detection and auto-fixing for Kai."""

import re
from typing import Optional, Tuple

def detect_and_fix_error(command: str, error_output: str, exit_code: int) -> Optional[Tuple[str, str]]:
    """
    Detect common errors and suggest fixes.
    
    Args:
        command: The command that failed
        error_output: Error message from stderr
        exit_code: Exit code of the failed command
        
    Returns:
        Tuple of (fixed_command, explanation) or None if no fix found
    """
    
    # Shell syntax error with && in sh
    if "Syntax error" in error_output and "&&" in error_output:
        if "&&" in command:
            # Fix: Use bash instead of sh, or split into separate commands
            fixed = f"bash -c '{command}'"
            explanation = "Fixed: Shell syntax error. The command uses '&&' which requires bash, not sh."
            return fixed, explanation
    
    # Command not found
    if "command not found" in error_output.lower() or exit_code == 127:
        cmd_name = command.split()[0]
        
        # Common typos and alternatives
        alternatives = {
            "pytohn": "python",
            "pyhton": "python",
            "gti": "git",
            "gti": "git",
            "claer": "clear",
            "cd..": "cd ..",
            "sl": "ls",
            "grpe": "grep",
            "mroe": "more",
            "les": "less",
        }
        
        if cmd_name in alternatives:
            fixed = command.replace(cmd_name, alternatives[cmd_name], 1)
            explanation = f"Fixed: Typo detected. Changed '{cmd_name}' to '{alternatives[cmd_name]}'."
            return fixed, explanation
    
    # Permission denied
    if "permission denied" in error_output.lower() or exit_code == 126:
        if not command.startswith("sudo "):
            fixed = f"sudo {command}"
            explanation = "Fixed: Permission denied. Added 'sudo' to run with elevated privileges."
            return fixed, explanation
    
    # File or directory not found
    if "no such file or directory" in error_output.lower():
        # Check if it's a path issue
        if "/" in command:
            explanation = "Error: File or directory not found. Check the path and try again."
            return None, explanation
    
    # Git not initialized
    if "not a git repository" in error_output.lower():
        if command.startswith("git ") and not command.startswith("git init"):
            fixed = f"git init && {command}"
            explanation = "Fixed: Not a git repository. Running 'git init' first."
            return fixed, explanation
    
    # Port already in use
    if "address already in use" in error_output.lower():
        port_match = re.search(r':(\d+)', error_output)
        if port_match:
            port = port_match.group(1)
            explanation = f"Error: Port {port} is already in use. Kill the process or use a different port."
            return None, explanation
    
    # Python module not found
    if "No module named" in error_output:
        module_match = re.search(r"No module named '([^']+)'", error_output)
        if module_match:
            module = module_match.group(1)
            fixed = f"pip install {module} && {command}"
            explanation = f"Fixed: Module '{module}' not found. Installing it first."
            return fixed, explanation
    
    # Unmatched quotes
    if "unmatched" in error_output.lower() and ("quote" in error_output.lower() or "'" in error_output or '"' in error_output):
        # Try to fix unmatched quotes
        single_quotes = command.count("'")
        double_quotes = command.count('"')
        
        if single_quotes % 2 != 0:
            fixed = command + "'"
            explanation = "Fixed: Added missing single quote at the end."
            return fixed, explanation
        elif double_quotes % 2 != 0:
            fixed = command + '"'
            explanation = "Fixed: Added missing double quote at the end."
            return fixed, explanation
    
    # Network unreachable
    if "network is unreachable" in error_output.lower() or "could not resolve host" in error_output.lower():
        explanation = "Error: Network issue detected. Check your internet connection."
        return None, explanation
    
    # Disk full
    if "no space left on device" in error_output.lower():
        explanation = "Error: Disk is full. Free up some space and try again."
        return None, explanation
    
    return None

def analyze_error(command: str, error_output: str, exit_code: int) -> str:
    """
    Analyze an error and provide helpful explanation.
    
    Args:
        command: The command that failed
        error_output: Error message from stderr
        exit_code: Exit code of the failed command
        
    Returns:
        Human-readable explanation of the error
    """
    
    if exit_code == 0:
        return "Command completed successfully."
    
    # Try to get a fix
    result = detect_and_fix_error(command, error_output, exit_code)
    if result:
        return result[1]
    
    # Generic error analysis
    if exit_code == 1:
        return "Command failed with general error. Check the error message above."
    elif exit_code == 2:
        return "Command failed due to misuse or syntax error."
    elif exit_code == 126:
        return "Permission denied or command not executable."
    elif exit_code == 127:
        return "Command not found. Check if it's installed and in PATH."
    elif exit_code == 130:
        return "Command interrupted by user (Ctrl+C)."
    elif exit_code == 137:
        return "Command killed (possibly out of memory)."
    elif exit_code == 143:
        return "Command terminated (SIGTERM)."
    else:
        return f"Command failed with exit code {exit_code}."
