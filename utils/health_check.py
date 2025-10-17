#!/usr/bin/env python3
"""
Health check and diagnostics system.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import importlib.util


class HealthCheck:
    """System health check and diagnostics."""
    
    def __init__(self):
        self.checks = []
        self.issues = []
        self.warnings = []
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check Python version."""
        version = sys.version_info
        if version.major == 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor} (requires 3.8+)"
    
    def check_dependencies(self) -> Tuple[bool, List[str]]:
        """Check if required dependencies are installed."""
        required = [
            "rich",
            "prompt_toolkit",
            "pyqrcode",
            "pytz",
        ]
        
        missing = []
        installed = []
        
        for package in required:
            spec = importlib.util.find_spec(package)
            if spec is None:
                missing.append(package)
            else:
                installed.append(package)
        
        if missing:
            return False, missing
        return True, installed
    
    def check_config_file(self) -> Tuple[bool, str]:
        """Check configuration file."""
        config_file = Path.home() / ".prometheus" / "config.json"
        
        if not config_file.exists():
            return False, "Config file not found"
        
        try:
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            return True, f"Config loaded ({len(config)} settings)"
        except Exception as e:
            return False, f"Config invalid: {str(e)}"
    
    def check_history_file(self) -> Tuple[bool, str]:
        """Check history file."""
        history_file = Path.home() / ".prometheus" / "history.txt"
        
        if history_file.exists():
            try:
                lines = len(history_file.read_text().splitlines())
                return True, f"History: {lines} commands"
            except:
                return False, "History file corrupted"
        return True, "History: empty"
    
    def check_api_keys(self) -> Tuple[bool, str]:
        """Check API keys configuration."""
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if gemini_key:
            masked = gemini_key[:8] + "..." if len(gemini_key) > 8 else "***"
            return True, f"Gemini API key set ({masked})"
        
        # Check if Ollama is available
        if shutil.which("ollama"):
            return True, "Ollama available (local mode)"
        
        return False, "No AI backend configured"
    
    def check_ollama(self) -> Tuple[bool, str]:
        """Check Ollama installation and models."""
        if not shutil.which("ollama"):
            return None, "Ollama not installed"
        
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                model_count = len(lines) - 1 if len(lines) > 1 else 0
                return True, f"Ollama: {model_count} models available"
            else:
                return False, "Ollama not responding"
        except:
            return False, "Ollama service error"
    
    def check_git(self) -> Tuple[bool, str]:
        """Check Git installation."""
        if shutil.which("git"):
            try:
                result = subprocess.run(
                    ["git", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                version = result.stdout.strip()
                return True, version
            except:
                return False, "Git installed but not responding"
        return None, "Git not installed (optional)"
    
    def check_disk_space(self) -> Tuple[bool, str]:
        """Check disk space."""
        try:
            stat = shutil.disk_usage(Path.home())
            free_gb = stat.free / (1024**3)
            total_gb = stat.total / (1024**3)
            percent_free = (stat.free / stat.total) * 100
            
            if free_gb < 1:
                return False, f"Low disk space: {free_gb:.1f}GB free"
            elif free_gb < 5:
                return None, f"Disk space: {free_gb:.1f}GB / {total_gb:.1f}GB ({percent_free:.0f}% free)"
            else:
                return True, f"Disk space: {free_gb:.1f}GB free"
        except:
            return None, "Could not check disk space"
    
    def check_memory(self) -> Tuple[bool, str]:
        """Check memory usage."""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
            
            mem_total = mem_free = mem_available = 0
            for line in lines:
                if 'MemTotal' in line:
                    mem_total = int(line.split()[1]) / 1024  # MB
                elif 'MemFree' in line:
                    mem_free = int(line.split()[1]) / 1024
                elif 'MemAvailable' in line:
                    mem_available = int(line.split()[1]) / 1024
            
            if mem_available < 500:
                return False, f"Low memory: {mem_available:.0f}MB available"
            elif mem_available < 1000:
                return None, f"Memory: {mem_available:.0f}MB / {mem_total:.0f}MB"
            else:
                return True, f"Memory: {mem_available:.0f}MB available"
        except:
            return None, "Could not check memory"
    
    def check_network(self) -> Tuple[bool, str]:
        """Check network connectivity."""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "2", "8.8.8.8"],
                capture_output=True,
                timeout=3
            )
            if result.returncode == 0:
                return True, "Network: Connected"
            return False, "Network: No connectivity"
        except:
            return None, "Network: Could not test"
    
    def check_shell_integration(self) -> Tuple[bool, str]:
        """Check if shell integration is set up."""
        shell_rc_files = [
            Path.home() / ".bashrc",
            Path.home() / ".zshrc",
        ]
        
        for rc_file in shell_rc_files:
            if rc_file.exists():
                try:
                    content = rc_file.read_text()
                    if "prometheus" in content.lower() or "prom" in content:
                        return True, f"Shell integration: {rc_file.name}"
                except:
                    pass
        
        return None, "No shell integration found (optional)"
    
    def check_terminal_features(self) -> Tuple[bool, str]:
        """Check terminal capabilities."""
        issues = []
        
        # Check terminal size
        try:
            import shutil
            cols, rows = shutil.get_terminal_size()
            if cols < 80:
                issues.append("Terminal width < 80 cols")
        except:
            issues.append("Could not detect terminal size")
        
        # Check color support
        if os.getenv("TERM") in ["xterm-256color", "screen-256color"]:
            color_support = "256 colors"
        elif os.getenv("TERM"):
            color_support = os.getenv("TERM")
        else:
            color_support = "unknown"
            issues.append("Terminal type not detected")
        
        if issues:
            return None, f"Terminal: {color_support}, {', '.join(issues)}"
        return True, f"Terminal: {color_support}"
    
    def check_plugins(self) -> Tuple[bool, str]:
        """Check plugins directory."""
        plugins_dir = Path.home() / ".prometheus" / "plugins"
        
        if not plugins_dir.exists():
            return True, "Plugins: 0 installed"
        
        plugin_files = list(plugins_dir.glob("*.py"))
        return True, f"Plugins: {len(plugin_files)} installed"
    
    def run_all_checks(self) -> Dict:
        """Run all health checks."""
        results = {}
        
        checks = [
            ("Python Version", self.check_python_version),
            ("Dependencies", self.check_dependencies),
            ("Configuration", self.check_config_file),
            ("History", self.check_history_file),
            ("AI Backend", self.check_api_keys),
            ("Ollama", self.check_ollama),
            ("Git", self.check_git),
            ("Disk Space", self.check_disk_space),
            ("Memory", self.check_memory),
            ("Network", self.check_network),
            ("Shell Integration", self.check_shell_integration),
            ("Terminal", self.check_terminal_features),
            ("Plugins", self.check_plugins),
        ]
        
        for name, check_func in checks:
            try:
                status, message = check_func()
                results[name] = {
                    "status": status,
                    "message": message
                }
            except Exception as e:
                results[name] = {
                    "status": False,
                    "message": f"Check failed: {str(e)}"
                }
        
        return results
    
    def get_recommendations(self, results: Dict) -> List[str]:
        """Get recommendations based on check results."""
        recommendations = []
        
        for name, result in results.items():
            status = result["status"]
            message = result["message"]
            
            if status is False:
                if name == "Dependencies":
                    missing = message  # List of missing packages
                    recommendations.append(f"Install missing dependencies: pip install {' '.join(missing)}")
                elif name == "AI Backend":
                    recommendations.append("Set up AI backend: export GEMINI_API_KEY=your_key or install Ollama")
                elif name == "Disk Space":
                    recommendations.append("Free up disk space: sudo apt clean or remove unused files")
                elif name == "Memory":
                    recommendations.append("Close unused applications to free memory")
                elif name == "Network":
                    recommendations.append("Check network connection")
                elif name == "Configuration":
                    recommendations.append("Reset configuration: prom config reset")
            
            elif status is None:
                if name == "Git":
                    recommendations.append("Install Git for enhanced features: sudo apt install git")
                elif name == "Shell Integration":
                    recommendations.append("Add to .bashrc: alias prom='python3 /path/to/prometheus/main.py'")
        
        return recommendations


def run_health_check():
    """Run health check and display results."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    console = Console()
    
    console.print(Panel(
        "[bold bright_cyan]🏥 Prometheus Health Check[/bold bright_cyan]",
        border_style="bright_cyan"
    ))
    
    checker = HealthCheck()
    
    with console.status("[cyan]Running diagnostics...[/cyan]"):
        results = checker.run_all_checks()
    
    # Create results table
    table = Table(border_style="cyan")
    table.add_column("Check", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="bright_white")
    
    passed = failed = warnings = 0
    
    for name, result in results.items():
        status = result["status"]
        message = result["message"]
        
        if status is True:
            status_icon = "[green]✓[/green]"
            passed += 1
        elif status is False:
            status_icon = "[red]✗[/red]"
            failed += 1
        else:  # None = warning
            status_icon = "[yellow]⚠[/yellow]"
            warnings += 1
        
        table.add_row(name, status_icon, message)
    
    console.print(table)
    
    # Summary
    console.print()
    if failed == 0:
        console.print("[bold green]✅ All critical checks passed![/bold green]")
    else:
        console.print(f"[bold red]❌ {failed} check(s) failed[/bold red]")
    
    if warnings > 0:
        console.print(f"[yellow]⚠️  {warnings} warning(s)[/yellow]")
    
    console.print(f"[dim]Passed: {passed} | Failed: {failed} | Warnings: {warnings}[/dim]")
    
    # Recommendations
    recommendations = checker.get_recommendations(results)
    if recommendations:
        console.print("\n[bold yellow]📋 Recommendations:[/bold yellow]")
        for i, rec in enumerate(recommendations, 1):
            console.print(f"  {i}. {rec}")
    
    return failed == 0
