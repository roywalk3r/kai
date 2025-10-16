"""Context-aware command suggestions and utilities."""

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class ContextAnalyzer:
    """Analyze current directory context and provide smart suggestions."""
    
    def __init__(self):
        self.cwd = os.getcwd()
        self.context = self._analyze_context()
    
    def _analyze_context(self) -> Dict:
        """Analyze current directory and detect project type."""
        context = {
            'is_git': os.path.isdir('.git'),
            'is_python': os.path.isfile('requirements.txt') or os.path.isfile('setup.py'),
            'is_node': os.path.isfile('package.json'),
            'is_rust': os.path.isfile('Cargo.toml'),
            'is_go': os.path.isfile('go.mod'),
            'is_docker': os.path.isfile('Dockerfile') or os.path.isfile('docker-compose.yml'),
            'has_makefile': os.path.isfile('Makefile'),
            'has_venv': os.path.isdir('.venv') or os.path.isdir('venv'),
        }
        return context
    
    def get_relevant_commands(self) -> List[str]:
        """Get relevant commands based on current context."""
        commands = []
        
        if self.context['is_git']:
            commands.extend([
                "git status",
                "git log -n 5",
                "git branch",
                "git diff",
            ])
        
        if self.context['is_python']:
            commands.extend([
                "pip list",
                "python --version",
                "pytest",
            ])
            if self.context['has_venv']:
                commands.append("source .venv/bin/activate")
        
        if self.context['is_node']:
            commands.extend([
                "npm install",
                "npm run dev",
                "npm test",
                "npm list",
            ])
        
        if self.context['is_docker']:
            commands.extend([
                "docker ps",
                "docker-compose up",
                "docker images",
            ])
        
        if self.context['has_makefile']:
            commands.extend([
                "make",
                "make help",
            ])
        
        return commands
    
    def show_context_help(self):
        """Show context-specific help."""
        relevant_commands = self.get_relevant_commands()
        
        if not relevant_commands:
            console.print("[yellow]No specific context detected. Showing general commands.[/yellow]")
            relevant_commands = [
                "ls -la",
                "pwd",
                "df -h",
                "ps aux",
            ]
        
        # Detect project type
        project_types = []
        if self.context['is_git']:
            project_types.append("Git Repository")
        if self.context['is_python']:
            project_types.append("Python Project")
        if self.context['is_node']:
            project_types.append("Node.js Project")
        if self.context['is_docker']:
            project_types.append("Docker Project")
        
        output = f"[bold cyan]Directory:[/bold cyan] {self.cwd}\n\n"
        
        if project_types:
            output += f"[bold cyan]Detected:[/bold cyan] {', '.join(project_types)}\n\n"
        
        output += "[bold cyan]Relevant Commands:[/bold cyan]\n"
        for cmd in relevant_commands:
            output += f"  • [bright_white]{cmd}[/bright_white]\n"
        
        console.print(Panel(
            output.rstrip(),
            border_style="bright_cyan",
            title="[bold bright_cyan]📋 Context Reference[/bold bright_cyan]",
            title_align="left"
        ))


def get_git_status() -> Optional[Dict]:
    """Get git repository status."""
    if not os.path.isdir('.git'):
        return None
    
    try:
        # Get current branch
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=2
        ).stdout.strip()
        
        # Get status
        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=2
        ).stdout.strip()
        
        # Count changes
        lines = status.split('\n') if status else []
        modified = sum(1 for line in lines if line.startswith(' M'))
        added = sum(1 for line in lines if line.startswith('A'))
        deleted = sum(1 for line in lines if line.startswith(' D'))
        untracked = sum(1 for line in lines if line.startswith('??'))
        
        return {
            'branch': branch,
            'modified': modified,
            'added': added,
            'deleted': deleted,
            'untracked': untracked,
            'clean': len(lines) == 0
        }
    except:
        return None


def show_quick_status():
    """Show quick status of current directory context."""
    analyzer = ContextAnalyzer()
    
    table = Table(title="Quick Status", border_style="bright_cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="bright_white")
    
    table.add_row("Directory", os.getcwd())
    
    # Git status
    if analyzer.context['is_git']:
        git_status = get_git_status()
        if git_status:
            status_str = f"Branch: {git_status['branch']}"
            if git_status['clean']:
                status_str += " (clean)"
            else:
                changes = []
                if git_status['modified']:
                    changes.append(f"{git_status['modified']}M")
                if git_status['added']:
                    changes.append(f"{git_status['added']}A")
                if git_status['deleted']:
                    changes.append(f"{git_status['deleted']}D")
                if git_status['untracked']:
                    changes.append(f"{git_status['untracked']}??")
                status_str += f" ({', '.join(changes)})"
            table.add_row("Git", status_str)
    
    # Python environment
    if analyzer.context['is_python']:
        python_version = subprocess.run(
            ["python", "--version"],
            capture_output=True,
            text=True
        ).stdout.strip()
        table.add_row("Python", python_version)
        
        if analyzer.context['has_venv']:
            venv_active = os.environ.get('VIRTUAL_ENV')
            table.add_row("Virtual Env", "Active" if venv_active else "Inactive")
    
    # Node.js
    if analyzer.context['is_node']:
        try:
            node_version = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True
            ).stdout.strip()
            table.add_row("Node.js", node_version)
        except:
            pass
    
    # Docker
    if analyzer.context['is_docker']:
        try:
            containers = subprocess.run(
                ["docker", "ps", "-q"],
                capture_output=True,
                text=True
            ).stdout.strip().split('\n')
            running = len([c for c in containers if c])
            table.add_row("Docker", f"{running} containers running")
        except:
            pass
    
    console.print(table)


def suggest_next_command(last_command: str) -> Optional[str]:
    """Suggest next logical command based on last command."""
    suggestions = {
        'git add': 'git commit -m "message"',
        'git commit': 'git push',
        'git clone': 'cd <repo-name>',
        'npm install': 'npm run dev',
        'pip install': 'python main.py',
        'make': 'make install',
        'docker build': 'docker run',
        'pytest': 'coverage report',
    }
    
    # Check if last command starts with any key
    for prefix, suggestion in suggestions.items():
        if last_command.startswith(prefix):
            return suggestion
    
    return None


def get_command_explanation(command: str) -> str:
    """Get a brief explanation of what a command does."""
    explanations = {
        'ls': 'List directory contents',
        'cd': 'Change directory',
        'pwd': 'Print working directory',
        'git status': 'Show git repository status',
        'git log': 'Show commit history',
        'git diff': 'Show changes',
        'docker ps': 'List running containers',
        'npm install': 'Install Node.js dependencies',
        'pip install': 'Install Python packages',
        'pytest': 'Run Python tests',
    }
    
    # Try exact match
    if command in explanations:
        return explanations[command]
    
    # Try partial match (first two words)
    words = command.split()
    if len(words) >= 2:
        partial = ' '.join(words[:2])
        if partial in explanations:
            return explanations[partial]
    
    # Try first word
    if words:
        first_word = words[0]
        if first_word in explanations:
            return explanations[first_word]
    
    return "Command execution"
