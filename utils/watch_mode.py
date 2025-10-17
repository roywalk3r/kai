#!/usr/bin/env python3
"""
Watch mode - continuously monitor command output.
"""

import time
import subprocess
import os
from typing import Optional, Callable
from datetime import datetime


class WatchMode:
    """Watch and continuously re-run commands."""
    
    def __init__(self, command: str, interval: int = 2):
        """
        Initialize watch mode.
        
        Args:
            command: Command to watch
            interval: Refresh interval in seconds
        """
        self.command = command
        self.interval = interval
        self.running = False
        self.last_output = None
        self.change_count = 0
    
    def watch(
        self,
        until_change: bool = False,
        max_runs: Optional[int] = None,
        executor_func: Optional[Callable] = None
    ):
        """
        Watch command output.
        
        Args:
            until_change: Stop when output changes
            max_runs: Maximum number of runs
            executor_func: Optional custom executor function
        """
        from rich.console import Console
        from rich.live import Live
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        self.running = True
        run_count = 0
        
        try:
            with Live(console=console, refresh_per_second=1) as live:
                while self.running:
                    run_count += 1
                    
                    # Execute command
                    if executor_func:
                        success, output = executor_func(self.command)
                    else:
                        success, output = self._execute(self.command)
                    
                    # Check for changes
                    if until_change and self.last_output is not None:
                        if output != self.last_output:
                            self.change_count += 1
                            console.print("\n[bold green]✓ Output changed![/bold green]")
                            break
                    
                    self.last_output = output
                    
                    # Create display
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    header = Text()
                    header.append(f"🔄 Watching: ", style="bold cyan")
                    header.append(self.command, style="bright_white")
                    header.append(f" (every {self.interval}s)", style="dim")
                    header.append(f"\n⏱️  {timestamp} ", style="dim")
                    header.append(f"| Run #{run_count}", style="dim")
                    if until_change:
                        header.append(f" | Changes: {self.change_count}", style="yellow")
                    header.append("\n[dim]Press Ctrl+C to stop[/dim]")
                    
                    # Display output
                    content = Text()
                    content.append(output[:2000])  # Limit display size
                    if len(output) > 2000:
                        content.append("\n... (output truncated)", style="dim")
                    
                    panel = Panel(
                        Text.assemble(header, "\n\n", content),
                        border_style="cyan",
                        title="[bold]Watch Mode[/bold]"
                    )
                    
                    live.update(panel)
                    
                    # Check max runs
                    if max_runs and run_count >= max_runs:
                        console.print(f"\n[yellow]Reached maximum {max_runs} runs[/yellow]")
                        break
                    
                    # Sleep
                    time.sleep(self.interval)
                    
        except KeyboardInterrupt:
            console.print("\n[yellow]Watch mode stopped[/yellow]")
    
    def _execute(self, command: str) -> tuple:
        """Execute command and return output."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def stop(self):
        """Stop watching."""
        self.running = False


def watch_command(
    command: str,
    interval: int = 2,
    until_change: bool = False,
    max_runs: Optional[int] = None,
    executor_func: Optional[Callable] = None
):
    """
    Watch a command's output.
    
    Args:
        command: Command to watch
        interval: Refresh interval in seconds
        until_change: Stop when output changes
        max_runs: Maximum number of runs
        executor_func: Optional custom executor
    """
    watcher = WatchMode(command, interval)
    watcher.watch(until_change, max_runs, executor_func)


class CommandTimer:
    """Time command execution."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.duration = None
    
    def start(self):
        """Start timing."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop timing."""
        self.end_time = time.time()
        if self.start_time:
            self.duration = self.end_time - self.start_time
        return self.duration
    
    def format_duration(self) -> str:
        """Format duration in human-readable form."""
        if not self.duration:
            return "N/A"
        
        if self.duration < 1:
            return f"{self.duration*1000:.0f}ms"
        elif self.duration < 60:
            return f"{self.duration:.2f}s"
        elif self.duration < 3600:
            minutes = int(self.duration // 60)
            seconds = self.duration % 60
            return f"{minutes}m {seconds:.1f}s"
        else:
            hours = int(self.duration // 3600)
            minutes = int((self.duration % 3600) // 60)
            return f"{hours}h {minutes}m"


def benchmark_command(
    command: str,
    runs: int = 5,
    executor_func: Optional[Callable] = None
) -> dict:
    """
    Benchmark a command by running it multiple times.
    
    Args:
        command: Command to benchmark
        runs: Number of runs
        executor_func: Optional custom executor
    
    Returns:
        Dict with benchmark results
    """
    from rich.console import Console
    from rich.progress import Progress
    
    console = Console()
    times = []
    
    console.print(f"[cyan]Benchmarking: {command}[/cyan]")
    console.print(f"[dim]Running {runs} times...[/dim]\n")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Benchmarking...", total=runs)
        
        for i in range(runs):
            timer = CommandTimer()
            timer.start()
            
            if executor_func:
                success, output = executor_func(command)
            else:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                success = result.returncode == 0
            
            duration = timer.stop()
            times.append(duration)
            
            progress.update(task, advance=1)
    
    # Calculate statistics
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    # Median
    sorted_times = sorted(times)
    if len(sorted_times) % 2 == 0:
        median_time = (sorted_times[len(sorted_times)//2 - 1] + sorted_times[len(sorted_times)//2]) / 2
    else:
        median_time = sorted_times[len(sorted_times)//2]
    
    return {
        "command": command,
        "runs": runs,
        "times": times,
        "average": avg_time,
        "min": min_time,
        "max": max_time,
        "median": median_time
    }


def show_benchmark_results(results: dict):
    """Display benchmark results."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    
    # Format times
    timer = CommandTimer()
    timer.duration = results["average"]
    avg_str = timer.format_duration()
    
    timer.duration = results["min"]
    min_str = timer.format_duration()
    
    timer.duration = results["max"]
    max_str = timer.format_duration()
    
    timer.duration = results["median"]
    median_str = timer.format_duration()
    
    # Create table
    table = Table(title="Benchmark Results", border_style="cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bright_white")
    
    table.add_row("Command", results["command"])
    table.add_row("Runs", str(results["runs"]))
    table.add_row("Average", f"[bold]{avg_str}[/bold]")
    table.add_row("Median", median_str)
    table.add_row("Fastest", f"[green]{min_str}[/green]")
    table.add_row("Slowest", f"[yellow]{max_str}[/yellow]")
    
    console.print(table)
    
    # Show individual times
    console.print("\n[bold]Individual Times:[/bold]")
    for i, t in enumerate(results["times"], 1):
        timer.duration = t
        console.print(f"  Run {i}: {timer.format_duration()}")
