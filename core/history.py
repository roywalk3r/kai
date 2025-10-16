"""Command history management for Prometheus."""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class CommandHistory:
    """Manages command history for Prometheus."""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.history_dir = Path.home() / ".prometheus"
        self.history_file = self.history_dir / "history.json"
        self.history: List[Dict] = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def save(self):
        """Save history to file."""
        self.history_dir.mkdir(exist_ok=True)
        # Keep only the last max_size entries
        if len(self.history) > self.max_size:
            self.history = self.history[-self.max_size:]
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def add(self, query: str, command: str, success: bool = True, output: Optional[str] = None):
        """Add a command to history."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "command": command,
            "success": success,
            "output": output[:500] if output else None  # Limit output size
        }
        self.history.append(entry)
        self.save()
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """Get n most recent commands."""
        return self.history[-n:]
    
    def search(self, query: str) -> List[Dict]:
        """Search history for commands matching query."""
        query_lower = query.lower()
        return [
            entry for entry in self.history
            if query_lower in entry['query'].lower() or query_lower in entry['command'].lower()
        ]
    
    def clear(self):
        """Clear all history."""
        self.history = []
        self.save()
    
    def format_entry(self, entry: Dict, index: int) -> str:
        """Format a history entry for display."""
        timestamp = entry['timestamp'][:19]  # Remove microseconds
        status = "✓" if entry.get('success', True) else "✗"
        return f"{index}. [{timestamp}] {status} {entry['query']} → {entry['command']}"
    
    def display(self, n: int = 10) -> str:
        """Return formatted history string."""
        recent = self.get_recent(n)
        if not recent:
            return "No command history yet."
        
        lines = [f"Recent Commands (last {len(recent)}):"]
        for i, entry in enumerate(recent, 1):
            lines.append(self.format_entry(entry, i))
        return "\n".join(lines)

# Global history instance
_history = None

def get_history() -> CommandHistory:
    """Get global history instance."""
    global _history
    if _history is None:
        _history = CommandHistory()
    return _history
