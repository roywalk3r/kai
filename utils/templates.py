#!/usr/bin/env python3
"""
Template system for saving and reusing command workflows.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime


class Template:
    """Command template with parameters."""
    
    def __init__(
        self,
        name: str,
        description: str,
        commands: List[str],
        parameters: Optional[Dict[str, str]] = None,
        category: str = "custom"
    ):
        self.name = name
        self.description = description
        self.commands = commands
        self.parameters = parameters or {}
        self.category = category
        self.created_at = datetime.now().isoformat()
        self.usage_count = 0
    
    def render(self, params: Dict[str, str]) -> List[str]:
        """
        Render template with parameters.
        
        Args:
            params: Parameter values
        
        Returns:
            List of rendered commands
        """
        rendered = []
        
        for command in self.commands:
            rendered_cmd = command
            
            # Replace parameters
            for param_name, param_value in params.items():
                placeholder = f"{{{param_name}}}"
                rendered_cmd = rendered_cmd.replace(placeholder, param_value)
            
            rendered.append(rendered_cmd)
        
        return rendered
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "commands": self.commands,
            "parameters": self.parameters,
            "category": self.category,
            "created_at": self.created_at,
            "usage_count": self.usage_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Template':
        """Create template from dictionary."""
        template = cls(
            name=data["name"],
            description=data["description"],
            commands=data["commands"],
            parameters=data.get("parameters"),
            category=data.get("category", "custom")
        )
        template.created_at = data.get("created_at", datetime.now().isoformat())
        template.usage_count = data.get("usage_count", 0)
        return template


class TemplateManager:
    """Manage command templates."""
    
    def __init__(self):
        self.templates_file = Path.home() / ".prometheus" / "templates.json"
        self.templates = self._load_templates()
        
        # Initialize with built-in templates
        if not self.templates:
            self._create_builtin_templates()
    
    def _load_templates(self) -> Dict[str, Template]:
        """Load templates from file."""
        if self.templates_file.exists():
            try:
                with open(self.templates_file, 'r') as f:
                    data = json.load(f)
                return {
                    name: Template.from_dict(template_data)
                    for name, template_data in data.items()
                }
            except:
                return {}
        return {}
    
    def _save_templates(self):
        """Save templates to file."""
        self.templates_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            name: template.to_dict()
            for name, template in self.templates.items()
        }
        
        with open(self.templates_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_builtin_templates(self):
        """Create built-in templates."""
        builtins = [
            Template(
                name="backup",
                description="Backup a directory",
                commands=[
                    "tar -czf {backup_name}_$(date +%Y%m%d_%H%M%S).tar.gz {source_dir}"
                ],
                parameters={
                    "backup_name": "Name for backup file",
                    "source_dir": "Directory to backup"
                },
                category="files"
            ),
            Template(
                name="git-workflow",
                description="Standard Git workflow",
                commands=[
                    "git add .",
                    "git commit -m \"{message}\"",
                    "git push origin {branch}"
                ],
                parameters={
                    "message": "Commit message",
                    "branch": "Branch name (default: main)"
                },
                category="git"
            ),
            Template(
                name="python-project",
                description="Initialize Python project",
                commands=[
                    "mkdir {project_name}",
                    "cd {project_name}",
                    "python3 -m venv venv",
                    "source venv/bin/activate",
                    "pip install {packages}",
                    "echo '{packages}' > requirements.txt"
                ],
                parameters={
                    "project_name": "Project directory name",
                    "packages": "Packages to install"
                },
                category="python"
            ),
            Template(
                name="docker-cleanup",
                description="Clean up Docker resources",
                commands=[
                    "docker stop $(docker ps -aq)",
                    "docker rm $(docker ps -aq)",
                    "docker rmi $(docker images -q -f dangling=true)",
                    "docker volume prune -f",
                    "docker network prune -f"
                ],
                parameters={},
                category="docker"
            ),
            Template(
                name="web-server",
                description="Start a simple web server",
                commands=[
                    "python3 -m http.server {port}"
                ],
                parameters={
                    "port": "Port number (default: 8000)"
                },
                category="dev"
            ),
            Template(
                name="find-large-files",
                description="Find large files in directory",
                commands=[
                    "find {directory} -type f -size +{size} -exec ls -lh {} \\; | sort -k5 -hr | head -n {limit}"
                ],
                parameters={
                    "directory": "Directory to search",
                    "size": "Minimum size (e.g., 100M)",
                    "limit": "Number of results"
                },
                category="system"
            ),
            Template(
                name="system-info",
                description="Gather system information",
                commands=[
                    "echo '=== CPU Info ===' && lscpu | grep 'Model name\\|CPU(s)'",
                    "echo '\\n=== Memory ===' && free -h",
                    "echo '\\n=== Disk ===' && df -h",
                    "echo '\\n=== Network ===' && ip a | grep 'inet '"
                ],
                parameters={},
                category="system"
            ),
        ]
        
        for template in builtins:
            self.templates[template.name] = template
        
        self._save_templates()
    
    def create_template(
        self,
        name: str,
        description: str,
        commands: List[str],
        parameters: Optional[Dict[str, str]] = None,
        category: str = "custom"
    ) -> bool:
        """
        Create a new template.
        
        Args:
            name: Template name
            description: Template description
            commands: List of commands
            parameters: Optional parameters
            category: Template category
        
        Returns:
            True if created successfully
        """
        if name in self.templates:
            return False
        
        template = Template(name, description, commands, parameters, category)
        self.templates[name] = template
        self._save_templates()
        return True
    
    def get_template(self, name: str) -> Optional[Template]:
        """Get template by name."""
        return self.templates.get(name)
    
    def delete_template(self, name: str) -> bool:
        """Delete a template."""
        if name in self.templates:
            # Don't delete built-in templates
            if self.templates[name].category != "custom":
                return False
            
            del self.templates[name]
            self._save_templates()
            return True
        return False
    
    def list_templates(self, category: Optional[str] = None) -> List[Template]:
        """
        List templates.
        
        Args:
            category: Optional category filter
        
        Returns:
            List of templates
        """
        templates = list(self.templates.values())
        
        if category:
            templates = [t for t in templates if t.category == category]
        
        return sorted(templates, key=lambda t: t.name)
    
    def get_categories(self) -> List[str]:
        """Get all template categories."""
        categories = set(t.category for t in self.templates.values())
        return sorted(categories)
    
    def use_template(self, name: str, params: Dict[str, str]) -> List[str]:
        """
        Use a template with parameters.
        
        Args:
            name: Template name
            params: Parameter values
        
        Returns:
            List of rendered commands
        """
        template = self.get_template(name)
        if not template:
            return []
        
        # Increment usage count
        template.usage_count += 1
        self._save_templates()
        
        return template.render(params)
    
    def export_template(self, name: str, output_file: Path) -> bool:
        """Export template to file."""
        template = self.get_template(name)
        if not template:
            return False
        
        with open(output_file, 'w') as f:
            json.dump(template.to_dict(), f, indent=2)
        
        return True
    
    def import_template(self, input_file: Path) -> bool:
        """Import template from file."""
        try:
            with open(input_file, 'r') as f:
                data = json.load(f)
            
            template = Template.from_dict(data)
            
            # Avoid name conflicts
            if template.name in self.templates:
                template.name = f"{template.name}_imported"
            
            self.templates[template.name] = template
            self._save_templates()
            return True
        except:
            return False


# Global template manager
_template_manager = None


def get_template_manager() -> TemplateManager:
    """Get global template manager instance."""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager


def list_templates(category: Optional[str] = None) -> List[Template]:
    """List available templates."""
    return get_template_manager().list_templates(category)


def use_template(name: str, params: Dict[str, str]) -> List[str]:
    """Use a template."""
    return get_template_manager().use_template(name, params)


def create_template(
    name: str,
    description: str,
    commands: List[str],
    parameters: Optional[Dict[str, str]] = None
) -> bool:
    """Create a template."""
    return get_template_manager().create_template(name, description, commands, parameters)


def show_templates():
    """Display templates in a formatted table."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    
    manager = get_template_manager()
    templates = manager.list_templates()
    
    if not templates:
        console = Console()
        console.print("[yellow]No templates available[/yellow]")
        return
    
    console = Console()
    
    # Group by category
    categories = manager.get_categories()
    
    for category in categories:
        category_templates = [t for t in templates if t.category == category]
        
        if not category_templates:
            continue
        
        table = Table(title=f"{category.title()} Templates", border_style="cyan")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="bright_white")
        table.add_column("Commands", justify="center", style="dim")
        table.add_column("Used", justify="center", style="dim")
        
        for template in category_templates:
            table.add_row(
                template.name,
                template.description,
                str(len(template.commands)),
                str(template.usage_count)
            )
        
        console.print(table)
        console.print()
    
    console.print(f"[dim]Total: {len(templates)} templates[/dim]")
    console.print("[dim]Use template: template use <name>[/dim]")
    console.print("[dim]Create template: template create <name>[/dim]")


def show_template_details(name: str):
    """Show detailed template information."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    
    manager = get_template_manager()
    template = manager.get_template(name)
    
    if not template:
        console = Console()
        console.print(f"[red]Template '{name}' not found[/red]")
        return
    
    console = Console()
    
    # Template info
    console.print(Panel(
        f"[bold bright_cyan]Name:[/bold bright_cyan] {template.name}\n"
        f"[bold bright_cyan]Description:[/bold bright_cyan] {template.description}\n"
        f"[bold bright_cyan]Category:[/bold bright_cyan] {template.category}\n"
        f"[bold bright_cyan]Used:[/bold bright_cyan] {template.usage_count} times",
        title="[bold]Template Details[/bold]",
        border_style="cyan"
    ))
    
    # Parameters
    if template.parameters:
        console.print("\n[bold]Parameters:[/bold]")
        for param, desc in template.parameters.items():
            console.print(f"  • [cyan]{{{param}}}[/cyan]: {desc}")
    
    # Commands
    console.print("\n[bold]Commands:[/bold]")
    for i, cmd in enumerate(template.commands, 1):
        console.print(f"  {i}. [dim]{cmd}[/dim]")
    
    # Usage example
    if template.parameters:
        console.print("\n[bold]Usage Example:[/bold]")
        example_params = {param: f"<{param}>" for param in template.parameters.keys()}
        console.print(f"  template use {template.name} {' '.join(f'{k}={v}' for k, v in example_params.items())}")
