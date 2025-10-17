#!/usr/bin/env python3
"""
Enhanced error recovery with AI-powered fix suggestions.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ErrorPattern:
    """Pattern for matching and fixing common errors."""
    
    def __init__(self, pattern: str, error_type: str, fixes: List[str]):
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.error_type = error_type
        self.fixes = fixes
    
    def matches(self, error_text: str) -> bool:
        """Check if this pattern matches the error."""
        return bool(self.pattern.search(error_text))
    
    def get_fixes(self) -> List[str]:
        """Get suggested fixes."""
        return self.fixes


# Common error patterns and their fixes
ERROR_PATTERNS = [
    ErrorPattern(
        r"(no such file or directory|cannot stat|not found).*['\"]?(\S+)['\"]?",
        "file_not_found",
        [
            "Check if the file path is correct (case-sensitive)",
            "Use 'find' or 'locate' to find the file",
            "Verify the file exists: ls -la {path}",
            "Check current directory: pwd"
        ]
    ),
    ErrorPattern(
        r"permission denied",
        "permission_denied",
        [
            "Try with sudo: sudo {command}",
            "Check file permissions: ls -l {file}",
            "Change permissions: chmod +x {file}",
            "Check ownership: ls -l {file}"
        ]
    ),
    ErrorPattern(
        r"command not found",
        "command_not_found",
        [
            "Install the package: sudo apt install {command}",
            "Check if command is in PATH: which {command}",
            "Try full path: /usr/bin/{command}",
            "Search for package: apt search {command}"
        ]
    ),
    ErrorPattern(
        r"port.*already in use|address already in use",
        "port_in_use",
        [
            "Find process using port: lsof -i :{port}",
            "Kill process: kill -9 $(lsof -t -i:{port})",
            "Use different port",
            "Check running services: netstat -tulpn"
        ]
    ),
    ErrorPattern(
        r"no space left on device",
        "disk_full",
        [
            "Check disk usage: df -h",
            "Find large files: du -sh * | sort -h",
            "Clean package cache: sudo apt clean",
            "Remove old logs: sudo journalctl --vacuum-time=7d"
        ]
    ),
    ErrorPattern(
        r"connection refused|connection timed out",
        "connection_failed",
        [
            "Check if service is running: systemctl status {service}",
            "Verify network connectivity: ping {host}",
            "Check firewall rules: sudo ufw status",
            "Test port: telnet {host} {port}"
        ]
    ),
    ErrorPattern(
        r"(module|package).*not found|no module named",
        "module_not_found",
        [
            "Install with pip: pip install {module}",
            "Check if in requirements.txt",
            "Activate virtual environment: source venv/bin/activate",
            "Check Python path: python -c 'import sys; print(sys.path)'"
        ]
    ),
    ErrorPattern(
        r"syntax error|invalid syntax",
        "syntax_error",
        [
            "Check for typos in command",
            "Verify quote matching",
            "Check command syntax: man {command}",
            "Try --help flag: {command} --help"
        ]
    ),
    ErrorPattern(
        r"access denied|forbidden",
        "access_denied",
        [
            "Check credentials",
            "Verify API key/token",
            "Check user permissions",
            "Try with elevated privileges"
        ]
    ),
    ErrorPattern(
        r"git.*failed|fatal.*git",
        "git_error",
        [
            "Check git status: git status",
            "Pull latest changes: git pull",
            "Check remote: git remote -v",
            "Reset if needed: git reset --hard"
        ]
    ),
]


class ErrorAnalyzer:
    """Analyzes command errors and provides intelligent fix suggestions."""
    
    def __init__(self):
        self.error_history_file = Path.home() / ".prometheus" / "error_history.json"
        self.error_history = self._load_error_history()
        self.patterns = ERROR_PATTERNS
    
    def _load_error_history(self) -> List[Dict]:
        """Load error history from file."""
        if self.error_history_file.exists():
            try:
                with open(self.error_history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_error_history(self):
        """Save error history to file."""
        self.error_history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.error_history_file, 'w') as f:
            json.dump(self.error_history[-100:], f, indent=2)  # Keep last 100
    
    def analyze_error(
        self,
        command: str,
        exit_code: int,
        stderr: str,
        stdout: str = ""
    ) -> Dict:
        """
        Analyze an error and provide fix suggestions.
        
        Returns:
            Dict with error_type, description, suggestions, and ai_prompt
        """
        # Record the error
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "exit_code": exit_code,
            "stderr": stderr[:500],  # First 500 chars
            "stdout": stdout[:500] if stdout else ""
        }
        self.error_history.append(error_record)
        self._save_error_history()
        
        # Analyze error
        error_text = stderr + " " + stdout
        
        # Try to match known patterns
        for pattern in self.patterns:
            if pattern.matches(error_text):
                suggestions = self._format_suggestions(
                    pattern.get_fixes(),
                    command,
                    error_text
                )
                
                return {
                    "error_type": pattern.error_type,
                    "description": self._extract_error_message(error_text),
                    "suggestions": suggestions,
                    "ai_prompt": self._build_ai_prompt(command, error_text, pattern.error_type),
                    "severity": self._determine_severity(exit_code, pattern.error_type)
                }
        
        # Unknown error - provide generic suggestions
        return {
            "error_type": "unknown",
            "description": self._extract_error_message(error_text),
            "suggestions": self._get_generic_suggestions(command, error_text),
            "ai_prompt": self._build_ai_prompt(command, error_text, "unknown"),
            "severity": "medium"
        }
    
    def _format_suggestions(
        self,
        suggestions: List[str],
        command: str,
        error_text: str
    ) -> List[str]:
        """Format suggestions with context."""
        formatted = []
        
        # Extract useful info from command and error
        cmd_parts = command.split()
        base_command = cmd_parts[0] if cmd_parts else ""
        
        # Extract file/path mentions
        file_match = re.search(r"['\"]([^'\"]+)['\"]", error_text)
        file_path = file_match.group(1) if file_match else "file"
        
        # Extract port numbers
        port_match = re.search(r"port\s+(\d+)", error_text)
        port = port_match.group(1) if port_match else "8080"
        
        for suggestion in suggestions:
            formatted.append(
                suggestion
                .replace("{command}", base_command)
                .replace("{file}", file_path)
                .replace("{path}", file_path)
                .replace("{port}", port)
                .replace("{service}", base_command)
                .replace("{host}", "localhost")
                .replace("{module}", base_command)
            )
        
        return formatted
    
    def _extract_error_message(self, error_text: str) -> str:
        """Extract the main error message."""
        lines = error_text.strip().split('\n')
        
        # Look for common error indicators
        for line in lines:
            line = line.strip()
            if any(indicator in line.lower() for indicator in [
                'error:', 'fatal:', 'failed:', 'exception:', 'cannot', 'unable'
            ]):
                return line[:200]  # First 200 chars
        
        # Return first non-empty line
        for line in lines:
            if line.strip():
                return line.strip()[:200]
        
        return "Unknown error occurred"
    
    def _get_generic_suggestions(self, command: str, error_text: str) -> List[str]:
        """Provide generic suggestions for unknown errors."""
        suggestions = [
            f"Check the command syntax: {command.split()[0]} --help",
            "Review the error message carefully",
            "Search for the error online",
        ]
        
        cmd_parts = command.split()
        if cmd_parts:
            suggestions.append(f"Check manual: man {cmd_parts[0]}")
        
        return suggestions
    
    def _build_ai_prompt(self, command: str, error_text: str, error_type: str) -> str:
        """Build a prompt for AI to provide better fix."""
        return (
            f"The command '{command}' failed with error type '{error_type}'.\n"
            f"Error output:\n{error_text[:500]}\n\n"
            f"Provide 2-3 specific, actionable fixes for this error. "
            f"Consider the context and provide exact commands when possible."
        )
    
    def _determine_severity(self, exit_code: int, error_type: str) -> str:
        """Determine error severity."""
        if error_type in ["disk_full", "permission_denied"]:
            return "high"
        elif error_type in ["file_not_found", "command_not_found"]:
            return "medium"
        elif exit_code > 100:
            return "high"
        else:
            return "low"
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        """Get recent errors from history."""
        return self.error_history[-limit:]
    
    def get_error_statistics(self) -> Dict:
        """Get error statistics."""
        if not self.error_history:
            return {
                "total_errors": 0,
                "most_common_type": None,
                "most_failed_command": None
            }
        
        error_types = {}
        commands = {}
        
        for error in self.error_history:
            cmd = error.get("command", "").split()[0]
            if cmd:
                commands[cmd] = commands.get(cmd, 0) + 1
        
        most_common_command = max(commands.items(), key=lambda x: x[1])[0] if commands else None
        
        return {
            "total_errors": len(self.error_history),
            "most_failed_command": most_common_command,
            "recent_errors": len([e for e in self.error_history[-20:]])
        }


def analyze_and_suggest_fix(command: str, exit_code: int, stderr: str, stdout: str = "") -> Dict:
    """
    Main function to analyze error and get suggestions.
    
    Args:
        command: The command that failed
        exit_code: Exit code of the command
        stderr: Standard error output
        stdout: Standard output (optional)
    
    Returns:
        Dict with error analysis and suggestions
    """
    analyzer = ErrorAnalyzer()
    return analyzer.analyze_error(command, exit_code, stderr, stdout)


def get_ai_fix_suggestion(command: str, error_output: str, ai_model) -> Optional[str]:
    """
    Get AI-powered fix suggestion.
    
    Args:
        command: Failed command
        error_output: Error output
        ai_model: AI model instance
    
    Returns:
        AI-suggested fix command or None
    """
    try:
        prompt = (
            f"The command '{command}' failed with this error:\n"
            f"{error_output}\n\n"
            f"Provide ONE fixed command that should work. "
            f"Return ONLY the command, no explanation."
        )
        
        response = ai_model.generate_command(prompt)
        if response and "command" in response:
            return response["command"]
    except:
        pass
    
    return None
