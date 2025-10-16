"""Smart history features with fuzzy search and analytics."""

import re
from typing import List, Optional, Dict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from core.history import get_history

console = Console()


class SmartHistory:
    """Enhanced history with smart features."""
    
    def __init__(self):
        self.history = get_history()
    
    def fuzzy_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Fuzzy search through command history."""
        query_lower = query.lower()
        matches = []
        
        for entry in reversed(self.history.history):
            command = entry.get('command', '')
            user_query = entry.get('query', '')
            
            # Simple fuzzy matching
            if (query_lower in command.lower() or 
                query_lower in user_query.lower()):
                matches.append(entry)
                
                if len(matches) >= limit:
                    break
        
        return matches
    
    def get_last_command(self) -> Optional[str]:
        """Get the last executed command."""
        if self.history.history:
            return self.history.history[-1].get('command')
        return None
    
    def get_last_successful_command(self) -> Optional[str]:
        """Get the last successful command."""
        for entry in reversed(self.history.history):
            if entry.get('success'):
                return entry.get('command')
        return None
    
    def get_last_failed_command(self) -> Optional[str]:
        """Get the last failed command."""
        for entry in reversed(self.history.history):
            if not entry.get('success'):
                return entry.get('command')
        return None
    
    def get_most_used_commands(self, limit: int = 10) -> List[tuple]:
        """Get most frequently used commands."""
        command_counts = {}
        
        for entry in self.history.history:
            cmd = entry.get('command', '')
            # Get base command (first word)
            base_cmd = cmd.split()[0] if cmd else ''
            if base_cmd:
                command_counts[base_cmd] = command_counts.get(base_cmd, 0) + 1
        
        # Sort by count
        sorted_commands = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_commands[:limit]
    
    def show_statistics(self):
        """Show history statistics."""
        total = len(self.history.history)
        successful = sum(1 for e in self.history.history if e.get('success'))
        failed = total - successful
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        table = Table(title="Command History Statistics", border_style="bright_cyan")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bright_white")
        
        table.add_row("Total Commands", str(total))
        table.add_row("Successful", f"{successful} ({success_rate:.1f}%)")
        table.add_row("Failed", str(failed))
        
        console.print(table)
        
        # Show most used commands
        most_used = self.get_most_used_commands(5)
        if most_used:
            console.print("\n[bold cyan]Most Used Commands:[/bold cyan]")
            for cmd, count in most_used:
                console.print(f"  [bright_white]{cmd}[/bright_white]: {count} times")
    
    def suggest_from_context(self, query: str) -> Optional[str]:
        """Suggest command based on query and context."""
        # Look for similar past queries
        matches = self.fuzzy_search(query, limit=5)
        
        if matches:
            # Return the most recent successful match
            for match in matches:
                if match.get('success'):
                    return match.get('command')
        
        return None
    
    def replay_command(self, index: int) -> Optional[str]:
        """Get command at specific history index."""
        try:
            if 0 <= index < len(self.history.history):
                return self.history.history[index].get('command')
            elif index < 0:  # Negative indexing
                return self.history.history[index].get('command')
        except IndexError:
            pass
        return None
    
    def show_recent(self, n: int = 10):
        """Show recent commands with enhanced formatting."""
        recent = list(reversed(self.history.history[-n:]))
        
        if not recent:
            console.print("[yellow]No command history yet[/yellow]")
            return
        
        table = Table(title=f"Recent Commands ({len(recent)})", border_style="bright_cyan")
        table.add_column("#", style="dim", width=4)
        table.add_column("Query", style="bright_white", width=30)
        table.add_column("Command", style="cyan", width=40)
        table.add_column("Status", style="green", width=8)
        
        for i, entry in enumerate(recent, 1):
            query = entry.get('query', '')[:30]
            command = entry.get('command', '')[:40]
            status = "✓" if entry.get('success') else "✗"
            status_color = "green" if entry.get('success') else "red"
            
            table.add_row(
                str(i),
                query,
                command,
                f"[{status_color}]{status}[/{status_color}]"
            )
        
        console.print(table)


def handle_bang_commands(query: str) -> Optional[str]:
    """Handle bash-style !! and !n commands."""
    smart_history = SmartHistory()
    
    # !! - repeat last command
    if query == "!!":
        last_cmd = smart_history.get_last_command()
        if last_cmd:
            console.print(f"[dim]Repeating: {last_cmd}[/dim]")
            return last_cmd
        else:
            console.print("[yellow]No previous command[/yellow]")
            return None
    
    # !-n - n commands ago
    match = re.match(r'^!-(\d+)$', query)
    if match:
        n = int(match.group(1))
        cmd = smart_history.replay_command(-n)
        if cmd:
            console.print(f"[dim]Repeating: {cmd}[/dim]")
            return cmd
        else:
            console.print(f"[yellow]No command at index -{n}[/yellow]")
            return None
    
    # !n - command at index n
    match = re.match(r'^!(\d+)$', query)
    if match:
        n = int(match.group(1))
        cmd = smart_history.replay_command(n)
        if cmd:
            console.print(f"[dim]Repeating: {cmd}[/dim]")
            return cmd
        else:
            console.print(f"[yellow]No command at index {n}[/yellow]")
            return None
    
    # !string - last command starting with string
    match = re.match(r'^!(.+)$', query)
    if match and not query.startswith('!!'):
        search_str = match.group(1)
        for entry in reversed(smart_history.history.history):
            cmd = entry.get('command', '')
            if cmd.startswith(search_str):
                console.print(f"[dim]Repeating: {cmd}[/dim]")
                return cmd
        console.print(f"[yellow]No command starting with '{search_str}'[/yellow]")
        return None
    
    return None


def analyze_command_patterns():
    """Analyze command usage patterns."""
    smart_history = SmartHistory()
    
    # Time-based analysis
    hourly_counts = {}
    for entry in smart_history.history.history:
        timestamp = entry.get('timestamp')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                hour = dt.hour
                hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
            except:
                pass
    
    if hourly_counts:
        console.print("\n[bold cyan]Command Usage by Hour:[/bold cyan]")
        for hour in sorted(hourly_counts.keys()):
            count = hourly_counts[hour]
            bar = "█" * (count // 2 or 1)
            console.print(f"  {hour:02d}:00 {bar} ({count})")
