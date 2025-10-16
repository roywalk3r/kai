"""Command suggestions and examples for Prometheus."""

from typing import List, Dict

# Common task categories and examples
SUGGESTIONS = {
    "file_operations": {
        "description": "File and directory operations",
        "examples": [
            "list all files in current directory",
            "create a file called notes.txt",
            "show contents of file.txt",
            "find all python files",
            "compress the logs folder",
            "extract archive.tar.gz",
            "copy file.txt to backup.txt",
            "delete old_file.txt",
            "rename file.txt to newname.txt",
        ]
    },
    "system_info": {
        "description": "System information and monitoring",
        "examples": [
            "show disk usage",
            "show memory usage",
            "what's my IP address",
            "show system information",
            "list running processes",
            "check CPU usage",
            "show network connections",
        ]
    },
    "text_processing": {
        "description": "Text search and manipulation",
        "examples": [
            "search for 'error' in log.txt",
            "count lines in file.txt",
            "show first 10 lines of file.txt",
            "find TODO comments in python files",
            "replace 'old' with 'new' in file.txt",
        ]
    },
    "git": {
        "description": "Git version control",
        "examples": [
            "show git status",
            "show git log",
            "show uncommitted changes",
            "list all branches",
            "show recent commits",
        ]
    },
    "network": {
        "description": "Network operations",
        "examples": [
            "ping google.com 5 times",
            "download file from URL",
            "check if port 8080 is open",
            "show my public IP",
        ]
    },
    "development": {
        "description": "Development tasks",
        "examples": [
            "count lines of code in python files",
            "find all imports in python files",
            "list files modified today",
            "show largest files in directory",
        ]
    }
}

def get_all_suggestions() -> Dict[str, Dict]:
    """Get all command suggestions organized by category."""
    return SUGGESTIONS

def search_suggestions(query: str) -> List[str]:
    """
    Search for suggestions matching a query.
    
    Args:
        query: Search term
        
    Returns:
        List of matching example commands
    """
    query_lower = query.lower()
    matches = []
    
    for category, data in SUGGESTIONS.items():
        for example in data["examples"]:
            if query_lower in example.lower():
                matches.append(example)
    
    return matches

def get_category_suggestions(category: str) -> List[str]:
    """
    Get suggestions for a specific category.
    
    Args:
        category: Category name
        
    Returns:
        List of example commands
    """
    if category in SUGGESTIONS:
        return SUGGESTIONS[category]["examples"]
    return []

def format_suggestions_help() -> str:
    """Format all suggestions as help text."""
    lines = ["# Command Examples\n"]
    
    for category, data in SUGGESTIONS.items():
        lines.append(f"\n## {data['description']}")
        for example in data["examples"]:
            lines.append(f"- {example}")
    
    return "\n".join(lines)
