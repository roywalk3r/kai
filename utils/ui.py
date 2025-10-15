"""UI helpers and formatting for Kai."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from typing import Optional

console = Console()

def print_banner():
    """Print the Kai welcome banner."""
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    
    # ASCII art logo
    logo = """
    ██╗  ██╗ █████╗ ██╗
    ██║ ██╔╝██╔══██╗██║
    █████╔╝ ███████║██║
    ██╔═██╗ ██╔══██║██║
    ██║  ██╗██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    """
    
    # Create styled text
    title = Text()
    title.append(logo, style="bold cyan")
    title.append("\n")
    title.append("AI-Powered Terminal Assistant", style="bold white")
    title.append("\n\n")
    title.append("✨ Transform natural language into commands", style="dim")
    title.append("\n")
    title.append("🛡️  Multi-layer safety protection", style="dim")
    title.append("\n")
    title.append("🎯 Context-aware and intelligent", style="dim")
    
    # Create panel
    panel = Panel(
        title,
        border_style="bright_cyan",
        box=box.DOUBLE,
        padding=(1, 2),
        subtitle="[dim]Type 'help' to get started | 'exit' to quit[/dim]",
        subtitle_align="center"
    )
    
    console.print(panel)
    console.print()

def print_first_time_welcome():
    """Print an enhanced welcome message."""
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    import time
    from datetime import datetime
    
    # Get current time for greeting
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
        emoji = "🌅"
    elif hour < 18:
        greeting = "Good Afternoon"
        emoji = "☀️"
    else:
        greeting = "Good Evening"
        emoji = "🌙"
    
    console.print()
    console.print(f"[bold bright_cyan]{emoji} {greeting}! Welcome to Kai![/bold bright_cyan]", justify="center")
    console.print()
    
    # Animated typing effect
    messages = [
        ("Initializing AI assistant", "cyan"),
        ("Loading context engine", "green"),
        ("Activating safety systems", "yellow"),
        ("Ready to assist!", "bright_green")
    ]
    
    for msg, color in messages:
        console.print(f"  [{color}]▸[/{color}] {msg}...", end="")
        time.sleep(0.2)
        console.print(f" [{color}]✓[/{color}]")
    
    console.print()
    
    # Feature highlights
    features = [
        Panel(
            "[bold cyan]🤖 Natural Language[/bold cyan]\n"
            "[dim]Just describe what you want:\n"
            "• list my files\n"
            "• create a backup\n"
            "• show disk usage[/dim]",
            border_style="cyan",
            padding=(1, 2)
        ),
        Panel(
            "[bold yellow]🛡️ Safety First[/bold yellow]\n"
            "[dim]Protected from:\n"
            "• Dangerous commands\n"
            "• Accidental deletions\n"
            "• Long-running tasks[/dim]",
            border_style="yellow",
            padding=(1, 2)
        ),
        Panel(
            "[bold green]⚡ Smart Features[/bold green]\n"
            "[dim]Includes:\n"
            "• Command history\n"
            "• Dry-run mode\n"
            "• Auto-suggestions[/dim]",
            border_style="green",
            padding=(1, 2)
        )
    ]
    
    console.print(Columns(features, equal=True, expand=True))
    console.print()
    
    # Quick start tips
    tips_panel = Panel(
        "[bold white]Quick Start Tips:[/bold white]\n\n"
        "[cyan]help[/cyan]          - Show all commands\n"
        "[cyan]examples[/cyan]      - See command examples\n"
        "[cyan]dry-run on[/cyan]    - Preview commands before running\n"
        "[cyan]history[/cyan]       - View your command history\n\n"
        "[dim italic]Try: 'list my files' or 'show system info'[/dim italic]",
        title="[bold bright_cyan]🚀 Get Started[/bold bright_cyan]",
        border_style="bright_cyan",
        padding=(1, 2)
    )
    
    console.print(tips_panel)
    console.print()
    console.print("[dim]═" * (console.width // 2) + "═[/dim]", justify="center")
    console.print()

def print_help():
    """Print help information."""
    help_text = """
# Kai Commands

## Natural Language
Just describe what you want to do:
- "list my files"
- "create a file called notes.txt"
- "show disk usage"
- "find all python files"

## Special Commands
- **exit/quit/q** - Exit Kai
- **terminate** - Stop currently running command
- **history [n]** - Show last n commands (default: 10)
- **clear-history** - Clear command history
- **config** - Show current configuration
- **config set <key> <value>** - Set configuration value
- **dry-run on/off** - Toggle dry-run mode
- **examples/suggestions** - Show example commands
- **welcome** - Show welcome screen again
- **help/?** - Show this help message
- **clear/cls** - Clear screen

## Configuration Options
- **timeout_seconds** - Command timeout (default: 20)
- **default_model** - AI model to use (default: llama3)
- **auto_confirm_safe** - Auto-confirm safe commands (default: false)
- **history_size** - Max history entries (default: 100)
- **dry_run** - Preview commands without executing (default: false)

## Examples
```
> list files sorted by size
> create a backup of my documents
> show me system information
> find TODO comments in python files
> compress the logs folder
> what's my IP address
```

## Tips
- Use **dry-run on** to preview commands before execution
- Use **history** to see your recent commands
- Type **examples** to see more command examples
- Commands are context-aware - you can refer to "the file" or "it"
    """
    console.print(Markdown(help_text))

def print_command(command: str):
    """Print a command with syntax highlighting."""
    console.print(f"[bold green]$ {command}[/bold green]")

def print_success(message: str):
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")

def print_error(message: str):
    """Print an error message."""
    console.print(f"[bold red]✗[/bold red] {message}", style="red")

def print_warning(message: str):
    """Print a warning message."""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}", style="yellow")

def print_info(message: str):
    """Print an info message."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}", style="blue")

def print_panel(content: str, title: Optional[str] = None, style: str = "cyan"):
    """Print content in a panel."""
    console.print(Panel(content, title=title, border_style=style))

def confirm(message: str, default: bool = False) -> bool:
    """Ask for user confirmation."""
    return Confirm.ask(message, default=default)

def prompt(message: str, default: str = "") -> str:
    """Prompt user for input."""
    if default:
        return Prompt.ask(message, default=default)
    return Prompt.ask(message)

def print_table(headers: list, rows: list, title: Optional[str] = None):
    """Print a formatted table."""
    table = Table(title=title)
    
    for header in headers:
        table.add_column(header, style="cyan")
    
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)

def print_code(code: str, language: str = "bash"):
    """Print code with syntax highlighting."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=False)
    console.print(syntax)

def clear_screen():
    """Clear the terminal screen."""
    console.clear()

def print_separator():
    """Print a separator line."""
    console.print("─" * console.width, style="dim")
