#!/usr/bin/env python3
"""
Project context - provides intelligent project descriptions and summaries.
"""

import os
from pathlib import Path
from typing import Dict, Optional, List
import subprocess


class ProjectContext:
    """Analyze and describe the current project."""
    
    def __init__(self):
        self.cwd = Path.cwd()
        self.project_name = self.cwd.name
        self.readme_content = None
        self.git_info = {}
        self.file_stats = {}
        self.language_stats = {}
    
    def get_description(self) -> str:
        """Get an intelligent project description."""
        parts = []
        
        # Project name and location
        parts.append(f"📁 **Project:** {self.project_name}")
        parts.append(f"📍 **Location:** {self.cwd}")
        
        # Check for README
        readme_path = self._find_readme()
        if readme_path:
            self.readme_content = self._read_file(readme_path)
            if self.readme_content:
                # Extract first paragraph or description
                lines = self.readme_content.split('\n')
                desc_lines = []
                for line in lines[1:20]:  # Skip title, look in first 20 lines
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('```'):
                        desc_lines.append(line)
                        if len(desc_lines) >= 3:
                            break
                
                if desc_lines:
                    parts.append(f"\n📄 **Description:**\n{' '.join(desc_lines)}")
        
        # Git info
        if self._is_git_repo():
            self._collect_git_info()
            if self.git_info:
                parts.append(f"\n🔀 **Git:**")
                if 'branch' in self.git_info:
                    parts.append(f"  • Branch: {self.git_info['branch']}")
                if 'commits' in self.git_info:
                    parts.append(f"  • Commits: {self.git_info['commits']}")
                if 'remote' in self.git_info:
                    parts.append(f"  • Remote: {self.git_info['remote']}")
        
        # Language detection
        self._detect_languages()
        if self.language_stats:
            parts.append(f"\n💻 **Languages:**")
            for lang, count in sorted(self.language_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                parts.append(f"  • {lang}: {count} files")
        
        # Project structure
        structure = self._get_structure()
        if structure:
            parts.append(f"\n📂 **Structure:**")
            parts.extend([f"  {line}" for line in structure[:10]])
        
        # Dependencies
        deps = self._find_dependencies()
        if deps:
            parts.append(f"\n📦 **Dependencies:**")
            parts.append(f"  • {deps}")
        
        return '\n'.join(parts)
    
    def get_summary(self) -> Dict:
        """Get project summary as structured data."""
        return {
            "name": self.project_name,
            "path": str(self.cwd),
            "readme_exists": self._find_readme() is not None,
            "is_git": self._is_git_repo(),
            "languages": self.language_stats,
            "git_info": self.git_info,
        }
    
    def _find_readme(self) -> Optional[Path]:
        """Find README file."""
        candidates = ['README.md', 'README.MD', 'README', 'README.txt', 'README.rst']
        for name in candidates:
            path = self.cwd / name
            if path.exists():
                return path
        return None
    
    def _read_file(self, path: Path, max_size: int = 10000) -> Optional[str]:
        """Read file safely."""
        try:
            if path.stat().st_size > max_size:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(max_size)
            else:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except:
            return None
    
    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repo."""
        return (self.cwd / '.git').exists()
    
    def _collect_git_info(self):
        """Collect git information."""
        try:
            # Current branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                self.git_info['branch'] = result.stdout.strip()
            
            # Commit count
            result = subprocess.run(
                ['git', 'rev-list', '--count', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                self.git_info['commits'] = result.stdout.strip()
            
            # Remote URL
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                self.git_info['remote'] = result.stdout.strip()
        except:
            pass
    
    def _detect_languages(self):
        """Detect programming languages in project."""
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.cs': 'C#',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.jsx': 'React',
            '.tsx': 'React/TS',
            '.vue': 'Vue',
            '.sh': 'Shell',
        }
        
        lang_count = {}
        
        for root, dirs, files in os.walk(self.cwd):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'build', 'dist'}]
            
            for file in files:
                ext = Path(file).suffix.lower()
                if ext in extensions:
                    lang = extensions[ext]
                    lang_count[lang] = lang_count.get(lang, 0) + 1
        
        self.language_stats = lang_count
    
    def _get_structure(self) -> List[str]:
        """Get project directory structure."""
        structure = []
        
        # Get top-level items
        try:
            items = sorted(self.cwd.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            
            for item in items[:15]:  # Limit to 15 items
                if item.name.startswith('.') and item.name not in {'.github', '.gitlab'}:
                    continue
                
                if item.is_dir():
                    # Count files in directory
                    try:
                        count = len(list(item.glob('*')))
                        structure.append(f"📁 {item.name}/ ({count} items)")
                    except:
                        structure.append(f"📁 {item.name}/")
                else:
                    # Show file with size
                    try:
                        size = item.stat().st_size
                        if size < 1024:
                            size_str = f"{size}B"
                        elif size < 1024 * 1024:
                            size_str = f"{size/1024:.1f}KB"
                        else:
                            size_str = f"{size/(1024*1024):.1f}MB"
                        structure.append(f"📄 {item.name} ({size_str})")
                    except:
                        structure.append(f"📄 {item.name}")
        except:
            pass
        
        return structure
    
    def _find_dependencies(self) -> Optional[str]:
        """Find and describe dependencies."""
        dep_files = {
            'requirements.txt': 'Python',
            'package.json': 'Node.js',
            'Cargo.toml': 'Rust',
            'pom.xml': 'Maven/Java',
            'build.gradle': 'Gradle/Java',
            'Gemfile': 'Ruby',
            'composer.json': 'PHP',
            'go.mod': 'Go',
        }
        
        found = []
        for filename, lang in dep_files.items():
            if (self.cwd / filename).exists():
                found.append(f"{lang} ({filename})")
        
        return ', '.join(found) if found else None


def show_project_description():
    """Display project description."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    
    console = Console()
    
    context = ProjectContext()
    description = context.get_description()
    
    console.print(Panel(
        Markdown(description),
        title="[bold cyan]📊 Project Overview[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))


def get_project_context_for_ai() -> str:
    """Get concise project context for AI queries."""
    context = ProjectContext()
    
    parts = [f"Current project: {context.project_name}"]
    
    # README summary
    readme_path = context._find_readme()
    if readme_path:
        content = context._read_file(readme_path, max_size=2000)
        if content:
            # Get first few meaningful lines
            lines = content.split('\n')
            desc = []
            for line in lines[:15]:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('```'):
                    desc.append(line)
                    if len(desc) >= 3:
                        break
            if desc:
                parts.append(f"Description: {' '.join(desc)}")
    
    # Languages
    context._detect_languages()
    if context.language_stats:
        langs = ', '.join([f"{lang} ({count} files)" for lang, count in 
                          sorted(context.language_stats.items(), key=lambda x: x[1], reverse=True)[:3]])
        parts.append(f"Languages: {langs}")
    
    # Git info
    if context._is_git_repo():
        context._collect_git_info()
        if 'branch' in context.git_info:
            parts.append(f"Git branch: {context.git_info['branch']}")
    
    return ". ".join(parts)


_project_context_cache = None
_cache_dir = None

def get_cached_project_context() -> str:
    """Get cached project context (refreshes if directory changed)."""
    global _project_context_cache, _cache_dir
    
    current_dir = str(Path.cwd())
    
    if _cache_dir != current_dir or _project_context_cache is None:
        _cache_dir = current_dir
        _project_context_cache = get_project_context_for_ai()
    
    return _project_context_cache
