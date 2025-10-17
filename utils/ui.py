"""UI helpers and formatting for Prometheus."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from typing import Optional

console = Console()

def print_banner():
    """Print the Prometheus welcome banner."""
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    from rich.align import Align
    
    # Prometheus ASCII art with fire theme
    logo = Text()
    logo.append("\n", style="")
    logo.append("    ╔═══════════════════════════════════╗\n", style="bold bright_red")
    logo.append("    ║                                   ║\n", style="bold red")
    logo.append("    ║     ", style="bold red")
    logo.append("▓", style="bold bright_yellow on bright_yellow")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("▓", style="bold bright_yellow on bright_yellow")
    logo.append("           ", style="")
    logo.append("▓", style="bold bright_yellow on bright_yellow")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("▓", style="bold bright_yellow on bright_yellow")
    logo.append("     ║\n", style="bold red")
    logo.append("    ║    ", style="bold red")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("███", style="bold bright_white on red")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("       ", style="")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("███", style="bold bright_white on red")
    logo.append("▓▓", style="bold bright_red on bright_red")
    logo.append("    ║\n", style="bold red")
    logo.append("    ║       ", style="bold red")
    logo.append("███", style="bold bright_white on red")
    logo.append("       ", style="")
    logo.append("███", style="bold bright_white on red")
    logo.append("       ║\n", style="bold red")
    logo.append("    ║        ", style="bold red")
    logo.append("█", style="bold red")
    logo.append("         ", style="")
    logo.append("█", style="bold red")
    logo.append("        ║\n", style="bold red")
    logo.append("    ║   ", style="bold red")
    logo.append("╔═══════════════════════╗", style="bold bright_yellow")
    logo.append("   ║\n", style="bold red")
    logo.append("    ║   ║ ", style="bold red")
    logo.append("P R O M E T H E U S", style="bold bright_white on red")
    logo.append(" ║   ║\n", style="bold red")
    logo.append("    ║   ", style="bold red")
    logo.append("╚═══════════════════════╝", style="bold bright_yellow")
    logo.append("   ║\n", style="bold red")
    logo.append("    ║                                   ║\n", style="bold red")
    logo.append("    ╚═══════════════════════════════════╝\n", style="bold bright_red")
    logo.append("          ", style="")
    logo.append("⚡ IGNITE YOUR TERMINAL ⚡", style="italic bright_yellow blink")
    logo.append("\n", style="")
    
    # Create styled content
    content = Text()
    content.append(logo)
    content.append("\n")
    content.append("    AI-Powered Terminal Assistant", style="bold white")
    content.append("\n\n")
    content.append("    ✨ ", style="yellow")
    content.append("Transform natural language into commands", style="bright_white")
    content.append("\n")
    content.append("    🛡️  ", style="green")
    content.append("Multi-layer safety protection", style="bright_white")
    content.append("\n")
    content.append("    🎯 ", style="magenta")
    content.append("Context-aware and intelligent", style="bright_white")
    content.append("\n")
    content.append("    🧠 ", style="blue")
    content.append("Smart error detection & auto-fix", style="bright_white")
    
    # Create panel with gradient border
    panel = Panel(
        Align.center(content),
        border_style="bright_cyan",
        box=box.DOUBLE,
        padding=(1, 2),
        subtitle="[dim italic]Type [bold cyan]'help'[/bold cyan] to get started | [bold yellow]'exit'[/bold yellow] to quit[/dim italic]",
        subtitle_align="center"
    )
    
    console.print(panel)
    console.print()

def print_first_time_welcome():
    """Print an enhanced welcome message."""
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.align import Align
    import time
    from datetime import datetime
    
    # Get current time for greeting
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
        emoji = "🌅"
        color = "yellow"
    elif hour < 18:
        greeting = "Good Afternoon"
        emoji = "☀️"
        color = "bright_yellow"
    else:
        greeting = "Good Evening"
        emoji = "🌙"
        color = "bright_blue"
    
    # Greeting with style
    greeting_text = Text()
    greeting_text.append(f"{emoji} ", style=color)
    greeting_text.append(greeting, style=f"bold {color}")
    greeting_text.append("! Welcome to ", style="bold white")
    greeting_text.append("Prometheus", style="bold bright_red")
    greeting_text.append("!", style="bold white")
    
    console.print()
    console.print(Align.center(greeting_text))
    console.print()
    
    # Animated typing effect with better visuals
    messages = [
        ("Initializing AI assistant", "bright_cyan", "🤖"),
        ("Loading context engine", "bright_green", "⚙️"),
        ("Activating safety systems", "bright_yellow", "🛡️"),
        ("Ready to assist!", "bright_magenta", "✨")
    ]
    
    for msg, color, icon in messages:
        console.print(f"  [{color}]▸[/{color}] {icon}  {msg}...", end="")
        time.sleep(0.15)
        console.print(f" [{color}]✓[/{color}]")
    
    console.print()
    
    # Feature highlights with better styling
    features = [
        Panel(
            "[bold bright_cyan]🤖 Natural Language[/bold bright_cyan]\n\n"
            "[bright_white]Just describe what you want:[/bright_white]\n"
            "[cyan]▸[/cyan] [dim]list my files[/dim]\n"
            "[cyan]▸[/cyan] [dim]create a backup[/dim]\n"
            "[cyan]▸[/cyan] [dim]show disk usage[/dim]",
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold]Feature 1[/bold]",
            title_align="left"
        ),
        Panel(
            "[bold bright_yellow]🛡️ Safety First[/bold bright_yellow]\n\n"
            "[bright_white]Protected from:[/bright_white]\n"
            "[yellow]▸[/yellow] [dim]Dangerous commands[/dim]\n"
            "[yellow]▸[/yellow] [dim]Accidental deletions[/dim]\n"
            "[yellow]▸[/yellow] [dim]Long-running tasks[/dim]",
            border_style="bright_yellow",
            padding=(1, 2),
            title="[bold]Feature 2[/bold]",
            title_align="left"
        ),
        Panel(
            "[bold bright_green]⚡ Smart Features[/bold bright_green]\n\n"
            "[bright_white]Includes:[/bright_white]\n"
            "[green]▸[/green] [dim]Auto error fixing[/dim]\n"
            "[green]▸[/green] [dim]Command history[/dim]\n"
            "[green]▸[/green] [dim]Dry-run mode[/dim]",
            border_style="bright_green",
            padding=(1, 2),
            title="[bold]Feature 3[/bold]",
            title_align="left"
        )
    ]
    
    console.print(Columns(features, equal=True, expand=True))
    console.print()
    
    # Quick start tips with better formatting
    tips_content = Text()
    tips_content.append("Quick Start Commands:\n\n", style="bold bright_white")
    tips_content.append("  help", style="bold cyan")
    tips_content.append("          → Show all commands\n", style="dim")
    tips_content.append("  examples", style="bold cyan")
    tips_content.append("      → See command examples\n", style="dim")
    tips_content.append("  dry-run on", style="bold cyan")
    tips_content.append("    → Preview before running\n", style="dim")
    tips_content.append("  history", style="bold cyan")
    tips_content.append("       → View command history\n\n", style="dim")
    tips_content.append("💡 ", style="yellow")
    tips_content.append("Try: ", style="dim italic")
    tips_content.append("'list my files'", style="bright_cyan italic")
    tips_content.append(" or ", style="dim italic")
    tips_content.append("'show system info'", style="bright_cyan italic")
    
    tips_panel = Panel(
        tips_content,
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
# Prometheus Commands

## Natural Language
Just describe what you want to do:
- "list my files"
- "create a file called notes.txt"
- "show disk usage"
- "find all python files"

## Special Commands
- **exit/quit/q** - Exit Prometheus
- **terminate** - Stop currently running command
- **help/?** - Show this help message
- **clear/cls** - Clear screen
- **welcome** - Show welcome screen again

## History Commands
- **history [n]** - Show last n commands (default: 10)
- **clear-history** - Clear command history
- **stats** - Show command usage statistics
- **!!** - Repeat last command
- **!n** - Repeat command at index n
- **!-n** - Repeat n commands ago
- **!string** - Repeat last command starting with string

## Quick Actions
- **--shorten <url>** - Shorten a URL
- **--qr <text>** - Generate QR code
- **--hash <text>** - Generate hash (MD5, SHA1, SHA256, SHA512)
- **--encode <type> <text>** - Encode text (base64, hex, url)
- **--decode <type> <text>** - Decode text
- **--time [location]** - Show world time
- **--calc <expression>** - Calculate math expression

## Search & Navigation
- **find <pattern>** - Fuzzy find files
- **grep <pattern>** - Search in files
- **search <name>** - Find function/class in codebase
- **analyze** - Analyze current project

## Context Commands
- **status** - Show quick directory status
- **ref/reference** - Show context-relevant commands

## AI Model Management 🆕
- **model** - Show current AI model
- **use gemini** - Switch to Google Gemini AI
- **use ollama** - Switch to local Ollama

## Configuration
- **config** - Show current configuration
- **config set <key> <value>** - Set configuration value
- **dry-run on/off** - Toggle dry-run mode
- **examples/suggestions** - Show example commands

## Plugin System
- **plugin list** - List installed plugins
- **plugin install <name>** - Install a plugin
- **plugin uninstall <name>** - Uninstall a plugin
- **plugin create <name>** - Create plugin template

## Alias System 🆕
- **alias** - List all aliases
- **alias add <name> <command>** - Create command alias
- **alias remove <name>** - Remove alias
- **alias import** - Import aliases from shell

## Template System 🆕
- **template list** - List available templates
- **template show <name>** - Show template details
- **template use <name> [params]** - Execute template

## Workflow Automation 🆕
- **workflow list** - List all workflows
- **workflow show <name>** - Show workflow details
- **workflow run <name>** - Execute workflow

## Remote Execution 🆕
- **remote list** - List configured hosts
- **remote add <name> <user@host>** - Add remote host
- **remote exec <host> <command>** - Execute on remote
- **remote test <host>** - Test connection

## Session Management 🆕
- **session info** - Show session statistics
- **session clear** - Clear session context
- **doctor** - Run health check

## Cache Management 🆕
- **cache stats** - Show cache statistics
- **cache clear** - Clear all cache
- **cache clean** - Remove expired entries

## Advanced History 🆕
- **history ui** - Interactive history browser
- **history failed** - Show failed commands only
- **history analysis** - Analyze usage patterns

## Watch & Timing ⚡ NEW
- **watch <command>** - Monitor command output (refreshes every 2s)
- **watch --interval 5 <cmd>** - Custom refresh interval
- **watch --until-change <cmd>** - Stop when output changes
- **time <command>** - Time command execution
- **benchmark <command> [runs]** - Run multiple times, show stats

## Bookmarks 📌 NEW
- **bookmarks** - List all directory bookmarks
- **bookmark add <name> <path>** - Save directory bookmark
- **bookmark remove <name>** - Remove bookmark
- **jump <name>** - Jump to bookmarked directory

## Notes 📝 NEW
- **notes** - Show notes for current directory
- **note "<text>"** - Add a note
- **notes clear** - Clear all notes for directory
- **notes search <query>** - Search all notes

## Favorites ⭐ NEW
- **favorites** - List all favorite commands
- **favorite add <name> <command>** - Save favorite command
- **favorite remove <name>** - Remove favorite
- **fav <name>** - Run favorite command

## Configuration Options
- **timeout_seconds** - Command timeout (default: 20)
- **default_model** - AI model to use (default: llama3)
- **auto_confirm_safe** - Auto-confirm safe commands (default: false)
- **history_size** - Max history entries (default: 100)
- **dry_run** - Preview commands without executing (default: false)

## Keyboard Shortcuts
- **Ctrl+Space** - Auto-complete paths/commands
- **Ctrl+X Ctrl+E** - Edit command in $EDITOR
- **Alt+E** - Explain last command
- **Ctrl+L** - Clear screen (keep command)
- **Alt+H** - Show keyboard shortcuts help
- **Ctrl+R** - Search command history
- **Ctrl+D** - Exit Prometheus
- **Ctrl+C** - Cancel current input

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

def confirm(message: str, default: bool = True) -> bool:
    """Ask for user confirmation."""
    return Confirm.ask(message, default=default)

def print_ai_response(message: str):
    """Print AI response with beautiful styling."""
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    
    # Check if it's a simple message or needs markdown
    if len(message) < 200 and '\n' not in message:
        # Short response - use simple panel
        response_text = Text()
        response_text.append("💬 ", style="bright_cyan")
        response_text.append(message, style="bright_white")
        
        panel = Panel(
            response_text,
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_cyan]Prometheus[/bold bright_cyan]",
            title_align="left"
        )
        console.print(panel)
    else:
        # Long response - use markdown
        panel = Panel(
            Markdown(message),
            border_style="bright_cyan",
            padding=(1, 2),
            title="[bold bright_cyan]💬 Prometheus[/bold bright_cyan]",
            title_align="left"
        )
        console.print(panel)
    console.print()

def print_command_suggestion(command: str, explanation: str = None):
    """Print a command suggestion with styling."""
    from rich.panel import Panel
    from rich.syntax import Syntax
    
    content = ""
    if explanation:
        content = f"[bright_white]{explanation}[/bright_white]\n\n"
    
    content += f"[bold bright_green]Command:[/bold bright_green]\n[bright_cyan]{command}[/bright_cyan]"
    
    panel = Panel(
        content,
        border_style="bright_green",
        padding=(1, 2),
        title="[bold bright_green]🎯 Suggested Command[/bold bright_green]",
        title_align="left"
    )
    console.print(panel)
    console.print()

def prompt(message: str, default: str = "") -> str:
    """Prompt user for input."""
    if default:
        return Prompt.ask(message, default=default)
    return Prompt.ask(message)

def print_code_diff(diff: str):
    """Print code diff with syntax highlighting."""
    from rich.syntax import Syntax
    syntax = Syntax(diff, "diff", theme="monokai", line_numbers=False)
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
