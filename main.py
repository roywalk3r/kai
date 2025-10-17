#!/usr/bin/env python3
"""
Prometheus - Intelligent Terminal Assistant
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
from utils.smart_history import SmartHistory, handle_bang_commands
from utils.context_commands import ContextAnalyzer, show_quick_status
from utils.keyboard import create_key_bindings
from core.plugins import get_plugin_manager
from rich.markdown import Markdown

def handle_special_command(query: str) -> bool:
    """
    Handle special built-in commands.
    
    Returns:
        True if command was handled, False otherwise
    """
    config = get_config()
    history = get_history()
    smart_history = SmartHistory()
    plugin_manager = get_plugin_manager()
    
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
    
    # Model switching commands
    elif query in ["use gemini", "use-gemini", "switch gemini", "model gemini"]:
        config.set("use_gemini", True)
        config.save()
        from rich.panel import Panel
        console.print(Panel(
            "[bold green]✓ Switched to Gemini AI[/bold green]\n\n"
            "[bright_white]Using Google's Gemini 2.0 Flash[/bright_white]\n"
            "[dim]Requires: GEMINI_API_KEY environment variable[/dim]",
            border_style="green",
            title="[bold]AI Model[/bold]"
        ))
        return True
    
    elif query in ["use ollama", "use-ollama", "switch ollama", "model ollama"]:
        config.set("use_gemini", False)
        config.save()
        from rich.panel import Panel
        console.print(Panel(
            "[bold green]✓ Switched to Ollama[/bold green]\n\n"
            "[bright_white]Using local Ollama with llama3[/bright_white]\n"
            "[dim]Requires: Ollama running on localhost:11434[/dim]",
            border_style="green",
            title="[bold]AI Model[/bold]"
        ))
        return True
    
    elif query in ["model", "which model", "current model", "ai model"]:
        from rich.panel import Panel
        use_gemini = config.get("use_gemini", True)
        
        # Check if actually available
        from ai.gemini_model import is_gemini_available
        gemini_available = is_gemini_available()
        
        if use_gemini:
            if gemini_available:
                status = "[bold green]Gemini AI (Active)[/bold green]"
                details = "[bright_white]✓ Connected to Google Gemini 2.0 Flash[/bright_white]"
            else:
                status = "[bold yellow]Gemini AI (Configured but not available)[/bold yellow]"
                details = "[yellow]⚠ GEMINI_API_KEY not set - falling back to Ollama[/yellow]"
        else:
            status = "[bold green]Ollama (Active)[/bold green]"
            details = "[bright_white]✓ Using local llama3 model[/bright_white]"
        
        console.print(Panel(
            f"{status}\n\n{details}\n\n"
            "[dim]Switch model:[/dim]\n"
            "[cyan]• use gemini[/cyan] - Google's Gemini AI\n"
            "[cyan]• use ollama[/cyan] - Local Ollama",
            border_style="cyan",
            title="[bold]Current AI Model[/bold]"
        ))
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
    
    # Quick actions
    elif query.startswith("--shorten "):
        from utils.quick_actions import shorten_url
        url = query.split(maxsplit=1)[1]
        shorten_url(url)
        return True
    
    elif query.startswith("--qr "):
        from utils.quick_actions import generate_qr_code
        text = query.split(maxsplit=1)[1]
        generate_qr_code(text)
        return True
    
    elif query.startswith("--hash "):
        from utils.quick_actions import generate_hash
        parts = query.split(maxsplit=2)
        if len(parts) == 3:
            generate_hash(parts[2], parts[1])
        else:
            generate_hash(parts[1])
        return True
    
    elif query.startswith("--encode "):
        from utils.quick_actions import encode_text
        parts = query.split(maxsplit=2)
        if len(parts) == 3:
            encode_text(parts[2], parts[1])
        else:
            encode_text(parts[1])
        return True
    
    elif query.startswith("--decode "):
        from utils.quick_actions import decode_text
        parts = query.split(maxsplit=2)
        if len(parts) == 3:
            decode_text(parts[2], parts[1])
        else:
            decode_text(parts[1])
        return True
    
    elif query.startswith("--time"):
        from utils.quick_actions import world_time, show_multiple_times
        if len(query.split()) > 1:
            location = query.split(maxsplit=1)[1]
            world_time(location)
        else:
            show_multiple_times()
        return True
    
    elif query.startswith("--calc "):
        from utils.quick_actions import calculate
        expression = query.split(maxsplit=1)[1]
        calculate(expression)
        return True
    
    # Search & Navigation
    elif query.startswith("find "):
        from utils.search import fuzzy_find_file
        pattern = query.split(maxsplit=1)[1]
        files = fuzzy_find_file(pattern)
        if files:
            console.print("[bold cyan]Found files:[/bold cyan]")
            for f in files:
                console.print(f"  [bright_white]{f}[/bright_white]")
        else:
            print_warning(f"No files found matching '{pattern}'")
        return True
    
    elif query.startswith("grep "):
        from utils.search import search_in_files
        pattern = query.split(maxsplit=1)[1]
        search_in_files(pattern)
        return True
    
    elif query.startswith("search "):
        from utils.search import find_in_codebase
        pattern = query.split(maxsplit=1)[1]
        find_in_codebase(pattern)
        return True
    
    # Context commands
    elif query == "status":
        show_quick_status()
        return True
    
    elif query == "ref" or query == "reference":
        analyzer = ContextAnalyzer()
        analyzer.show_context_help()
        return True
    
    elif query == "analyze":
        from utils.search import analyze_project
        analyze_project()
        return True
    
    # Watch mode
    elif query.startswith("watch "):
        from utils.watch_mode import watch_command
        parts = query.split(maxsplit=1)
        if len(parts) < 2:
            print_error("Usage: watch <command>")
            return True
        
        # Parse options
        command_part = parts[1]
        interval = 2
        until_change = False
        
        if "--interval" in command_part:
            try:
                parts = command_part.split("--interval")
                interval = int(parts[1].split()[0])
                command_part = parts[0].strip() + " ".join(parts[1].split()[1:])
            except:
                pass
        
        if "--until-change" in command_part:
            until_change = True
            command_part = command_part.replace("--until-change", "").strip()
        
        # Remove quotes if present
        command_part = command_part.strip('"\'')
        
        watch_command(command_part, interval=interval, until_change=until_change)
        return True
    
    # Command timing & benchmarking
    elif query.startswith("time "):
        from utils.watch_mode import CommandTimer
        command = query.split(maxsplit=1)[1]
        
        timer = CommandTimer()
        timer.start()
        
        console.print(f"[cyan]Timing: {command}[/cyan]\n")
        success, output = execute_command(command)
        
        duration = timer.stop()
        console.print(f"\n[bold]⏱️  Execution time: {timer.format_duration()}[/bold]")
        return True
    
    elif query.startswith("benchmark "):
        from utils.watch_mode import benchmark_command, show_benchmark_results
        parts = query.split(maxsplit=2)
        
        if len(parts) < 2:
            print_error("Usage: benchmark <command> [runs]")
            return True
        
        command = parts[1].strip('"\'')
        runs = int(parts[2]) if len(parts) > 2 else 5
        
        results = benchmark_command(command, runs)
        show_benchmark_results(results)
        return True
    
    # Bookmarks
    elif query == "bookmarks" or query == "bookmark":
        from utils.productivity import show_bookmarks
        show_bookmarks()
        return True
    
    elif query.startswith("bookmark add "):
        from utils.productivity import get_bookmark_manager
        parts = query.split(maxsplit=3)
        if len(parts) < 4:
            print_error("Usage: bookmark add <name> <path>")
            return True
        
        name, path = parts[2], parts[3]
        manager = get_bookmark_manager()
        if manager.add(name, path):
            print_success(f"Bookmark '{name}' added")
        return True
    
    elif query.startswith("bookmark remove "):
        from utils.productivity import get_bookmark_manager
        name = query.split(maxsplit=2)[2]
        manager = get_bookmark_manager()
        if manager.remove(name):
            print_success(f"Bookmark '{name}' removed")
        else:
            print_error(f"Bookmark '{name}' not found")
        return True
    
    elif query.startswith("jump "):
        from utils.productivity import get_bookmark_manager
        name = query.split(maxsplit=1)[1]
        manager = get_bookmark_manager()
        path = manager.get(name)
        
        if path:
            import os
            try:
                os.chdir(path)
                print_success(f"Jumped to: {path}")
            except Exception as e:
                print_error(f"Could not change directory: {e}")
        else:
            print_error(f"Bookmark '{name}' not found")
        return True
    
    # Notes
    elif query == "notes":
        from utils.productivity import show_notes
        show_notes()
        return True
    
    elif query.startswith("note "):
        from utils.productivity import get_notes_manager
        note_text = query.split(maxsplit=1)[1].strip('"\'')
        manager = get_notes_manager()
        manager.add(note_text)
        print_success("Note added")
        return True
    
    elif query == "notes clear":
        from utils.productivity import get_notes_manager
        if confirm("Clear all notes for this directory?", default=False):
            manager = get_notes_manager()
            manager.clear()
            print_success("Notes cleared")
        return True
    
    elif query.startswith("notes search "):
        from utils.productivity import get_notes_manager
        from rich.console import Console
        query_text = query.split(maxsplit=2)[2]
        manager = get_notes_manager()
        results = manager.search(query_text)
        
        console = Console()
        if results:
            console.print(f"[cyan]Found {len(results)} note(s):[/cyan]\n")
            for note in results:
                console.print(f"[dim]{note['directory']}[/dim]")
                console.print(f"  {note['text']}\n")
        else:
            console.print("[yellow]No notes found[/yellow]")
        return True
    
    # Favorites
    elif query == "favorites" or query == "fav":
        from utils.productivity import show_favorites
        show_favorites()
        return True
    
    elif query.startswith("favorite add "):
        from utils.productivity import get_favorites_manager
        parts = query.split(maxsplit=3)
        if len(parts) < 4:
            print_error("Usage: favorite add <name> <command>")
            return True
        
        name = parts[2]
        command = parts[3].strip('"\'')
        manager = get_favorites_manager()
        manager.add(name, command)
        print_success(f"Favorite '{name}' added")
        return True
    
    elif query.startswith("favorite remove "):
        from utils.productivity import get_favorites_manager
        name = query.split(maxsplit=2)[2]
        manager = get_favorites_manager()
        if manager.remove(name):
            print_success(f"Favorite '{name}' removed")
        else:
            print_error(f"Favorite '{name}' not found")
        return True
    
    elif query.startswith("fav "):
        from utils.productivity import get_favorites_manager
        name = query.split(maxsplit=1)[1]
        manager = get_favorites_manager()
        command = manager.use(name)
        
        if command:
            console.print(f"[cyan]Running favorite: {command}[/cyan]")
            success, output = execute_command(command)
            return True
        else:
            print_error(f"Favorite '{name}' not found")
            return True
    
    # Smart history
    elif query == "stats":
        smart_history.show_statistics()
        return True
    
    elif query.startswith("!"):
        # Handle bang commands
        cmd = handle_bang_commands(query)
        if cmd:
            # Execute the command
            from ai.model import ask_ai
            response = ask_ai(f"run: {cmd}")
            if response["intent"] == "run":
                success, output = execute_command(response["command"])
                if not config.get("dry_run", False):
                    history.add(query, response["command"], success, output)
        return True
    
    # Plugin commands
    elif query == "plugin" or query.startswith("plugin "):
        parts = query.split()
        if len(parts) < 2:
            print_error("Usage: plugin [list|install|uninstall|create] [name]")
            return True
        
        subcommand = parts[1]
        
        if subcommand == "list":
            plugin_manager.list_plugins()
        elif subcommand == "install" and len(parts) >= 3:
            plugin_name = parts[2]
            source = parts[3] if len(parts) > 3 else ""
            plugin_manager.install_plugin(plugin_name, source)
        elif subcommand == "uninstall" and len(parts) >= 3:
            plugin_manager.uninstall_plugin(parts[2])
        elif subcommand == "create" and len(parts) >= 3:
            from core.plugins import create_plugin_template
            create_plugin_template(parts[2])
        else:
            print_error("Usage: plugin [list|install|uninstall|create] [name]")
        return True
    
    # Alias commands
    elif query == "alias" or query.startswith("alias "):
        from utils.aliases import show_aliases_table, add_alias, remove_alias, list_aliases, get_alias_manager
        parts = query.split(maxsplit=2)
        
        if len(parts) < 2:
            show_aliases_table()
            return True
        
        subcommand = parts[1]
        
        if subcommand == "list":
            show_aliases_table()
        elif subcommand == "add" and len(parts) == 3:
            # Parse: alias add name command
            alias_parts = parts[2].split(maxsplit=1)
            if len(alias_parts) == 2:
                if add_alias(alias_parts[0], alias_parts[1]):
                    print_success(f"Alias '{alias_parts[0]}' added")
                else:
                    print_error("Failed to add alias")
            else:
                print_error("Usage: alias add <name> <command>")
        elif subcommand == "remove" and len(parts) == 3:
            if remove_alias(parts[2]):
                print_success(f"Alias '{parts[2]}' removed")
            else:
                print_error(f"Alias '{parts[2]}' not found")
        elif subcommand == "import":
            manager = get_alias_manager()
            count = manager.import_from_shell("bash")
            print_success(f"Imported {count} aliases from shell")
        else:
            print_error("Usage: alias [list|add|remove|import]")
        return True
    
    # Cache commands
    elif query == "cache" or query.startswith("cache "):
        from utils.cache import show_cache_stats, get_response_cache
        parts = query.split()
        
        if len(parts) < 2:
            show_cache_stats()
            return True
        
        subcommand = parts[1]
        
        if subcommand == "stats":
            show_cache_stats()
        elif subcommand == "clear":
            cache = get_response_cache()
            cache.invalidate()
            print_success("Cache cleared")
        elif subcommand == "clean":
            cache = get_response_cache()
            removed = cache.clean_expired()
            print_success(f"Removed {removed} expired entries")
        else:
            print_error("Usage: cache [stats|clear|clean]")
        return True
    
    # Health check
    elif query == "doctor":
        from utils.health_check import run_health_check
        run_health_check()
        return True
    
    # Template commands
    elif query == "template" or query.startswith("template "):
        from utils.templates import show_templates, show_template_details, use_template, create_template, get_template_manager
        parts = query.split(maxsplit=2)
        
        if len(parts) < 2:
            show_templates()
            return True
        
        subcommand = parts[1]
        
        if subcommand == "list":
            show_templates()
        elif subcommand == "show" and len(parts) >= 3:
            show_template_details(parts[2])
        elif subcommand == "use" and len(parts) >= 3:
            # Parse parameters: template use backup source_dir=/path backup_name=mybackup
            template_and_params = parts[2].split()
            template_name = template_and_params[0]
            params = {}
            for param in template_and_params[1:]:
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
            
            commands = use_template(template_name, params)
            if commands:
                console.print(f"[cyan]Executing template '{template_name}'...[/cyan]")
                for cmd in commands:
                    console.print(f"  [dim]$ {cmd}[/dim]")
                    success, output = execute_command(cmd)
                    if not success:
                        print_error(f"Template execution failed at: {cmd}")
                        break
            else:
                print_error(f"Template '{template_name}' not found")
        else:
            print_error("Usage: template [list|show|use] [name] [params...]")
        return True
    
    # Workflow commands
    elif query == "workflow" or query.startswith("workflow "):
        from utils.workflows import show_workflows, show_workflow_details, get_workflow_manager, WorkflowExecutor
        parts = query.split(maxsplit=2)
        
        if len(parts) < 2:
            show_workflows()
            return True
        
        subcommand = parts[1]
        
        if subcommand == "list":
            show_workflows()
        elif subcommand == "show" and len(parts) >= 3:
            show_workflow_details(parts[2])
        elif subcommand == "run" and len(parts) >= 3:
            manager = get_workflow_manager()
            workflow = manager.get_workflow(parts[2])
            if workflow:
                console.print(f"[cyan]Running workflow '{workflow.name}'...[/cyan]")
                executor = WorkflowExecutor(lambda cmd, **kwargs: execute_command(cmd))
                results = executor.execute_workflow(workflow)
                
                # Display results
                for step_result in results["steps"]:
                    if step_result.get("skipped"):
                        console.print(f"[dim]⊘ {step_result['name']} (skipped)[/dim]")
                    elif step_result.get("success"):
                        console.print(f"[green]✓ {step_result['name']}[/green]")
                    else:
                        console.print(f"[red]✗ {step_result['name']}[/red]")
                
                if results["success"]:
                    print_success("Workflow completed successfully")
                else:
                    print_error("Workflow failed")
            else:
                print_error(f"Workflow '{parts[2]}' not found")
        else:
            print_error("Usage: workflow [list|show|run] [name]")
        return True
    
    # Remote execution commands
    elif query == "remote" or query.startswith("remote "):
        from utils.remote_exec import show_remote_hosts, execute_remote_command, get_remote_executor
        parts = query.split(maxsplit=3)
        
        if len(parts) < 2:
            show_remote_hosts()
            return True
        
        subcommand = parts[1]
        
        if subcommand == "list":
            show_remote_hosts()
        elif subcommand == "add" and len(parts) >= 3:
            # Parse: remote add name user@hostname
            executor = get_remote_executor()
            if '@' in parts[2]:
                user, hostname = parts[2].split('@')
                name = parts[3] if len(parts) > 3 else hostname
                if executor.add_host(name, hostname, user):
                    print_success(f"Host '{name}' added")
                else:
                    print_error("Failed to add host")
            else:
                print_error("Usage: remote add <name> <user@hostname>")
        elif subcommand == "remove" and len(parts) >= 3:
            executor = get_remote_executor()
            if executor.remove_host(parts[2]):
                print_success(f"Host '{parts[2]}' removed")
            else:
                print_error(f"Host '{parts[2]}' not found")
        elif subcommand == "exec" and len(parts) >= 4:
            host_name = parts[2]
            command = parts[3]
            execute_remote_command(host_name, command)
        elif subcommand == "test" and len(parts) >= 3:
            executor = get_remote_executor()
            success, output = executor.test_connection(parts[2])
            if success:
                print_success(f"Connection to '{parts[2]}' OK")
            else:
                print_error(f"Connection failed: {output}")
        else:
            print_error("Usage: remote [list|add|remove|exec|test]")
        return True
    
    # Session commands
    elif query == "session" or query.startswith("session "):
        from core.session import show_session_info, get_session_context
        parts = query.split()
        
        if len(parts) < 2 or parts[1] == "info":
            show_session_info()
        elif parts[1] == "clear":
            session = get_session_context()
            session.clear_context()
            print_success("Session context cleared")
        else:
            print_error("Usage: session [info|clear]")
        return True
    
    # Enhanced history commands
    elif query.startswith("history "):
        from utils.interactive_history import show_history_ui, show_history_table, show_failed_commands, show_history_analysis
        parts = query.split()
        
        if len(parts) < 2:
            show_history_table(history.get_all())
            return True
        
        subcommand = parts[1]
        
        if subcommand == "ui":
            result = show_history_ui(history.get_all())
            if result:
                action = result.get("action")
                item = result.get("item")
                if action == "run":
                    # Re-execute the command
                    console.print(f"[cyan]Running: {item['command']}[/cyan]")
                    execute_command(item["command"])
                elif action == "fix":
                    print_info("Fix functionality integrated with --fix flag")
                elif action == "explain":
                    print_info(f"Command: {item['command']}")
        elif subcommand == "failed":
            show_failed_commands(history.get_all())
        elif subcommand == "analysis" or subcommand == "analyze":
            show_history_analysis(history.get_all())
        else:
            show_history_table(history.get_all())
        return True
    
    # Try plugin handlers
    if plugin_manager.handle_command(query.split()[0] if query else "", query.split()[1:] if len(query.split()) > 1 else []):
        return True
    
    return False

def main():
    """Main application loop."""
    # Initialize
    config = get_config()
    history = get_history()
    conv_context = get_conversation_context()
    
    # Setup prompt with history
    prometheus_dir = Path.home() / ".prometheus"
    prometheus_dir.mkdir(exist_ok=True)
    
    # Create custom prompt with style
    from prompt_toolkit.formatted_text import HTML
    
    def get_prompt():
        return HTML('<ansibrightred><b>🔥 prometheus</b></ansibrightred> <ansiyellow>❯</ansiyellow> ')
    
    # Create key bindings
    session_state = {}
    key_bindings = create_key_bindings(session_state)
    
    session = PromptSession(
        message=get_prompt,
        history=FileHistory(str(prometheus_dir / "prompt_history")),
        auto_suggest=AutoSuggestFromHistory(),
        key_bindings=key_bindings,
        enable_history_search=True,
    )
    
    # Load plugins
    plugin_manager = get_plugin_manager()
    plugin_manager.load_all_plugins()
    
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
            
            # Expand aliases
            from utils.aliases import expand_alias
            original_query = query
            query = expand_alias(query)
            if query != original_query:
                console.print(f"[dim]→ {query}[/dim]")
            
            # Handle special commands
            if handle_special_command(query):
                continue
            
            # Check cache first
            from utils.cache import get_response_cache
            cache = get_response_cache()
            cached_response = cache.get(query, str(Path.cwd()))
            
            if cached_response:
                console.print("[dim]⚡ (cached response)[/dim]")
                response = cached_response
            else:
                # Ask AI to interpret the query
                response = ask_ai(query)
                
                # Cache the response if appropriate
                if cache.should_cache(query):
                    cache.set(query, response, str(Path.cwd()))
            
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
                    
                    # Analyze errors and provide suggestions
                    if not success:
                        from utils.error_recovery import analyze_and_suggest_fix
                        error_analysis = analyze_and_suggest_fix(command, 1, output)
                        
                        if error_analysis.get("suggestions"):
                            console.print("\n[bold yellow]💡 Suggestions:[/bold yellow]")
                            for i, suggestion in enumerate(error_analysis["suggestions"][:3], 1):
                                console.print(f"  {i}. {suggestion}")
                            console.print("\n[dim]Run 'prom --fix' for AI-powered fix[/dim]")
            
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
            "[bold bright_cyan]Updating Prometheus...[/bold bright_cyan]",
            border_style="bright_cyan"
        ))
        
        # Determine installation directory
        script_dir = Path(__file__).parent.absolute()
        
        # Check if we're in a system installation (requires sudo)
        is_system_install = str(script_dir).startswith('/opt/') or str(script_dir).startswith('/usr/')
        
        try:
            # Check if directory is writable
            if not os.access(script_dir, os.W_OK):
                if is_system_install:
                    console.print("[yellow]⚠️  System installation detected. Requires sudo privileges.[/yellow]")
                    console.print("\n[bright_white]Run with sudo:[/bright_white]")
                    console.print(f"  [cyan]sudo {script_dir}/main.py update[/cyan]")
                    console.print("\n[dim]Or reinstall to user directory for automatic updates.[/dim]")
                    return
                else:
                    console.print("[red]❌ No write permission to installation directory[/red]")
                    return
            
            # Fix git ownership issue if present
            git_config_result = subprocess.run(
                ["git", "config", "--global", "--get", "safe.directory"],
                cwd=script_dir,
                capture_output=True,
                text=True
            )
            
            if str(script_dir) not in git_config_result.stdout:
                console.print("[dim]Configuring git safe directory...[/dim]")
                subprocess.run(
                    ["git", "config", "--global", "--add", "safe.directory", str(script_dir)],
                    capture_output=True
                )
            
            # Git pull
            result = subprocess.run(
                ["git", "pull"],
                cwd=script_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                console.print("[green]✓ Updated from git[/green]")
                if result.stdout.strip() and "Already up to date" not in result.stdout:
                    console.print(result.stdout)
                elif "Already up to date" in result.stdout:
                    console.print("[dim]Already up to date[/dim]")
                
                # Update dependencies
                console.print("\n[cyan]Updating dependencies...[/cyan]")
                venv_pip = script_dir / ".venv" / "bin" / "pip"
                if venv_pip.exists():
                    pip_result = subprocess.run(
                        [str(venv_pip), "install", "-r", "requirements.txt", "--upgrade", "-q"],
                        cwd=script_dir,
                        capture_output=True,
                        text=True
                    )
                    if pip_result.returncode == 0:
                        console.print("[green]✓ Dependencies updated[/green]")
                    else:
                        console.print(f"[yellow]⚠️  Dependency update had issues: {pip_result.stderr}[/yellow]")
                else:
                    console.print("[yellow]⚠️  Virtual environment not found, skipping dependency update[/yellow]")
                
                console.print("\n[bold green]✅ Prometheus updated successfully![/bold green]")
            else:
                console.print(f"[red]❌ Update failed: {result.stderr}[/red]")
                if "dubious ownership" in result.stderr:
                    console.print("\n[yellow]Try running with sudo:[/yellow]")
                    console.print(f"  [cyan]sudo {script_dir}/main.py update[/cyan]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")
    
    elif subcommand == "uninstall":
        console.print(Panel(
            "[bold red]⚠️  Uninstalling Prometheus[/bold red]\n\n"
            "[bright_white]This will remove Prometheus from your system.[/bright_white]\n"
            "[dim]Your configuration in ~/.prometheus will be preserved.[/dim]",
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
            config_file = Path.home() / ".prometheus" / "config.json"
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
            table = Table(title="Prometheus Configuration", border_style="cyan")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="bright_white")
            for key, value in config.config.items():
                table.add_row(key, str(value))
            console.print(table)
        else:
            # Show config location
            config_file = Path.home() / ".prometheus" / "config.json"
            console.print(Panel(
                f"[bold bright_white]Configuration File:[/bold bright_white]\n"
                f"[bright_cyan]{config_file}[/bright_cyan]\n\n"
                f"[bold]Commands:[/bold]\n"
                f"[cyan]<alias> config show[/cyan]   - Show current config\n"
                f"[cyan]<alias> config edit[/cyan]   - Edit config file\n"
                f"[cyan]<alias> config reset[/cyan]  - Reset to defaults",
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
            filename = args[1] if len(args) > 1 else "prometheus_history.json"
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
        
        table = Table(title="Prometheus System Information", border_style="bright_cyan")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="bright_white")
        
        script_dir = Path(__file__).parent.absolute()
        table.add_row("Version", "1.0.0")
        table.add_row("Install Location", str(script_dir))
        table.add_row("Config Directory", str(Path.home() / ".prometheus"))
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
        console.print("Run [cyan]<your-alias> --help[/cyan] for available commands")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Prometheus - AI-Powered Terminal Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage Modes:

1. Interactive Mode:
  <your-alias>           Start interactive session (e.g., prom)

2. One-Shot Mode:
  <your-alias> "query"   Execute a single query and exit
  
  Examples:
    prom "list my files"
    prom "update my system"
    prom "show disk usage"
    prom "create a backup of my documents"

3. Subcommands:
  <your-alias> update             Update Prometheus to the latest version
  <your-alias> uninstall          Uninstall Prometheus from the system
  <your-alias> config [show|edit|reset]  Manage configuration
  <your-alias> history [clear|export]    Manage command history
  <your-alias> info               Show system information

More Examples:
  prom --version         Show version information
  prom --dry-run         Enable preview mode
  prom "find python files" --dry-run  Preview without executing

For more information, visit: https://github.com/roywalk3r/prometheus
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
        version='Prometheus Terminal Assistant v1.0.0'
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
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Fix errors from last command'
    )
    parser.add_argument(
        '--explain',
        action='store_true',
        help='Explain last command'
    )
    parser.add_argument(
        '--shorten',
        type=str,
        metavar='URL',
        help='Shorten a URL'
    )
    parser.add_argument(
        '--qr',
        type=str,
        metavar='TEXT',
        help='Generate QR code'
    )
    parser.add_argument(
        '--hash',
        type=str,
        metavar='TEXT',
        help='Generate hash of text'
    )
    parser.add_argument(
        '--encode',
        nargs=2,
        metavar=('TYPE', 'TEXT'),
        help='Encode text (base64, hex, etc.)'
    )
    parser.add_argument(
        '--time',
        type=str,
        nargs='?',
        const='all',
        metavar='LOCATION',
        help='Show world time'
    )
    
    args = parser.parse_args()
    
    # Handle quick action flags
    if args.shorten:
        from utils.quick_actions import shorten_url
        shorten_url(args.shorten)
        sys.exit(0)
    
    if args.qr:
        from utils.quick_actions import generate_qr_code
        generate_qr_code(args.qr)
        sys.exit(0)
    
    if args.hash:
        from utils.quick_actions import generate_hash
        generate_hash(args.hash)
        sys.exit(0)
    
    if args.encode:
        from utils.quick_actions import encode_text
        encode_text(args.encode[1], args.encode[0])
        sys.exit(0)
    
    if args.time:
        from utils.quick_actions import world_time, show_multiple_times
        if args.time == 'all':
            show_multiple_times()
        else:
            world_time(args.time)
        sys.exit(0)
    
    if args.fix:
        from utils.smart_history import SmartHistory
        smart_history = SmartHistory()
        last_failed = smart_history.get_last_failed_command()
        if last_failed:
            console.print(f"[yellow]Last failed command:[/yellow] {last_failed}")
            console.print("[dim]Analyzing error...[/dim]")
            # Let AI suggest fix
            execute_one_shot(f"fix this command: {last_failed}")
        else:
            console.print("[yellow]No failed commands in history[/yellow]")
        sys.exit(0)
    
    if args.explain:
        from utils.smart_history import SmartHistory
        smart_history = SmartHistory()
        last_cmd = smart_history.get_last_command()
        if last_cmd:
            console.print(f"[cyan]Last command:[/cyan] {last_cmd}")
            execute_one_shot(f"explain this command: {last_cmd}")
        else:
            console.print("[yellow]No commands in history[/yellow]")
        sys.exit(0)
    
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
