#!/usr/bin/env python3
"""
Interactive history browser with rich UI.
"""

from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import HTML
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class InteractiveHistoryBrowser:
    """Interactive terminal UI for browsing command history."""
    
    def __init__(self, history_items: List[Dict]):
        """
        Initialize browser.
        
        Args:
            history_items: List of history entries with command, timestamp, success, output
        """
        self.history_items = history_items
        self.selected_index = len(history_items) - 1 if history_items else 0
        self.filter_text = ""
        self.show_failed_only = False
        self.result = None
    
    def get_filtered_items(self) -> List[Dict]:
        """Get filtered history items."""
        items = self.history_items
        
        # Filter by failed status
        if self.show_failed_only:
            items = [item for item in items if not item.get("success", True)]
        
        # Filter by search text
        if self.filter_text:
            items = [
                item for item in items
                if self.filter_text.lower() in item.get("command", "").lower()
            ]
        
        return items
    
    def get_display_text(self) -> str:
        """Generate display text for current state."""
        filtered_items = self.get_filtered_items()
        
        if not filtered_items:
            return "No history items found"
        
        # Ensure selected index is valid
        if self.selected_index >= len(filtered_items):
            self.selected_index = len(filtered_items) - 1
        if self.selected_index < 0:
            self.selected_index = 0
        
        lines = []
        lines.append("=" * 80)
        lines.append("COMMAND HISTORY BROWSER")
        lines.append("=" * 80)
        lines.append("")
        
        # Show filter info
        if self.show_failed_only:
            lines.append("[Filter: Failed commands only]")
        if self.filter_text:
            lines.append(f"[Search: {self.filter_text}]")
        lines.append(f"Showing {len(filtered_items)} of {len(self.history_items)} commands")
        lines.append("")
        
        # Show items around selection (5 before, 5 after)
        start_idx = max(0, self.selected_index - 5)
        end_idx = min(len(filtered_items), self.selected_index + 6)
        
        for i in range(start_idx, end_idx):
            item = filtered_items[i]
            command = item.get("command", "")
            success = item.get("success", True)
            timestamp = item.get("timestamp", "")
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = timestamp[:8] if timestamp else ""
            
            # Status icon
            status = "✓" if success else "✗"
            
            # Truncate long commands
            if len(command) > 60:
                command = command[:57] + "..."
            
            # Highlight selected
            if i == self.selected_index:
                lines.append(f"> [{status}] {time_str} | {command}")
            else:
                lines.append(f"  [{status}] {time_str} | {command}")
        
        lines.append("")
        lines.append("=" * 80)
        
        # Show details of selected item
        if filtered_items:
            selected = filtered_items[self.selected_index]
            lines.append("SELECTED COMMAND DETAILS:")
            lines.append(f"Command: {selected.get('command', '')}")
            lines.append(f"Status: {'Success' if selected.get('success') else 'Failed'}")
            lines.append(f"Timestamp: {selected.get('timestamp', '')}")
            
            output = selected.get("output", "")
            if output:
                lines.append(f"Output: {output[:200]}...")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("Controls: ↑/↓ Navigate | Enter Run | F Fix | E Explain | / Search | Q Quit")
        
        return "\n".join(lines)
    
    def run(self) -> Optional[Dict]:
        """
        Run the interactive browser.
        
        Returns:
            Selected action and item, or None if cancelled
        """
        kb = KeyBindings()
        
        @kb.add('up')
        def move_up(event):
            if self.selected_index > 0:
                self.selected_index -= 1
        
        @kb.add('down')
        def move_down(event):
            filtered = self.get_filtered_items()
            if self.selected_index < len(filtered) - 1:
                self.selected_index += 1
        
        @kb.add('enter')
        def select_item(event):
            filtered = self.get_filtered_items()
            if filtered:
                self.result = {"action": "run", "item": filtered[self.selected_index]}
                event.app.exit()
        
        @kb.add('f')
        def fix_command(event):
            filtered = self.get_filtered_items()
            if filtered:
                self.result = {"action": "fix", "item": filtered[self.selected_index]}
                event.app.exit()
        
        @kb.add('e')
        def explain_command(event):
            filtered = self.get_filtered_items()
            if filtered:
                self.result = {"action": "explain", "item": filtered[self.selected_index]}
                event.app.exit()
        
        @kb.add('q')
        def quit_browser(event):
            event.app.exit()
        
        @kb.add('c-c')
        def cancel(event):
            event.app.exit()
        
        # Layout
        text_control = FormattedTextControl(
            text=lambda: self.get_display_text()
        )
        
        window = Window(content=text_control)
        layout = Layout(HSplit([window]))
        
        # Application
        app = Application(
            layout=layout,
            key_bindings=kb,
            full_screen=True
        )
        
        app.run()
        return self.result


def show_history_ui(history_items: List[Dict]) -> Optional[Dict]:
    """
    Show interactive history UI.
    
    Args:
        history_items: List of history entries
    
    Returns:
        User action or None
    """
    if not history_items:
        console = Console()
        console.print("[yellow]No history items to display[/yellow]")
        return None
    
    try:
        browser = InteractiveHistoryBrowser(history_items)
        return browser.run()
    except Exception as e:
        # Fallback to simple table if interactive fails
        show_history_table(history_items)
        return None


def show_history_table(history_items: List[Dict], limit: int = 20):
    """Display history in a simple table format."""
    console = Console()
    
    if not history_items:
        console.print("[yellow]No command history[/yellow]")
        return
    
    table = Table(title="Command History", border_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Time", style="dim")
    table.add_column("Status", justify="center")
    table.add_column("Command", style="bright_white")
    
    # Show most recent first
    recent_items = history_items[-limit:]
    
    for i, item in enumerate(reversed(recent_items), 1):
        command = item.get("command", "")
        success = item.get("success", True)
        timestamp = item.get("timestamp", "")
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%H:%M")
        except:
            time_str = timestamp[:5] if timestamp else ""
        
        # Status
        if success:
            status = "[green]✓[/green]"
        else:
            status = "[red]✗[/red]"
        
        # Truncate long commands
        if len(command) > 60:
            command = command[:57] + "..."
        
        table.add_row(str(i), time_str, status, command)
    
    console.print(table)
    console.print(f"\n[dim]Showing {len(recent_items)} of {len(history_items)} commands[/dim]")


def show_failed_commands(history_items: List[Dict]):
    """Show only failed commands."""
    failed = [item for item in history_items if not item.get("success", True)]
    
    console = Console()
    
    if not failed:
        console.print("[green]✓ No failed commands in history[/green]")
        return
    
    console.print(Panel(
        f"[bold red]{len(failed)} Failed Command(s)[/bold red]",
        border_style="red"
    ))
    
    table = Table(border_style="red")
    table.add_column("Time", style="dim")
    table.add_column("Command", style="bright_white")
    table.add_column("Error", style="red")
    
    for item in failed[-10:]:  # Last 10 failed
        timestamp = item.get("timestamp", "")
        command = item.get("command", "")
        output = item.get("output", "")
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%H:%M")
        except:
            time_str = ""
        
        # Extract error from output
        error_msg = output[:50] + "..." if len(output) > 50 else output
        
        table.add_row(time_str, command, error_msg)
    
    console.print(table)
    console.print("\n[dim]Use 'prom --fix' to get AI-powered fix suggestions[/dim]")


def analyze_history_patterns(history_items: List[Dict]) -> Dict:
    """Analyze patterns in command history."""
    if not history_items:
        return {}
    
    # Count commands
    command_counts = {}
    success_counts = {}
    failure_counts = {}
    hourly_usage = [0] * 24
    
    for item in history_items:
        command = item.get("command", "").split()[0]
        success = item.get("success", True)
        timestamp = item.get("timestamp", "")
        
        # Count command usage
        command_counts[command] = command_counts.get(command, 0) + 1
        
        # Count successes/failures
        if success:
            success_counts[command] = success_counts.get(command, 0) + 1
        else:
            failure_counts[command] = failure_counts.get(command, 0) + 1
        
        # Hourly usage
        try:
            dt = datetime.fromisoformat(timestamp)
            hourly_usage[dt.hour] += 1
        except:
            pass
    
    # Find most used
    most_used = sorted(command_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Find most failed
    most_failed = sorted(failure_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Peak hour
    peak_hour = hourly_usage.index(max(hourly_usage)) if hourly_usage else 0
    
    return {
        "total_commands": len(history_items),
        "unique_commands": len(command_counts),
        "most_used": most_used,
        "most_failed": most_failed,
        "peak_hour": peak_hour,
        "success_rate": sum(1 for item in history_items if item.get("success", True)) / len(history_items) * 100
    }


def show_history_analysis(history_items: List[Dict]):
    """Display history analysis."""
    console = Console()
    analysis = analyze_history_patterns(history_items)
    
    if not analysis:
        console.print("[yellow]Not enough history data[/yellow]")
        return
    
    # Overview
    console.print(Panel(
        f"[bold bright_cyan]Total Commands:[/bold bright_cyan] {analysis['total_commands']}\n"
        f"[bold bright_cyan]Unique Commands:[/bold bright_cyan] {analysis['unique_commands']}\n"
        f"[bold bright_cyan]Success Rate:[/bold bright_cyan] {analysis['success_rate']:.1f}%\n"
        f"[bold bright_cyan]Peak Hour:[/bold bright_cyan] {analysis['peak_hour']}:00",
        title="[bold]History Analysis[/bold]",
        border_style="cyan"
    ))
    
    # Most used commands
    if analysis['most_used']:
        console.print("\n[bold]Most Used Commands:[/bold]")
        table = Table(border_style="cyan")
        table.add_column("Command", style="cyan")
        table.add_column("Count", justify="right", style="bright_white")
        
        for cmd, count in analysis['most_used']:
            table.add_row(cmd, str(count))
        
        console.print(table)
    
    # Most failed commands
    if analysis['most_failed']:
        console.print("\n[bold]Most Failed Commands:[/bold]")
        table = Table(border_style="red")
        table.add_column("Command", style="red")
        table.add_column("Failures", justify="right", style="bright_white")
        
        for cmd, count in analysis['most_failed']:
            table.add_row(cmd, str(count))
        
        console.print(table)
