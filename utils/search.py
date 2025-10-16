"""Search and navigation utilities for Prometheus."""

import os
import subprocess
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def fuzzy_find_file(pattern: str, start_dir: str = ".") -> List[str]:
    """Fuzzy find files matching pattern."""
    try:
        result = subprocess.run(
            ["find", start_dir, "-type", "f", "-iname", f"*{pattern}*"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        files = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return files[:50]  # Limit to 50 results
    except Exception as e:
        console.print(f"[red]Search error: {e}[/red]")
        return []


def search_in_files(pattern: str, file_pattern: str = "*", directory: str = ".") -> None:
    """Search for pattern in files (smart grep)."""
    try:
        # Use ripgrep if available, otherwise fall back to grep
        cmd = None
        if subprocess.run(["which", "rg"], capture_output=True).returncode == 0:
            cmd = ["rg", "-n", "--color", "always", pattern, "-g", file_pattern, directory]
        else:
            cmd = ["grep", "-rn", "--color=always", pattern, directory]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.stdout:
            console.print(Panel(
                result.stdout[:2000],  # Limit output
                border_style="bright_cyan",
                title=f"[bold bright_cyan]🔍 Search Results: '{pattern}'[/bold bright_cyan]",
                title_align="left"
            ))
        else:
            console.print(f"[yellow]No matches found for '{pattern}'[/yellow]")
            
    except subprocess.TimeoutExpired:
        console.print("[red]Search timed out[/red]")
    except Exception as e:
        console.print(f"[red]Search error: {e}[/red]")


def find_in_codebase(function_name: str, extensions: Optional[List[str]] = None) -> None:
    """Find function/class definitions in codebase."""
    if extensions is None:
        extensions = [".py", ".js", ".java", ".cpp", ".c", ".go", ".rs"]
    
    ext_patterns = " -o ".join([f'-name "*{ext}"' for ext in extensions])
    
    try:
        # Find files with matching extensions
        find_cmd = f"find . -type f \\( {ext_patterns} \\) -exec grep -l '{function_name}' {{}} +"
        result = subprocess.run(find_cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        if result.stdout:
            files = result.stdout.strip().split('\n')
            
            table = Table(title=f"Files containing '{function_name}'", border_style="cyan")
            table.add_column("File", style="bright_white")
            table.add_column("Path", style="dim")
            
            for file_path in files[:20]:  # Limit to 20 results
                file_name = os.path.basename(file_path)
                dir_path = os.path.dirname(file_path) or "."
                table.add_row(file_name, dir_path)
            
            console.print(table)
        else:
            console.print(f"[yellow]No matches found for '{function_name}'[/yellow]")
            
    except subprocess.TimeoutExpired:
        console.print("[red]Search timed out[/red]")
    except Exception as e:
        console.print(f"[red]Search error: {e}[/red]")


def fuzzy_directory_search(pattern: str, max_depth: int = 3) -> List[str]:
    """Find directories matching pattern."""
    try:
        result = subprocess.run(
            ["find", ".", "-maxdepth", str(max_depth), "-type", "d", "-iname", f"*{pattern}*"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        dirs = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return dirs[:20]  # Limit to 20 results
    except Exception as e:
        console.print(f"[red]Directory search error: {e}[/red]")
        return []


def smart_cd(pattern: str) -> Optional[str]:
    """Smart directory change with fuzzy matching."""
    # First try exact match
    if os.path.isdir(pattern):
        return os.path.abspath(pattern)
    
    # Try fuzzy matching
    matches = fuzzy_directory_search(pattern)
    
    if not matches:
        console.print(f"[yellow]No directories found matching '{pattern}'[/yellow]")
        return None
    elif len(matches) == 1:
        return os.path.abspath(matches[0])
    else:
        # Show options
        table = Table(title=f"Multiple matches for '{pattern}'", border_style="cyan")
        table.add_column("#", style="dim")
        table.add_column("Directory", style="bright_white")
        
        for i, dir_path in enumerate(matches, 1):
            table.add_row(str(i), dir_path)
        
        console.print(table)
        console.print("[dim]Use the full path or refine your search[/dim]")
        return None


def show_project_structure(max_depth: int = 2) -> None:
    """Display project structure as a tree."""
    try:
        # Try to use 'tree' command if available
        if subprocess.run(["which", "tree"], capture_output=True).returncode == 0:
            result = subprocess.run(
                ["tree", "-L", str(max_depth), "-I", ".git|__pycache__|node_modules|.venv"],
                capture_output=True,
                text=True,
                timeout=5
            )
            console.print(result.stdout)
        else:
            # Fallback to simple ls -R
            result = subprocess.run(
                ["find", ".", "-maxdepth", str(max_depth), "-not", "-path", "*/.git/*", 
                 "-not", "-path", "*/__pycache__/*"],
                capture_output=True,
                text=True,
                timeout=5
            )
            console.print(result.stdout)
    except subprocess.TimeoutExpired:
        console.print("[red]Tree generation timed out[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def analyze_project() -> None:
    """Analyze current project and show statistics."""
    cwd = os.getcwd()
    
    # Check if it's a git repository
    is_git = os.path.isdir('.git')
    
    # Count files by extension
    extensions = {}
    total_files = 0
    total_size = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.startswith('.'):
                continue
            
            total_files += 1
            ext = os.path.splitext(file)[1] or 'no extension'
            extensions[ext] = extensions.get(ext, 0) + 1
            
            try:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
            except:
                pass
    
    # Create summary
    table = Table(title="Project Analysis", border_style="bright_cyan")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="bright_white")
    
    table.add_row("Directory", cwd)
    table.add_row("Git Repository", "Yes" if is_git else "No")
    table.add_row("Total Files", str(total_files))
    table.add_row("Total Size", f"{total_size / 1024 / 1024:.2f} MB")
    
    # Top file types
    top_extensions = sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:5]
    for ext, count in top_extensions:
        table.add_row(f"Files ({ext})", str(count))
    
    console.print(table)
    
    # If git repo, show git info
    if is_git:
        try:
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            commits = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True,
                text=True
            ).stdout.strip().split('\n')
            
            console.print(f"\n[cyan]Git Branch:[/cyan] {branch}")
            console.print(f"[cyan]Total Commits:[/cyan] {len(commits)}")
        except:
            pass
