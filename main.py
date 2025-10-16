#!/usr/bin/env python3
"""
Kai - Intelligent Terminal Assistant
Main entry point for the application.
"""

import sys
import argparse
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pathlib import Path

from ai.model import ask_ai
from ai.context import get_conversation_context
from core.executor import execute_command, terminate_process
from core.config import get_config
from core.history import get_history
from utils.ui import (
    print_banner, print_help, print_error, print_warning,
    print_info, print_success, confirm, console, print_first_time_welcome,
    print_ai_response
)
from utils.safety import SafetyLevel
from utils.suggestions import format_suggestions_help
from rich.markdown import Markdown

def handle_special_command(query: str) -> bool:
    """
    Handle special built-in commands.
    
    Returns:
        True if command was handled, False otherwise
    """
    config = get_config()
    history = get_history()
    
    # Exit commands
    if query in ["exit", "quit", "q"]:
        console.print("[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    
    # Terminate running process
    elif query == "terminate":
        terminate_process()
        return True
    
    # Help
    elif query in ["help", "?"]:
        print_help()
        return True
    
    # Examples/Suggestions
    elif query in ["examples", "suggestions"]:
        console.print(Markdown(format_suggestions_help()))
        return True
    
    # History commands
    elif query == "history":
        console.print(history.display())
        return True
    
    elif query.startswith("history "):
        try:
            n = int(query.split()[1])
            console.print(history.display(n))
        except (ValueError, IndexError):
            print_error("Usage: history [n]")
        return True
    
    elif query == "clear-history":
        if confirm("Clear all command history?", default=False):
            history.clear()
            print_success("History cleared")
        return True
    
    # Configuration commands
    elif query == "config":
        console.print(config.display())
        return True
    
    elif query.startswith("config set "):
        try:
            parts = query.split(maxsplit=2)
            if len(parts) < 3:
                print_error("Usage: config set <key> <value>")
            else:
                key, value = parts[1], parts[2]
                # Try to parse value as int or bool
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                elif value.isdigit():
                    value = int(value)
                config.set(key, value)
                config.save()
                print_success(f"Set {key} = {value}")
        except Exception as e:
            print_error(f"Error setting config: {e}")
        return True
    
    # Dry-run mode toggle
    elif query in ["dry-run on", "dryrun on"]:
        config.set("dry_run", True)
        config.save()
        print_info("Dry-run mode enabled")
        return True
    
    elif query in ["dry-run off", "dryrun off"]:
        config.set("dry_run", False)
        config.save()
        print_info("Dry-run mode disabled")
        return True
    
    # Clear screen
    elif query in ["clear", "cls"]:
        console.clear()
        return True
    
    # Show welcome screen
    elif query == "welcome":
        print_first_time_welcome()
        return True
    
    return False

def main():
    """Main application loop."""
    # Initialize
    config = get_config()
    history = get_history()
    conv_context = get_conversation_context()
    
    # Setup prompt with history
    kai_dir = Path.home() / ".kai"
    kai_dir.mkdir(exist_ok=True)
    
    # Create custom prompt with style
    from prompt_toolkit.formatted_text import HTML
    
    def get_prompt():
        return HTML('<ansibrightcyan><b>kai</b></ansibrightcyan> <ansiyellow>❯</ansiyellow> ')
    
    session = PromptSession(
        message=get_prompt,
        history=FileHistory(str(kai_dir / "prompt_history")),
        auto_suggest=AutoSuggestFromHistory(),
    )
    
    # Print banner
    print_banner()
    
    # Show enhanced welcome screen every time
    print_first_time_welcome()
    
    # Show AI model status
    from ai.gemini_model import is_gemini_available
    if is_gemini_available():
        print_info("🤖 Using Gemini AI (Google)")
    else:
        print_info("🤖 Using Ollama (Local AI)")
        print_warning("💡 Tip: Set GEMINI_API_KEY environment variable to use Gemini")
    
    # Check if dry-run mode is enabled
    if config.get("dry_run", False):
        print_warning("Dry-run mode is enabled")
    
    # Main loop
    while True:
        try:
            # Get user input with styled prompt
            query = session.prompt().strip()
            
            if not query:
                continue
            
            # Handle special commands
            if handle_special_command(query):
                continue
            
            # Ask AI to interpret the query
            response = ask_ai(query)
            
            # Handle different response types
            if response["intent"] == "error":
                print_error(response["message"])
                continue
            
            elif response["intent"] == "explain":
                print_ai_response(response["message"])
                continue
            
            elif response["intent"] == "run":
                command = response["command"]
                warning = response.get("warning")
                safety_level = response.get("safety_level", SafetyLevel.SAFE)
                
                # Check if command is interactive (vim, nano, etc.)
                from utils.safety import is_interactive_command
                is_interactive = is_interactive_command(command)
                
                # Show warning if present
                if warning:
                    from rich.panel import Panel
                    
                    # Style warning based on safety level
                    if safety_level == SafetyLevel.DANGEROUS:
                        warning_panel = Panel(
                            f"[bold red]⚠️  DANGER![/bold red]\n\n"
                            f"[bright_white]{warning}[/bright_white]\n\n"
                            f"[dim]This command could be destructive![/dim]",
                            border_style="red",
                            title="[bold red]⚠️  Warning[/bold red]",
                            title_align="left",
                            padding=(1, 2)
                        )
                        console.print(warning_panel)
                        
                        if not confirm("[bold red]Are you SURE you want to run this?[/bold red]", default=False):
                            print_info("Command cancelled")
                            continue
                    else:
                        warning_panel = Panel(
                            f"[bright_white]{warning}[/bright_white]",
                            border_style="yellow",
                            title="[bold yellow]⚠️  Warning[/bold yellow]",
                            title_align="left",
                            padding=(1, 2)
                        )
                        console.print(warning_panel)
                        
                        if not confirm("[yellow]Proceed?[/yellow]", default=True):
                            print_info("Command cancelled")
                            continue
                
                # Execute command
                dry_run = config.get("dry_run", False)
                
                # If interactive, inform user and run without capture
                if is_interactive and not dry_run:
                    print_info("Running interactive command...")
                    success, output = execute_command(command, dry_run=dry_run, interactive=True)
                else:
                    success, output = execute_command(command, dry_run=dry_run, interactive=False)
                
                # Add to history and conversation context
                if not dry_run:
                    history.add(query, command, success, output)
                    conv_context.add_interaction(query, command, output)
            
            else:
                print_error(f"Unknown intent: {response['intent']}")
        
        except KeyboardInterrupt:
            console.print("\n[dim]Use 'exit' or 'quit' to exit[/dim]")
            continue
        
        except EOFError:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break
        
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}")
            continue

def execute_one_shot(query: str):
    """Execute a single query and exit."""
    from rich.panel import Panel
    
    # Show what we're processing
    console.print(Panel(
        f"[bright_cyan]💬 {query}[/bright_cyan]",
        border_style="bright_cyan",
        title="[bold bright_cyan]Query[/bold bright_cyan]",
        title_align="left",
        padding=(0, 1)
    ))
    console.print()
    
    # Get AI response
    response = ask_ai(query)
    
    # Handle different response types
    if response["intent"] == "error":
        print_error(response["message"])
        sys.exit(1)
    
    elif response["intent"] == "explain":
        print_ai_response(response["message"])
        sys.exit(0)
    
    elif response["intent"] == "run":
        command = response["command"]
        warning = response.get("warning")
        safety_level = response.get("safety_level", SafetyLevel.SAFE)
        
        # Check if command is interactive
        from utils.safety import is_interactive_command
        is_interactive = is_interactive_command(command)
        
        # Show warning if present
        if warning:
            from rich.panel import Panel
            
            if safety_level == SafetyLevel.DANGEROUS:
                warning_panel = Panel(
                    f"[bold red]⚠️  DANGER![/bold red]\n\n"
                    f"[bright_white]{warning}[/bright_white]\n\n"
                    f"[dim]This command could be destructive![/dim]",
                    border_style="red",
                    title="[bold red]⚠️  Warning[/bold red]",
                    title_align="left",
                    padding=(1, 2)
                )
                console.print(warning_panel)
                
                if not confirm("[bold red]Are you SURE you want to run this?[/bold red]", default=False):
                    console.print("[yellow]Command cancelled[/yellow]")
                    sys.exit(0)
            else:
                warning_panel = Panel(
                    f"[bright_white]{warning}[/bright_white]",
                    border_style="yellow",
                    title="[bold yellow]⚠️  Warning[/bold yellow]",
                    title_align="left",
                    padding=(1, 2)
                )
                console.print(warning_panel)
                
                if not confirm("[yellow]Proceed?[/yellow]", default=True):
                    console.print("[yellow]Command cancelled[/yellow]")
                    sys.exit(0)
        
        # Execute command
        config = get_config()
        dry_run = config.get("dry_run", False)
        
        if is_interactive and not dry_run:
            print_info("Running interactive command...")
            success, output = execute_command(command, dry_run=dry_run, interactive=True)
        else:
            success, output = execute_command(command, dry_run=dry_run, interactive=False)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    
    else:
        print_error(f"Unknown intent: {response['intent']}")
        sys.exit(1)

def handle_subcommand(subcommand: str, args: list):
    """Handle subcommands like update, uninstall, config, etc."""
    import subprocess
    import os
    from rich.panel import Panel
    
    if subcommand == "update":
        console.print(Panel(
            "[bold bright_cyan]Updating Kai...[/bold bright_cyan]",
            border_style="bright_cyan"
        ))
        
        # Determine installation directory
        script_dir = Path(__file__).parent.absolute()
        
        try:
            # Git pull
            result = subprocess.run(
                ["git", "pull"],
                cwd=script_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✓ Updated from git[/green]")
                console.print(result.stdout)
                
                # Update dependencies
                console.print("\n[cyan]Updating dependencies...[/cyan]")
                venv_pip = script_dir / ".venv" / "bin" / "pip"
                subprocess.run(
                    [str(venv_pip), "install", "-r", "requirements.txt", "--upgrade"],
                    cwd=script_dir
                )
                console.print("[green]✓ Dependencies updated[/green]")
                console.print("\n[bold green]✅ Kai updated successfully![/bold green]")
            else:
                console.print(f"[red]❌ Update failed: {result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
    
    elif subcommand == "uninstall":
        console.print(Panel(
            "[bold red]⚠️  Uninstalling Kai[/bold red]\n\n"
            "[bright_white]This will remove Kai from your system.[/bright_white]\n"
            "[dim]Your configuration in ~/.kai will be preserved.[/dim]",
            border_style="red",
            title="[bold red]Uninstall[/bold red]"
        ))
        
        if not confirm("[red]Are you sure?[/red]", default=False):
            console.print("[yellow]Uninstall cancelled[/yellow]")
            return
        
        script_dir = Path(__file__).parent.absolute()
        uninstall_script = script_dir / "uninstall.sh"
        
        if uninstall_script.exists():
            os.system(f"bash {uninstall_script}")
        else:
            console.print("[red]❌ Uninstall script not found[/red]")
    
    elif subcommand == "config":
        if args and args[0] == "edit":
            # Open config in editor
            config_file = Path.home() / ".kai" / "config.json"
            editor = os.environ.get("EDITOR", "nano")
            os.system(f"{editor} {config_file}")
        elif args and args[0] == "reset":
            # Reset config to defaults
            if confirm("[yellow]Reset configuration to defaults?[/yellow]", default=False):
                config = get_config()
                config.config = config.DEFAULT_CONFIG.copy()
                config.save()
                console.print("[green]✓ Configuration reset[/green]")
        elif args and args[0] == "show":
            # Show config
            config = get_config()
            from rich.table import Table
            table = Table(title="Kai Configuration", border_style="cyan")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="bright_white")
            for key, value in config.config.items():
                table.add_row(key, str(value))
            console.print(table)
        else:
            # Show config location
            config_file = Path.home() / ".kai" / "config.json"
            console.print(Panel(
                f"[bold bright_white]Configuration File:[/bold bright_white]\n"
                f"[bright_cyan]{config_file}[/bright_cyan]\n\n"
                f"[bold]Commands:[/bold]\n"
                f"[cyan]kai config show[/cyan]   - Show current config\n"
                f"[cyan]kai config edit[/cyan]   - Edit config file\n"
                f"[cyan]kai config reset[/cyan]  - Reset to defaults",
                border_style="bright_cyan",
                title="[bold bright_cyan]Configuration[/bold bright_cyan]"
            ))
    
    elif subcommand == "history":
        if args and args[0] == "clear":
            if confirm("[yellow]Clear command history?[/yellow]", default=False):
                history = get_history()
                history.history = []
                history.save()
                console.print("[green]✓ History cleared[/green]")
        elif args and args[0] == "export":
            # Export history to file
            filename = args[1] if len(args) > 1 else "kai_history.json"
            history = get_history()
            import json
            with open(filename, 'w') as f:
                json.dump(history.history, f, indent=2)
            console.print(f"[green]✓ History exported to {filename}[/green]")
        else:
            # Show history
            history = get_history()
            from rich.table import Table
            table = Table(title="Command History", border_style="cyan")
            table.add_column("#", style="dim")
            table.add_column("Query", style="bright_white")
            table.add_column("Command", style="cyan")
            table.add_column("Success", style="green")
            
            for i, entry in enumerate(history.history[-20:], 1):
                table.add_row(
                    str(i),
                    entry.get("query", "")[:50],
                    entry.get("command", "")[:50],
                    "✓" if entry.get("success") else "✗"
                )
            console.print(table)
    
    elif subcommand == "info":
        # Show system info
        from rich.table import Table
        import platform
        
        table = Table(title="Kai System Information", border_style="bright_cyan")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="bright_white")
        
        script_dir = Path(__file__).parent.absolute()
        table.add_row("Version", "1.0.0")
        table.add_row("Install Location", str(script_dir))
        table.add_row("Config Directory", str(Path.home() / ".kai"))
        table.add_row("Python Version", platform.python_version())
        table.add_row("Platform", platform.platform())
        
        # Check AI model
        from ai.gemini_model import is_gemini_available
        if is_gemini_available():
            table.add_row("AI Model", "Gemini (Google)")
        else:
            table.add_row("AI Model", "Ollama (Local)")
        
        console.print(table)
    
    else:
        console.print(f"[red]Unknown subcommand: {subcommand}[/red]")
        console.print("Run [cyan]kai --help[/cyan] for available commands")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Kai - AI-Powered Terminal Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Modes:

1. Interactive Mode:
  kai                    Start interactive session

2. One-Shot Mode (NEW!):
  kai "query"            Execute a single query and exit
  
  Examples:
    kai "list my files"
    kai "update my system"
    kai "show disk usage"
    kai "create a backup of my documents"

3. Subcommands:
  kai update             Update Kai to the latest version
  kai uninstall          Uninstall Kai from the system
  kai config [show|edit|reset]  Manage configuration
  kai history [clear|export]    Manage command history
  kai info               Show system information

More Examples:
  kai --version          Show version information
  kai --dry-run          Enable preview mode
  kai "find python files" --dry-run  Preview without executing

For more information, visit: https://github.com/roywalk3r/kai
        """
    )
    parser.add_argument(
        'command',
        nargs='?',
        help='Command or subcommand to execute (update, uninstall, config, history, info, or natural language query)'
    )
    parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments for subcommand or rest of the query'
    )
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Kai Terminal Assistant v1.0.0'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Enable dry-run mode (preview commands without executing)'
    )
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip the welcome banner'
    )
    
    args = parser.parse_args()
    
    # Check if it's a subcommand or a one-shot query
    if args.command:
        # List of known subcommands
        subcommands = ['update', 'uninstall', 'config', 'history', 'info']
        
        if args.command in subcommands:
            # It's a subcommand
            handle_subcommand(args.command, args.args)
            sys.exit(0)
        else:
            # It's a one-shot query - execute and exit
            query = args.command
            if args.args:
                query += ' ' + ' '.join(args.args)
            
            # Execute one-shot command
            execute_one_shot(query)
            sys.exit(0)
    
    # Set dry-run mode if specified
    if args.dry_run:
        config = get_config()
        config.set('dry_run', True)
        config.save()
    
    try:
        # Skip banner if requested
        if args.no_banner:
            # Temporarily disable banner
            import utils.ui
            original_banner = utils.ui.print_banner
            original_welcome = utils.ui.print_first_time_welcome
            utils.ui.print_banner = lambda: None
            utils.ui.print_first_time_welcome = lambda: None
            main()
            utils.ui.print_banner = original_banner
            utils.ui.print_first_time_welcome = original_welcome
        else:
            main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
