"""Enhanced keyboard shortcuts and bindings for Prometheus."""

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app
from rich.console import Console
import subprocess
import os

console = Console()


def create_key_bindings(session_state: dict) -> KeyBindings:
    """Create custom key bindings for Prometheus."""
    kb = KeyBindings()
    
    # Ctrl+Space: Auto-complete paths/commands
    @kb.add('c-space')
    def _(event):
        """Trigger auto-completion."""
        buffer = event.current_buffer
        buffer.start_completion()
    
    # Ctrl+X Ctrl+E: Edit command in $EDITOR
    @kb.add('c-x', 'c-e')
    def _(event):
        """Edit command in external editor."""
        import tempfile
        buffer = event.current_buffer
        
        # Get current text
        text = buffer.text
        
        # Create temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(text)
            temp_file = f.name
        
        # Open in editor
        editor = os.environ.get('EDITOR', 'nano')
        try:
            subprocess.run([editor, temp_file])
            
            # Read back the edited text
            with open(temp_file, 'r') as f:
                new_text = f.read().strip()
            
            # Update buffer
            buffer.text = new_text
            buffer.cursor_position = len(new_text)
        finally:
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass
    
    # Alt+E: Explain last command
    @kb.add('escape', 'e')
    def _(event):
        """Explain the last command."""
        from core.history import get_history
        history = get_history()
        
        if history.history:
            last_entry = history.history[-1]
            last_cmd = last_entry.get('command', '')
            
            if last_cmd:
                # Set buffer to explain command
                buffer = event.current_buffer
                buffer.text = f"explain {last_cmd}"
                buffer.cursor_position = len(buffer.text)
                console.print("[dim]💡 Explaining last command...[/dim]")
    
    # Ctrl+L: Clear screen but keep command
    @kb.add('c-l')
    def _(event):
        """Clear screen."""
        console.clear()
        from utils.ui import print_banner
        print_banner()
    
    # Alt+H: Show quick help
    @kb.add('escape', 'h')
    def _(event):
        """Show quick keyboard shortcuts help."""
        from rich.panel import Panel
        help_text = """[bold cyan]Keyboard Shortcuts:[/bold cyan]

[yellow]Ctrl+Space[/yellow]      Auto-complete paths/commands
[yellow]Ctrl+X Ctrl+E[/yellow]   Edit command in $EDITOR
[yellow]Alt+E[/yellow]           Explain last command
[yellow]Ctrl+L[/yellow]          Clear screen (keep command)
[yellow]Alt+H[/yellow]           Show this help
[yellow]Ctrl+R[/yellow]          Search command history
[yellow]Ctrl+D[/yellow]          Exit Prometheus
[yellow]Ctrl+C[/yellow]          Cancel current input
"""
        console.print(Panel(
            help_text,
            border_style="bright_cyan",
            title="[bold bright_cyan]⌨️  Keyboard Shortcuts[/bold bright_cyan]",
            title_align="left"
        ))
    
    # Ctrl+R: Search history (enhanced)
    @kb.add('c-r')
    def _(event):
        """Enhanced history search."""
        console.print("[dim]🔍 History search mode - type to filter...[/dim]")
        # The default Ctrl+R behavior will kick in
    
    return kb


def setup_multiline_support():
    """Configure multi-line input support."""
    # This is handled by prompt_toolkit's multiline parameter
    return {
        'multiline': False,  # Can be toggled with Meta+Enter
        'enable_history_search': True,
        'complete_while_typing': True,
    }


def create_toolbar(session_state: dict) -> str:
    """Create a toolbar for the bottom of the terminal."""
    from core.config import get_config
    config = get_config()
    
    # Get current mode info
    dry_run = config.get("dry_run", False)
    
    toolbar_items = []
    
    if dry_run:
        toolbar_items.append("[DRY-RUN]")
    
    toolbar_items.append("Ctrl+L: Clear")
    toolbar_items.append("Alt+H: Help")
    toolbar_items.append("Ctrl+D: Exit")
    
    return " | ".join(toolbar_items)


def handle_clipboard_paste(text: str) -> str:
    """Handle multi-line clipboard paste."""
    # Strip common issues from pasted text
    text = text.strip()
    
    # If multi-line, ask user if they want to execute all lines
    lines = text.split('\n')
    if len(lines) > 1:
        console.print(f"[yellow]⚠️  Pasted {len(lines)} lines[/yellow]")
        console.print("[dim]Multi-line execution not yet supported. Using first line only.[/dim]")
        return lines[0]
    
    return text
