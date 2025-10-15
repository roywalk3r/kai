import subprocess
import threading
import signal
import time
import sys
from typing import Optional, Tuple
from rich.console import Console
from .config import get_config
from ai.error_fixer import detect_and_fix_error, analyze_error

console = Console()
current_process = None
process_timer = None

def kill_process():
    """Kill the current process due to timeout."""
    global current_process
    if current_process and current_process.poll() is None:
        try:
            current_process.terminate()
            time.sleep(0.5)
            if current_process.poll() is None:
                current_process.kill()
        except Exception:
            pass
        config = get_config()
        timeout = config.get("timeout_seconds", 20)
        console.print(f"[red]⏰ Process killed after {timeout}s timeout.[/red]")
        current_process = None

def execute_command(cmd: str, dry_run: bool = False, interactive: bool = False) -> Tuple[bool, Optional[str]]:
    """
    Execute a shell command.
    
    Args:
        cmd: Command to execute
        dry_run: If True, only print the command without executing
        interactive: If True, run command interactively (no output capture)
        
    Returns:
        Tuple of (success, output)
    """
    global current_process, process_timer
    
    # Enhanced command display
    from rich.panel import Panel
    console.print(Panel(
        f"[bold bright_white]{cmd}[/bold bright_white]",
        border_style="bright_green",
        padding=(0, 1),
        title="[bold bright_green]⚡ Executing[/bold bright_green]",
        title_align="left"
    ))
    
    if dry_run:
        console.print("[dim]Dry-run mode: Command not executed[/dim]")
        return True, None
    
    config = get_config()
    timeout_seconds = config.get("timeout_seconds", 20)
    output_lines = []
    stderr_output = ""

    try:
        # For interactive commands, don't capture output
        if interactive:
            result = subprocess.run(
                cmd,
                shell=True,
                text=True
            )
            return result.returncode == 0, None
        
        # For non-interactive commands, capture output
        current_process = subprocess.Popen(
            cmd,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
        )

        # Set up timeout thread
        process_timer = threading.Timer(timeout_seconds, kill_process)
        process_timer.start()

        # Stream stdout live
        if current_process.stdout:
            for line in current_process.stdout:
                line_stripped = line.rstrip()
                console.print(line_stripped)
                output_lines.append(line_stripped)

        # Wait for process to complete
        current_process.wait()
        
        # Check stderr
        if current_process.stderr:
            stderr_output = current_process.stderr.read()
            if stderr_output:
                console.print(f"[red]{stderr_output}[/red]")
                output_lines.append(f"ERROR: {stderr_output}")
        
        # Check return code
        return_code = current_process.returncode
        success = return_code == 0
        
        if not success:
            console.print(f"[yellow]Command exited with code {return_code}[/yellow]")
            
            # Try to detect and fix the error
            fix_result = detect_and_fix_error(cmd, stderr_output, return_code)
            if fix_result:
                fixed_cmd, explanation = fix_result
                from rich.panel import Panel
                fix_panel = Panel(
                    f"[bright_white]{explanation}[/bright_white]\n\n"
                    f"[bold bright_green]Suggested fix:[/bold bright_green]\n"
                    f"[bright_cyan]{fixed_cmd}[/bright_cyan]",
                    border_style="bright_cyan",
                    title="[bold bright_cyan]💡 Smart Fix Detected[/bold bright_cyan]",
                    title_align="left",
                    padding=(1, 2)
                )
                console.print()
                console.print(fix_panel)
                
                # Ask if user wants to run the fix
                from rich.prompt import Confirm
                if Confirm.ask("\n[cyan]Run the fixed command?[/cyan]", default=True):
                    console.print()
                    return execute_command(fixed_cmd, dry_run=False, interactive=interactive)
            else:
                # Provide error analysis
                analysis = analyze_error(cmd, stderr_output, return_code)
                from rich.panel import Panel
                error_panel = Panel(
                    f"[bright_white]{analysis}[/bright_white]",
                    border_style="yellow",
                    title="[bold yellow]📋 Error Analysis[/bold yellow]",
                    title_align="left",
                    padding=(1, 2)
                )
                console.print()
                console.print(error_panel)
        
        return success, "\n".join(output_lines)

    except KeyboardInterrupt:
        console.print("[yellow]⛔ Command interrupted by user.[/yellow]")
        if current_process:
            try:
                current_process.terminate()
            except Exception:
                pass
        return False, None

    except Exception as e:
        console.print(f"[red]Error executing command: {str(e)}[/red]")
        return False, str(e)

    finally:
        # Cleanup
        if current_process and current_process.poll() is None:
            try:
                current_process.terminate()
            except Exception:
                pass
        current_process = None
        if process_timer:
            process_timer.cancel()
            process_timer = None

def terminate_process():
    """Kill the currently running process manually."""
    global current_process
    if current_process and current_process.poll() is None:
        try:
            current_process.terminate()
            time.sleep(0.5)
            if current_process.poll() is None:
                current_process.kill()
            console.print("[red]⛔ Process terminated by user.[/red]")
        except Exception as e:
            console.print(f"[red]Error terminating process: {str(e)}[/red]")
        current_process = None
    else:
        console.print("[dim]No running process to terminate.[/dim]")
