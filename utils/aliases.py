#!/usr/bin/env python3
"""
Command aliases system for custom shortcuts.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class AliasManager:
    """Manage command aliases and shortcuts."""
    
    def __init__(self):
        self.aliases_file = Path.home() / ".prometheus" / "aliases.json"
        self.aliases = self._load_aliases()
    
    def _load_aliases(self) -> Dict[str, str]:
        """Load aliases from file."""
        if self.aliases_file.exists():
            try:
                with open(self.aliases_file, 'r') as f:
                    return json.load(f)
            except:
                return self._get_default_aliases()
        return self._get_default_aliases()
    
    def _get_default_aliases(self) -> Dict[str, str]:
        """Get default aliases."""
        return {
            # Git aliases
            "gs": "git status",
            "ga": "git add .",
            "gc": "git commit -m",
            "gp": "git push",
            "gl": "git pull",
            "gd": "git diff",
            "gco": "git checkout",
            "gb": "git branch",
            "glog": "git log --oneline --graph --decorate",
            
            # Docker aliases
            "dp": "docker ps",
            "dpa": "docker ps -a",
            "di": "docker images",
            "dex": "docker exec -it",
            "dlog": "docker logs",
            "dstop": "docker stop $(docker ps -aq)",
            "drm": "docker rm $(docker ps -aq)",
            
            # System aliases
            "ll": "ls -alh",
            "la": "ls -A",
            "ports": "netstat -tulpn",
            "psg": "ps aux | grep",
            "myip": "curl ifconfig.me",
            "speedtest": "curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -",
            
            # Python aliases
            "py": "python3",
            "pip": "pip3",
            "venv": "python3 -m venv venv && source venv/bin/activate",
            "pyserver": "python3 -m http.server",
            
            # Directory navigation
            "..": "cd ..",
            "...": "cd ../..",
            "home": "cd ~",
            
            # File operations
            "backup": "tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz",
            "extract": "tar -xzf",
            
            # Monitoring
            "cpu": "top -bn1 | grep Cpu",
            "mem": "free -h",
            "disk": "df -h",
            
            # Prometheus specific
            "pstatus": "status",
            "pref": "ref",
            "pstats": "stats",
            "pfind": "find",
        }
    
    def _save_aliases(self):
        """Save aliases to file."""
        self.aliases_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.aliases_file, 'w') as f:
            json.dump(self.aliases, f, indent=2)
    
    def expand_alias(self, query: str) -> str:
        """
        Expand alias if it exists.
        
        Args:
            query: User query
        
        Returns:
            Expanded query or original query
        """
        parts = query.strip().split(None, 1)
        if not parts:
            return query
        
        alias = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        if alias in self.aliases:
            expanded = self.aliases[alias]
            if args:
                # If alias command expects arguments, append them
                return f"{expanded} {args}"
            return expanded
        
        return query
    
    def add_alias(self, alias: str, command: str) -> bool:
        """
        Add or update an alias.
        
        Args:
            alias: Alias name
            command: Command to execute
        
        Returns:
            True if successful
        """
        if not alias or not command:
            return False
        
        # Validate alias name (alphanumeric and underscore/dash only)
        if not all(c.isalnum() or c in '-_.' for c in alias):
            return False
        
        self.aliases[alias] = command
        self._save_aliases()
        return True
    
    def remove_alias(self, alias: str) -> bool:
        """
        Remove an alias.
        
        Args:
            alias: Alias to remove
        
        Returns:
            True if removed
        """
        if alias in self.aliases:
            del self.aliases[alias]
            self._save_aliases()
            return True
        return False
    
    def list_aliases(self, filter_str: Optional[str] = None) -> Dict[str, str]:
        """
        List all aliases or filtered aliases.
        
        Args:
            filter_str: Optional filter string
        
        Returns:
            Dict of aliases
        """
        if filter_str:
            return {
                k: v for k, v in self.aliases.items()
                if filter_str.lower() in k.lower() or filter_str.lower() in v.lower()
            }
        return self.aliases.copy()
    
    def get_alias(self, alias: str) -> Optional[str]:
        """Get command for an alias."""
        return self.aliases.get(alias)
    
    def alias_exists(self, alias: str) -> bool:
        """Check if alias exists."""
        return alias in self.aliases
    
    def import_from_shell(self, shell: str = "bash") -> int:
        """
        Import aliases from shell config.
        
        Args:
            shell: Shell type (bash, zsh)
        
        Returns:
            Number of aliases imported
        """
        import re
        
        shell_files = {
            "bash": [".bashrc", ".bash_aliases"],
            "zsh": [".zshrc", ".zsh_aliases"]
        }
        
        count = 0
        home = Path.home()
        
        for filename in shell_files.get(shell, []):
            filepath = home / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                    
                    # Match alias definitions: alias name='command'
                    pattern = r"alias\s+([a-zA-Z0-9_-]+)=['\"]([^'\"]+)['\"]"
                    matches = re.findall(pattern, content)
                    
                    for alias, command in matches:
                        if not self.alias_exists(alias):
                            self.add_alias(alias, command)
                            count += 1
                except:
                    continue
        
        return count
    
    def export_to_shell(self, output_file: Optional[Path] = None) -> str:
        """
        Export aliases to shell format.
        
        Args:
            output_file: Optional file to write to
        
        Returns:
            Shell-formatted aliases
        """
        lines = ["# Prometheus aliases", ""]
        
        for alias, command in sorted(self.aliases.items()):
            # Escape single quotes in command
            escaped_command = command.replace("'", "'\\''")
            lines.append(f"alias {alias}='{escaped_command}'")
        
        content = "\n".join(lines)
        
        if output_file:
            output_file.write_text(content)
        
        return content


# Global alias manager instance
_alias_manager = None


def get_alias_manager() -> AliasManager:
    """Get global alias manager instance."""
    global _alias_manager
    if _alias_manager is None:
        _alias_manager = AliasManager()
    return _alias_manager


def expand_alias(query: str) -> str:
    """Expand alias in query."""
    return get_alias_manager().expand_alias(query)


def add_alias(alias: str, command: str) -> bool:
    """Add an alias."""
    return get_alias_manager().add_alias(alias, command)


def remove_alias(alias: str) -> bool:
    """Remove an alias."""
    return get_alias_manager().remove_alias(alias)


def list_aliases(filter_str: Optional[str] = None) -> Dict[str, str]:
    """List aliases."""
    return get_alias_manager().list_aliases(filter_str)


def show_aliases_table():
    """Display aliases in a formatted table."""
    from rich.table import Table
    from rich.console import Console
    
    manager = get_alias_manager()
    aliases = manager.list_aliases()
    
    if not aliases:
        console = Console()
        console.print("[yellow]No aliases defined[/yellow]")
        return
    
    table = Table(title="Command Aliases", border_style="cyan")
    table.add_column("Alias", style="cyan", no_wrap=True)
    table.add_column("Command", style="bright_white")
    table.add_column("Category", style="dim")
    
    # Categorize aliases
    categories = {
        "git": ["gs", "ga", "gc", "gp", "gl", "gd", "gco", "gb", "glog"],
        "docker": ["dp", "dpa", "di", "dex", "dlog", "dstop", "drm"],
        "system": ["ll", "la", "ports", "psg", "myip", "cpu", "mem", "disk"],
        "python": ["py", "pip", "venv", "pyserver"],
        "files": ["backup", "extract"],
        "prometheus": ["pstatus", "pref", "pstats", "pfind"]
    }
    
    def get_category(alias):
        for cat, alias_list in categories.items():
            if alias in alias_list:
                return cat
        return "custom"
    
    for alias, command in sorted(aliases.items()):
        category = get_category(alias)
        # Truncate long commands
        display_cmd = command if len(command) < 60 else command[:57] + "..."
        table.add_row(alias, display_cmd, category)
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Total: {len(aliases)} aliases[/dim]")
    console.print("[dim]Add alias: alias add <name> <command>[/dim]")
    console.print("[dim]Remove alias: alias remove <name>[/dim]")
