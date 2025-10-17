#!/usr/bin/env python3
"""
Advanced tools: Environment manager, Export/Import, Multi-line builder, Output formatting.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil


# ==================== ENVIRONMENT MANAGER ====================

class EnvironmentManager:
    """Manage environment variables and .env files."""
    
    def __init__(self):
        self.env_dir = Path.home() / ".prometheus" / "environments"
        self.env_dir.mkdir(parents=True, exist_ok=True)
        self.current_env = {}
    
    def set(self, key: str, value: str, persist: bool = True):
        """Set environment variable."""
        os.environ[key] = value
        self.current_env[key] = value
        
        if persist:
            env_file = self.env_dir / "default.env"
            self._update_env_file(env_file, key, value)
    
    def get(self, key: str) -> Optional[str]:
        """Get environment variable."""
        return os.environ.get(key)
    
    def unset(self, key: str):
        """Unset environment variable."""
        if key in os.environ:
            del os.environ[key]
        if key in self.current_env:
            del self.current_env[key]
    
    def list_all(self) -> Dict[str, str]:
        """List all environment variables."""
        return dict(os.environ)
    
    def load_from_file(self, env_name: str = "default"):
        """Load environment from file."""
        env_file = self.env_dir / f"{env_name}.env"
        if not env_file.exists():
            return False
        
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ[key] = value
                    self.current_env[key] = value
        return True
    
    def save_to_file(self, env_name: str = "default", keys: Optional[List[str]] = None):
        """Save environment to file."""
        env_file = self.env_dir / f"{env_name}.env"
        
        vars_to_save = {}
        if keys:
            for key in keys:
                if key in os.environ:
                    vars_to_save[key] = os.environ[key]
        else:
            vars_to_save = self.current_env
        
        with open(env_file, 'w') as f:
            f.write("# Prometheus Environment Variables\n")
            f.write(f"# Saved: {Path.cwd()}\n\n")
            for key, value in sorted(vars_to_save.items()):
                f.write(f'{key}="{value}"\n')
        
        return True
    
    def _update_env_file(self, env_file: Path, key: str, value: str):
        """Update single variable in env file."""
        lines = []
        updated = False
        
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.strip().startswith(f"{key}="):
                        lines.append(f'{key}="{value}"\n')
                        updated = True
                    else:
                        lines.append(line)
        
        if not updated:
            lines.append(f'{key}="{value}"\n')
        
        with open(env_file, 'w') as f:
            f.writelines(lines)
    
    def list_env_files(self) -> List[str]:
        """List available environment files."""
        return [f.stem for f in self.env_dir.glob("*.env")]


def show_environment(filter_prometheus: bool = False):
    """Display environment variables."""
    from rich.table import Table
    from rich.console import Console
    
    env_vars = dict(os.environ)
    
    if filter_prometheus:
        # Show only Prometheus-related vars
        env_vars = {k: v for k, v in env_vars.items() 
                   if 'PROM' in k.upper() or k in ['PATH', 'HOME', 'USER', 'SHELL']}
    
    table = Table(title="Environment Variables", border_style="cyan")
    table.add_column("Variable", style="cyan", no_wrap=True)
    table.add_column("Value", style="bright_white")
    
    for key, value in sorted(env_vars.items()):
        # Truncate long values
        display_value = value if len(value) < 60 else value[:57] + "..."
        table.add_row(key, display_value)
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Total: {len(env_vars)} variables[/dim]")


# ==================== EXPORT/IMPORT SYSTEM ====================

class ConfigExporter:
    """Export and import Prometheus configurations."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".prometheus"
    
    def export_all(self, output_file: Path) -> bool:
        """Export all configurations."""
        data = {
            "version": "1.0",
            "exported_at": __import__('datetime').datetime.now().isoformat(),
            "config": self._load_json("config.json"),
            "aliases": self._load_json("aliases.json"),
            "templates": self._load_json("templates.json"),
            "workflows": self._load_json("workflows/workflows.json"),
            "bookmarks": self._load_json("bookmarks.json"),
            "favorites": self._load_json("favorites.json"),
            "remote_hosts": self._load_json("remote_hosts.json"),
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return True
    
    def import_all(self, input_file: Path, selective: Optional[List[str]] = None) -> Dict[str, bool]:
        """Import configurations."""
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        results = {}
        
        mappings = {
            "config": "config.json",
            "aliases": "aliases.json",
            "templates": "templates.json",
            "workflows": "workflows/workflows.json",
            "bookmarks": "bookmarks.json",
            "favorites": "favorites.json",
            "remote_hosts": "remote_hosts.json",
        }
        
        for key, filename in mappings.items():
            if selective and key not in selective:
                continue
            
            if key in data and data[key]:
                try:
                    self._save_json(filename, data[key])
                    results[key] = True
                except Exception as e:
                    results[key] = False
            else:
                results[key] = False
        
        return results
    
    def _load_json(self, filename: str) -> Dict:
        """Load JSON file."""
        file_path = self.config_dir / filename
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_json(self, filename: str, data: Dict):
        """Save JSON file."""
        file_path = self.config_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)


# ==================== MULTI-LINE COMMAND BUILDER ====================

def multiline_builder() -> Optional[str]:
    """Interactive multi-line command builder."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    
    console = Console()
    
    console.print(Panel(
        "[bold cyan]Multi-line Command Builder[/bold cyan]\n\n"
        "[bright_white]Enter commands line by line[/bright_white]\n"
        "[dim]• Empty line to finish\n"
        "• Type 'cancel' to abort[/dim]",
        border_style="cyan"
    ))
    
    lines = []
    line_num = 1
    
    while True:
        try:
            from prompt_toolkit import prompt
            line = prompt(f"[{line_num}] ").strip()
            
            if not line:
                break
            
            if line.lower() == 'cancel':
                console.print("[yellow]Cancelled[/yellow]")
                return None
            
            lines.append(line)
            line_num += 1
            
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Cancelled[/yellow]")
            return None
    
    if not lines:
        return None
    
    # Display preview
    command = " && ".join(lines)
    console.print("\n[bold]Preview:[/bold]")
    syntax = Syntax(command, "bash", theme="monokai", line_numbers=False)
    console.print(syntax)
    
    # Confirm
    from prompt_toolkit import prompt as simple_prompt
    response = simple_prompt("\nExecute? [y/n] (y): ").strip().lower()
    
    if response in ['', 'y', 'yes']:
        return command
    
    return None


# ==================== OUTPUT FORMATTING ====================

class OutputFormatter:
    """Format command output in various ways."""
    
    @staticmethod
    def format_json(text: str) -> str:
        """Format text as pretty JSON."""
        try:
            data = json.loads(text)
            return json.dumps(data, indent=2, sort_keys=True)
        except:
            return text
    
    @staticmethod
    def format_table(text: str, delimiter: str = None) -> str:
        """Format text as table."""
        from rich.table import Table
        from rich.console import Console
        from io import StringIO
        
        lines = text.strip().split('\n')
        if not lines:
            return text
        
        # Auto-detect delimiter
        if delimiter is None:
            if '\t' in lines[0]:
                delimiter = '\t'
            elif '  ' in lines[0]:
                delimiter = '  '
            else:
                delimiter = ' '
        
        # Parse lines
        rows = []
        for line in lines:
            if delimiter == '  ':
                # Multiple spaces as delimiter
                cols = [c.strip() for c in line.split('  ') if c.strip()]
            else:
                cols = [c.strip() for c in line.split(delimiter)]
            if cols:
                rows.append(cols)
        
        if not rows:
            return text
        
        # Create table
        table = Table(border_style="cyan")
        
        # Add columns (use first row as header if looks like header)
        headers = rows[0]
        data_rows = rows[1:] if len(rows) > 1 else []
        
        for header in headers:
            table.add_column(header, style="cyan")
        
        # Add data
        for row in data_rows:
            # Pad row to match column count
            while len(row) < len(headers):
                row.append("")
            table.add_row(*row[:len(headers)])
        
        # Render to string
        console = Console(file=StringIO(), width=120)
        console.print(table)
        return console.file.getvalue()
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """Copy text to clipboard."""
        try:
            # Try xclip (Linux)
            subprocess.run(
                ['xclip', '-selection', 'clipboard'],
                input=text.encode(),
                check=True
            )
            return True
        except:
            try:
                # Try pbcopy (macOS)
                subprocess.run(
                    ['pbcopy'],
                    input=text.encode(),
                    check=True
                )
                return True
            except:
                try:
                    # Try wl-copy (Wayland)
                    subprocess.run(
                        ['wl-copy'],
                        input=text.encode(),
                        check=True
                    )
                    return True
                except:
                    return False
    
    @staticmethod
    def highlight_syntax(text: str, language: str = "bash") -> str:
        """Apply syntax highlighting."""
        from rich.syntax import Syntax
        from rich.console import Console
        from io import StringIO
        
        syntax = Syntax(text, language, theme="monokai", line_numbers=False)
        console = Console(file=StringIO(), width=120)
        console.print(syntax)
        return console.file.getvalue()


# ==================== GLOBAL INSTANCES ====================

_env_manager = None
_config_exporter = None


def get_env_manager() -> EnvironmentManager:
    """Get global environment manager."""
    global _env_manager
    if _env_manager is None:
        _env_manager = EnvironmentManager()
    return _env_manager


def get_config_exporter() -> ConfigExporter:
    """Get global config exporter."""
    global _config_exporter
    if _config_exporter is None:
        _config_exporter = ConfigExporter()
    return _config_exporter
