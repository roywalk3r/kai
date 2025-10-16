"""Plugin system for Prometheus terminal assistant."""

import os
import json
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Callable
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class Plugin:
    """Base class for Prometheus plugins."""
    
    def __init__(self):
        self.name = "Unknown Plugin"
        self.version = "1.0.0"
        self.description = "No description"
        self.author = "Unknown"
        self.commands = {}
    
    def initialize(self):
        """Initialize the plugin. Override this method."""
        pass
    
    def register_command(self, command: str, handler: Callable):
        """Register a command handler."""
        self.commands[command] = handler
    
    def handle_command(self, command: str, args: List[str]) -> bool:
        """Handle a command. Returns True if handled, False otherwise."""
        if command in self.commands:
            self.commands[command](args)
            return True
        return False


class PluginManager:
    """Manages plugins for Prometheus."""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dir = Path.home() / ".prometheus" / "plugins"
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
        # Create plugin registry file if it doesn't exist
        self.registry_file = self.plugin_dir / "registry.json"
        if not self.registry_file.exists():
            self._save_registry({})
    
    def _load_registry(self) -> Dict:
        """Load plugin registry."""
        try:
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_registry(self, registry: Dict):
        """Save plugin registry."""
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def load_plugin(self, plugin_path: Path) -> Optional[Plugin]:
        """Load a single plugin from file."""
        try:
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for Plugin class in module
                if hasattr(module, 'PrometheusPlugin'):
                    plugin = module.PrometheusPlugin()
                    plugin.initialize()
                    return plugin
        except Exception as e:
            console.print(f"[red]Error loading plugin {plugin_path}: {e}[/red]")
        return None
    
    def load_all_plugins(self):
        """Load all plugins from plugin directory."""
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            plugin = self.load_plugin(plugin_file)
            if plugin:
                self.plugins[plugin.name] = plugin
                console.print(f"[green]✓ Loaded plugin: {plugin.name} v{plugin.version}[/green]")
    
    def install_plugin(self, plugin_name: str, source: str):
        """Install a plugin from a source (URL or path)."""
        # In a real implementation, this would download and install the plugin
        console.print(Panel(
            f"[bright_white]Installing plugin:[/bright_white] {plugin_name}\n"
            f"[bright_white]Source:[/bright_white] {source}\n\n"
            f"[dim]Feature coming soon: Plugin installation from repositories[/dim]",
            border_style="bright_cyan",
            title="[bold bright_cyan]📦 Plugin Installation[/bold bright_cyan]",
            title_align="left"
        ))
    
    def uninstall_plugin(self, plugin_name: str):
        """Uninstall a plugin."""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            
            # Remove from disk
            plugin_file = self.plugin_dir / f"{plugin_name}.py"
            if plugin_file.exists():
                plugin_file.unlink()
            
            console.print(f"[green]✓ Uninstalled plugin: {plugin_name}[/green]")
        else:
            console.print(f"[yellow]Plugin not found: {plugin_name}[/yellow]")
    
    def list_plugins(self):
        """List all installed plugins."""
        if not self.plugins:
            console.print("[yellow]No plugins installed[/yellow]")
            console.print("\n[dim]Install plugins with: prom plugin install <name>[/dim]")
            return
        
        table = Table(title="Installed Plugins", border_style="bright_cyan")
        table.add_column("Name", style="cyan")
        table.add_column("Version", style="bright_white")
        table.add_column("Description", style="dim")
        table.add_column("Author", style="dim")
        
        for plugin in self.plugins.values():
            table.add_row(plugin.name, plugin.version, plugin.description, plugin.author)
        
        console.print(table)
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def handle_command(self, command: str, args: List[str]) -> bool:
        """Try to handle command with plugins. Returns True if handled."""
        for plugin in self.plugins.values():
            if plugin.handle_command(command, args):
                return True
        return False


# Global plugin manager instance
_plugin_manager = None


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager


# Example plugin template
EXAMPLE_PLUGIN_TEMPLATE = '''"""
Example Prometheus Plugin

This is a template for creating Prometheus plugins.
"""

from core.plugins import Plugin

class PrometheusPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.name = "Example Plugin"
        self.version = "1.0.0"
        self.description = "An example plugin"
        self.author = "Your Name"
    
    def initialize(self):
        """Initialize the plugin."""
        # Register commands
        self.register_command("example", self.handle_example)
    
    def handle_example(self, args):
        """Handle the 'example' command."""
        print(f"Example command called with args: {args}")
'''


def create_plugin_template(name: str):
    """Create a plugin template file."""
    plugin_manager = get_plugin_manager()
    plugin_file = plugin_manager.plugin_dir / f"{name}.py"
    
    if plugin_file.exists():
        console.print(f"[yellow]Plugin file already exists: {plugin_file}[/yellow]")
        return
    
    template = EXAMPLE_PLUGIN_TEMPLATE.replace("Example Plugin", name.title())
    template = template.replace("example", name.lower())
    
    with open(plugin_file, 'w') as f:
        f.write(template)
    
    console.print(Panel(
        f"[green]✓ Plugin template created:[/green]\n{plugin_file}\n\n"
        f"[bright_white]Next steps:[/bright_white]\n"
        f"1. Edit the plugin file\n"
        f"2. Reload Prometheus\n"
        f"3. Your plugin will be automatically loaded",
        border_style="bright_cyan",
        title="[bold bright_cyan]📝 Plugin Created[/bold bright_cyan]",
        title_align="left"
    ))
