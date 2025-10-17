#!/usr/bin/env python3
"""
Session memory and context management.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import deque


class SessionContext:
    """Manage session context and memory."""
    
    def __init__(self, persist: bool = False):
        """
        Initialize session context.
        
        Args:
            persist: Whether to persist context between sessions
        """
        self.persist = persist
        self.context_file = Path.home() / ".prometheus" / "session_context.json"
        
        # Conversation history (last N exchanges)
        self.conversation_history = deque(maxlen=10)
        
        # File/path references mentioned
        self.file_references = []
        
        # Variables and values
        self.variables = {}
        
        # Last commands and results
        self.command_history = deque(maxlen=20)
        
        # Current working context
        self.current_directory = Path.cwd()
        self.current_project_type = None
        
        # Session metadata
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        
        # Load persisted context if enabled
        if self.persist:
            self._load_context()
    
    def add_exchange(self, query: str, response: Dict):
        """
        Add a query-response exchange to context.
        
        Args:
            query: User query
            response: System response
        """
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response
        })
        
        # Extract file references from query and response
        self._extract_file_references(query)
        if isinstance(response, dict) and "command" in response:
            self._extract_file_references(response["command"])
        
        # Save if persistence is enabled
        if self.persist:
            self._save_context()
    
    def add_command_result(self, command: str, success: bool, output: str):
        """
        Add command execution result.
        
        Args:
            command: Executed command
            success: Whether command succeeded
            output: Command output
        """
        self.command_history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
            "output": output[:500]  # Limit output size
        })
    
    def _extract_file_references(self, text: str):
        """Extract file/path references from text."""
        import re
        
        # Match file paths (basic patterns)
        patterns = [
            r'[\'"]([/\w\-\.]+)[\'"]',  # Quoted paths
            r'\b([\w\-]+\.[\w]+)\b',  # filename.ext
            r'\b(/[\w/\-\.]+)\b',  # Absolute paths
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 2 and match not in self.file_references:
                    # Check if it looks like a file
                    if '.' in match or '/' in match:
                        self.file_references.append(match)
        
        # Keep only last 20 references
        self.file_references = self.file_references[-20:]
    
    def set_variable(self, name: str, value: Any):
        """Set a context variable."""
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Optional[Any]:
        """Get a context variable."""
        return self.variables.get(name)
    
    def get_context_summary(self) -> str:
        """Get a summary of current context for AI."""
        summary_parts = []
        
        # Current directory
        summary_parts.append(f"Current directory: {self.current_directory}")
        
        # Recent conversation
        if self.conversation_history:
            last_queries = [ex["query"] for ex in list(self.conversation_history)[-3:]]
            summary_parts.append(f"Recent queries: {', '.join(last_queries)}")
        
        # File references
        if self.file_references:
            summary_parts.append(f"Referenced files: {', '.join(self.file_references[-5:])}")
        
        # Variables
        if self.variables:
            var_str = ', '.join(f"{k}={v}" for k, v in self.variables.items())
            summary_parts.append(f"Variables: {var_str}")
        
        # Last command result
        if self.command_history:
            last_cmd = list(self.command_history)[-1]
            status = "succeeded" if last_cmd["success"] else "failed"
            summary_parts.append(f"Last command '{last_cmd['command']}' {status}")
        
        return "\n".join(summary_parts)
    
    def resolve_reference(self, ref: str) -> Optional[str]:
        """
        Resolve contextual references like 'it', 'that', 'the file'.
        
        Args:
            ref: Reference to resolve
        
        Returns:
            Resolved value or None
        """
        ref_lower = ref.lower()
        
        # Positional references
        if ref_lower in ["it", "that", "this"]:
            if self.file_references:
                return self.file_references[-1]
        
        if "file" in ref_lower:
            if self.file_references:
                return self.file_references[-1]
        
        # Ordinal references (the second one, the third file, etc.)
        import re
        ordinal_match = re.search(r'(first|second|third|fourth|fifth|last|\d+(?:st|nd|rd|th))', ref_lower)
        if ordinal_match and self.file_references:
            ordinal = ordinal_match.group(1)
            ordinal_map = {
                "first": 0, "second": 1, "third": 2, "fourth": 3, "fifth": 4,
                "last": -1
            }
            
            if ordinal in ordinal_map:
                idx = ordinal_map[ordinal]
                if -len(self.file_references) <= idx < len(self.file_references):
                    return self.file_references[idx]
        
        # Variable reference
        if ref in self.variables:
            return self.variables[ref]
        
        return None
    
    def get_relevant_history(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Get relevant history items for current query.
        
        Args:
            query: Current query
            limit: Maximum items to return
        
        Returns:
            List of relevant history items
        """
        query_lower = query.lower()
        relevant = []
        
        for exchange in reversed(self.conversation_history):
            # Check if exchange is relevant
            past_query = exchange["query"].lower()
            
            # Simple relevance check (can be improved with embeddings)
            if any(word in past_query for word in query_lower.split() if len(word) > 3):
                relevant.append(exchange)
            
            if len(relevant) >= limit:
                break
        
        return list(reversed(relevant))
    
    def clear_context(self):
        """Clear all context except session metadata."""
        self.conversation_history.clear()
        self.file_references.clear()
        self.variables.clear()
        self.command_history.clear()
    
    def _save_context(self):
        """Save context to file."""
        if not self.persist:
            return
        
        self.context_file.parent.mkdir(parents=True, exist_ok=True)
        
        context_data = {
            "session_id": self.session_id,
            "session_start": self.session_start.isoformat(),
            "current_directory": str(self.current_directory),
            "conversation_history": list(self.conversation_history),
            "file_references": self.file_references,
            "variables": self.variables,
            "command_history": list(self.command_history)
        }
        
        with open(self.context_file, 'w') as f:
            json.dump(context_data, f, indent=2)
    
    def _load_context(self):
        """Load context from file."""
        if not self.context_file.exists():
            return
        
        try:
            with open(self.context_file, 'r') as f:
                context_data = json.load(f)
            
            # Load only recent session data (last 24 hours)
            session_start = datetime.fromisoformat(context_data["session_start"])
            if (datetime.now() - session_start).days < 1:
                self.conversation_history = deque(context_data.get("conversation_history", []), maxlen=10)
                self.file_references = context_data.get("file_references", [])
                self.variables = context_data.get("variables", {})
                self.command_history = deque(context_data.get("command_history", []), maxlen=20)
        except:
            pass
    
    def get_statistics(self) -> Dict:
        """Get session statistics."""
        success_count = sum(1 for cmd in self.command_history if cmd.get("success"))
        total_commands = len(self.command_history)
        
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "exchanges": len(self.conversation_history),
            "commands_executed": total_commands,
            "success_rate": f"{(success_count/total_commands*100):.0f}%" if total_commands > 0 else "N/A",
            "files_referenced": len(self.file_references),
            "variables_set": len(self.variables)
        }


# Global session instance
_session_context = None


def get_session_context(persist: bool = False) -> SessionContext:
    """Get global session context instance."""
    global _session_context
    if _session_context is None:
        _session_context = SessionContext(persist=persist)
    return _session_context


def show_session_info():
    """Display session information."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    session = get_session_context()
    stats = session.get_statistics()
    
    console = Console()
    
    # Session info
    console.print(Panel(
        f"[bold bright_cyan]Session ID:[/bold bright_cyan] {session.session_id}\n"
        f"[bold bright_cyan]Duration:[/bold bright_cyan] {stats['session_duration']}\n"
        f"[bold bright_cyan]Directory:[/bold bright_cyan] {session.current_directory}",
        title="[bold]Session Info[/bold]",
        border_style="cyan"
    ))
    
    # Statistics table
    table = Table(title="Session Statistics", border_style="cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bright_white")
    
    for key, value in stats.items():
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)
    
    # Recent context
    if session.file_references:
        console.print("\n[bold]Recent File References:[/bold]")
        for ref in session.file_references[-5:]:
            console.print(f"  • {ref}")
    
    if session.variables:
        console.print("\n[bold]Variables:[/bold]")
        for name, value in session.variables.items():
            console.print(f"  • {name} = {value}")
