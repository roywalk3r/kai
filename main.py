#!/usr/bin/env python3
"""
Kai - Intelligent Terminal Assistant
Main entry point for the application.
"""

import sys
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
    print_info, print_success, confirm, console, print_first_time_welcome
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
    
    session = PromptSession(
        history=FileHistory(str(kai_dir / "prompt_history")),
        auto_suggest=AutoSuggestFromHistory(),
    )
    
    # Print banner
    print_banner()
    
    # Show enhanced welcome screen every time
    print_first_time_welcome()
    
    # Check if dry-run mode is enabled
    if config.get("dry_run", False):
        print_warning("Dry-run mode is enabled")
    
    # Main loop
    while True:
        try:
            # Get user input
            query = session.prompt("> ").strip()
            
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
                console.print(response["message"])
                continue
            
            elif response["intent"] == "run":
                command = response["command"]
                warning = response.get("warning")
                safety_level = response.get("safety_level", SafetyLevel.SAFE)
                
                # Show warning if present
                if warning:
                    print_warning(warning)
                    
                    # For dangerous commands, require explicit confirmation
                    if safety_level == SafetyLevel.DANGEROUS:
                        if not confirm("Are you SURE you want to run this?", default=False):
                            print_info("Command cancelled")
                            continue
                    else:
                        if not confirm("Proceed?", default=True):
                            print_info("Command cancelled")
                            continue
                
                # Execute command
                dry_run = config.get("dry_run", False)
                success, output = execute_command(command, dry_run=dry_run)
                
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

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
