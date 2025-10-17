#!/usr/bin/env python3
"""
Productivity tools: Bookmarks, Notes, and Favorites.
Combined module for quick-access features.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


# ==================== BOOKMARKS ====================

class BookmarkManager:
    """Manage directory bookmarks for quick navigation."""
    
    def __init__(self):
        self.bookmarks_file = Path.home() / ".prometheus" / "bookmarks.json"
        self.bookmarks = self._load()
    
    def _load(self) -> Dict[str, str]:
        """Load bookmarks from file."""
        if self.bookmarks_file.exists():
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        """Save bookmarks to file."""
        self.bookmarks_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.bookmarks_file, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)
    
    def add(self, name: str, path: str) -> bool:
        """Add a bookmark."""
        expanded_path = str(Path(path).expanduser().absolute())
        self.bookmarks[name] = expanded_path
        self._save()
        return True
    
    def remove(self, name: str) -> bool:
        """Remove a bookmark."""
        if name in self.bookmarks:
            del self.bookmarks[name]
            self._save()
            return True
        return False
    
    def get(self, name: str) -> Optional[str]:
        """Get bookmark path."""
        return self.bookmarks.get(name)
    
    def list_all(self) -> Dict[str, str]:
        """List all bookmarks."""
        return self.bookmarks.copy()


def show_bookmarks():
    """Display all bookmarks."""
    from rich.table import Table
    from rich.console import Console
    
    manager = BookmarkManager()
    bookmarks = manager.list_all()
    
    if not bookmarks:
        console = Console()
        console.print("[yellow]No bookmarks defined[/yellow]")
        console.print("[dim]Add one: bookmark add <name> <path>[/dim]")
        return
    
    table = Table(title="Directory Bookmarks", border_style="cyan")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Path", style="bright_white")
    
    for name, path in sorted(bookmarks.items()):
        # Check if path exists
        exists = Path(path).exists()
        status = "✓" if exists else "✗"
        table.add_row(f"{status} {name}", path)
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Jump to: jump <name>[/dim]")


# ==================== NOTES ====================

class NotesManager:
    """Manage quick notes per directory."""
    
    def __init__(self):
        self.notes_dir = Path.home() / ".prometheus" / "notes"
        self.notes_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_note_file(self, directory: Optional[str] = None) -> Path:
        """Get note file for directory."""
        if directory is None:
            directory = str(Path.cwd())
        
        # Create safe filename from path
        safe_name = directory.replace('/', '_').replace('\\', '_')
        return self.notes_dir / f"{safe_name}.json"
    
    def add(self, note: str, directory: Optional[str] = None, tags: Optional[List[str]] = None):
        """Add a note."""
        note_file = self._get_note_file(directory)
        
        # Load existing notes
        if note_file.exists():
            with open(note_file, 'r') as f:
                notes = json.load(f)
        else:
            notes = []
        
        # Add new note
        notes.append({
            "text": note,
            "timestamp": datetime.now().isoformat(),
            "tags": tags or []
        })
        
        # Save
        with open(note_file, 'w') as f:
            json.dump(notes, f, indent=2)
    
    def list_notes(self, directory: Optional[str] = None) -> List[Dict]:
        """List notes for directory."""
        note_file = self._get_note_file(directory)
        
        if note_file.exists():
            with open(note_file, 'r') as f:
                return json.load(f)
        return []
    
    def clear(self, directory: Optional[str] = None):
        """Clear notes for directory."""
        note_file = self._get_note_file(directory)
        if note_file.exists():
            note_file.unlink()
    
    def search(self, query: str) -> List[Dict]:
        """Search all notes."""
        results = []
        query_lower = query.lower()
        
        for note_file in self.notes_dir.glob("*.json"):
            try:
                with open(note_file, 'r') as f:
                    notes = json.load(f)
                    for note in notes:
                        if query_lower in note["text"].lower():
                            results.append({
                                **note,
                                "directory": note_file.stem.replace('_', '/')
                            })
            except:
                continue
        
        return results


def show_notes(directory: Optional[str] = None):
    """Display notes for current directory."""
    from rich.console import Console
    from rich.panel import Panel
    
    manager = NotesManager()
    notes = manager.list_notes(directory)
    
    console = Console()
    
    if not notes:
        console.print("[yellow]No notes for this directory[/yellow]")
        console.print("[dim]Add one: note \"your note here\"[/dim]")
        return
    
    dir_path = directory or str(Path.cwd())
    console.print(Panel(
        f"[bold bright_cyan]Notes for:[/bold bright_cyan] {dir_path}",
        border_style="cyan"
    ))
    
    for i, note in enumerate(notes, 1):
        timestamp = datetime.fromisoformat(note["timestamp"]).strftime("%Y-%m-%d %H:%M")
        tags = f" [{', '.join(note['tags'])}]" if note.get("tags") else ""
        
        console.print(f"\n[cyan]{i}.[/cyan] [dim]{timestamp}[/dim]{tags}")
        console.print(f"   {note['text']}")


# ==================== FAVORITES ====================

class FavoritesManager:
    """Manage favorite commands/snippets."""
    
    def __init__(self):
        self.favorites_file = Path.home() / ".prometheus" / "favorites.json"
        self.favorites = self._load()
    
    def _load(self) -> Dict:
        """Load favorites from file."""
        if self.favorites_file.exists():
            try:
                with open(self.favorites_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        """Save favorites to file."""
        self.favorites_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.favorites_file, 'w') as f:
            json.dump(self.favorites, f, indent=2)
    
    def add(self, name: str, command: str, description: str = "", category: str = "general") -> bool:
        """Add a favorite."""
        self.favorites[name] = {
            "command": command,
            "description": description,
            "category": category,
            "created": datetime.now().isoformat(),
            "usage_count": 0
        }
        self._save()
        return True
    
    def remove(self, name: str) -> bool:
        """Remove a favorite."""
        if name in self.favorites:
            del self.favorites[name]
            self._save()
            return True
        return False
    
    def get(self, name: str) -> Optional[Dict]:
        """Get favorite."""
        return self.favorites.get(name)
    
    def use(self, name: str) -> Optional[str]:
        """Use a favorite (increments counter)."""
        if name in self.favorites:
            self.favorites[name]["usage_count"] += 1
            self._save()
            return self.favorites[name]["command"]
        return None
    
    def list_all(self, category: Optional[str] = None) -> Dict:
        """List all favorites."""
        if category:
            return {k: v for k, v in self.favorites.items() if v.get("category") == category}
        return self.favorites.copy()


def show_favorites(category: Optional[str] = None):
    """Display favorites."""
    from rich.table import Table
    from rich.console import Console
    
    manager = FavoritesManager()
    favorites = manager.list_all(category)
    
    if not favorites:
        console = Console()
        console.print("[yellow]No favorites defined[/yellow]")
        console.print("[dim]Add one: favorite add <name> <command>[/dim]")
        return
    
    table = Table(title="Favorite Commands", border_style="cyan")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Command", style="bright_white")
    table.add_column("Category", style="dim")
    table.add_column("Used", justify="right", style="dim")
    
    for name, fav in sorted(favorites.items()):
        cmd = fav["command"]
        if len(cmd) > 50:
            cmd = cmd[:47] + "..."
        
        table.add_row(
            name,
            cmd,
            fav.get("category", "general"),
            str(fav.get("usage_count", 0))
        )
    
    console = Console()
    console.print(table)
    console.print(f"\n[dim]Use: fav <name> or favorite run <name>[/dim]")


# ==================== GLOBAL INSTANCES ====================

_bookmark_manager = None
_notes_manager = None
_favorites_manager = None


def get_bookmark_manager() -> BookmarkManager:
    """Get global bookmark manager."""
    global _bookmark_manager
    if _bookmark_manager is None:
        _bookmark_manager = BookmarkManager()
    return _bookmark_manager


def get_notes_manager() -> NotesManager:
    """Get global notes manager."""
    global _notes_manager
    if _notes_manager is None:
        _notes_manager = NotesManager()
    return _notes_manager


def get_favorites_manager() -> FavoritesManager:
    """Get global favorites manager."""
    global _favorites_manager
    if _favorites_manager is None:
        _favorites_manager = FavoritesManager()
    return _favorites_manager
