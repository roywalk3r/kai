"""Context management for better AI responses."""

import os
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class SystemContext:
    """Manages system context for AI model."""
    
    def __init__(self):
        self.os_name = platform.system()
        self.os_version = platform.release()
        self.shell = os.environ.get('SHELL', '/bin/bash')
        self.user = os.environ.get('USER', 'user')
        self.home = str(Path.home())
        self.cwd = os.getcwd()
    
    def update_cwd(self):
        """Update current working directory."""
        self.cwd = os.getcwd()
    
    def get_context_string(self) -> str:
        """Get formatted context string for AI prompt."""
        return f"""
System Context:
- OS: {self.os_name} {self.os_version}
- Shell: {self.shell}
- User: {self.user}
- Current Directory: {self.cwd}
- Home Directory: {self.home}
"""
    
    def get_directory_contents(self, limit: int = 20) -> List[str]:
        """Get list of files in current directory."""
        try:
            items = []
            for item in Path(self.cwd).iterdir():
                if len(items) >= limit:
                    break
                items.append(item.name)
            return items
        except Exception:
            return []
    
    def check_command_available(self, command: str) -> bool:
        """Check if a command is available on the system."""
        try:
            result = subprocess.run(
                ['which', command],
                capture_output=True,
                text=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_common_tools(self) -> Dict[str, bool]:
        """Check availability of common tools."""
        tools = ['git', 'docker', 'npm', 'python', 'python3', 'node', 'java', 'go']
        return {tool: self.check_command_available(tool) for tool in tools}

class ConversationContext:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 5):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        self.last_command: Optional[str] = None
        self.last_output: Optional[str] = None
    
    def add_interaction(self, query: str, command: str, output: Optional[str] = None):
        """Add an interaction to history."""
        self.history.append({
            'query': query,
            'command': command,
            'output': output[:200] if output else None  # Limit output size
        })
        
        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        self.last_command = command
        self.last_output = output
    
    def get_context_string(self) -> str:
        """Get formatted conversation context."""
        if not self.history:
            return ""
        
        lines = ["Recent Commands:"]
        for i, interaction in enumerate(self.history[-3:], 1):
            lines.append(f"{i}. User: {interaction['query']}")
            lines.append(f"   Command: {interaction['command']}")
        
        return "\n".join(lines)
    
    def clear(self):
        """Clear conversation history."""
        self.history = []
        self.last_command = None
        self.last_output = None

# Global context instances
_system_context = None
_conversation_context = None

def get_system_context() -> SystemContext:
    """Get global system context instance."""
    global _system_context
    if _system_context is None:
        _system_context = SystemContext()
    return _system_context

def get_conversation_context() -> ConversationContext:
    """Get global conversation context instance."""
    global _conversation_context
    if _conversation_context is None:
        _conversation_context = ConversationContext()
    return _conversation_context
