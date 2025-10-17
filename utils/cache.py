#!/usr/bin/env python3
"""
Response caching system for faster repeated queries.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime, timedelta


class ResponseCache:
    """Cache for AI responses and search results."""
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl_minutes: int = 60):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory for cache files
            ttl_minutes: Time-to-live for cache entries in minutes
        """
        self.cache_dir = cache_dir or (Path.home() / ".prometheus" / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.ttl = timedelta(minutes=ttl_minutes)
        self.cache_file = self.cache_dir / "response_cache.json"
        self.cache = self._load_cache()
        
        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "saves": 0
        }
    
    def _load_cache(self) -> Dict:
        """Load cache from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _generate_key(self, query: str, context: Optional[str] = None) -> str:
        """
        Generate cache key from query and context.
        
        Args:
            query: User query
            context: Optional context (e.g., current directory)
        
        Returns:
            Cache key (hash)
        """
        # Normalize query
        normalized = query.lower().strip()
        
        # Include context if provided
        if context:
            normalized = f"{normalized}|{context}"
        
        # Generate hash
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]
    
    def get(self, query: str, context: Optional[str] = None) -> Optional[Dict]:
        """
        Get cached response.
        
        Args:
            query: User query
            context: Optional context
        
        Returns:
            Cached response or None
        """
        key = self._generate_key(query, context)
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check if expired
            cached_time = datetime.fromisoformat(entry.get("timestamp", "2000-01-01"))
            if datetime.now() - cached_time < self.ttl:
                self.stats["hits"] += 1
                return entry.get("response")
            else:
                # Remove expired entry
                del self.cache[key]
                self._save_cache()
        
        self.stats["misses"] += 1
        return None
    
    def set(self, query: str, response: Dict, context: Optional[str] = None):
        """
        Cache a response.
        
        Args:
            query: User query
            response: Response to cache
            context: Optional context
        """
        key = self._generate_key(query, context)
        
        self.cache[key] = {
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }
        
        self.stats["saves"] += 1
        self._save_cache()
    
    def invalidate(self, query: Optional[str] = None):
        """
        Invalidate cache entries.
        
        Args:
            query: Optional specific query to invalidate. If None, clear all.
        """
        if query:
            key = self._generate_key(query)
            if key in self.cache:
                del self.cache[key]
        else:
            self.cache.clear()
        
        self._save_cache()
    
    def clean_expired(self) -> int:
        """
        Remove expired cache entries.
        
        Returns:
            Number of entries removed
        """
        now = datetime.now()
        expired_keys = []
        
        for key, entry in self.cache.items():
            cached_time = datetime.fromisoformat(entry.get("timestamp", "2000-01-01"))
            if now - cached_time >= self.ttl:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
        
        if expired_keys:
            self._save_cache()
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "saves": self.stats["saves"],
            "hit_rate": f"{hit_rate:.1f}%",
            "cache_size": len(self.cache),
            "cache_file_size": self._get_cache_file_size()
        }
    
    def _get_cache_file_size(self) -> str:
        """Get cache file size in human-readable format."""
        if self.cache_file.exists():
            size_bytes = self.cache_file.stat().st_size
            for unit in ['B', 'KB', 'MB']:
                if size_bytes < 1024:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024
            return f"{size_bytes:.1f} GB"
        return "0 B"
    
    def should_cache(self, query: str) -> bool:
        """
        Determine if a query should be cached.
        
        Args:
            query: User query
        
        Returns:
            True if should cache
        """
        # Don't cache very short queries
        if len(query.strip()) < 3:
            return False
        
        # Don't cache commands with time-sensitive operations
        time_sensitive = [
            "now", "today", "current", "latest", "recent",
            "status", "ps", "top", "watch"
        ]
        
        query_lower = query.lower()
        if any(word in query_lower for word in time_sensitive):
            return False
        
        return True


class SearchCache:
    """Specialized cache for search results."""
    
    def __init__(self, ttl_minutes: int = 30):
        self.cache_dir = Path.home() / ".prometheus" / "cache"
        self.cache_file = self.cache_dir / "search_cache.json"
        self.ttl = timedelta(minutes=ttl_minutes)
        self.cache = self._load()
    
    def _load(self) -> Dict:
        """Load search cache."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save(self):
        """Save search cache."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
    
    def get_file_search(self, pattern: str, directory: str) -> Optional[List]:
        """Get cached file search results."""
        key = f"file:{pattern}:{directory}"
        return self._get(key)
    
    def set_file_search(self, pattern: str, directory: str, results: List):
        """Cache file search results."""
        key = f"file:{pattern}:{directory}"
        self._set(key, results)
    
    def get_content_search(self, pattern: str, directory: str) -> Optional[List]:
        """Get cached content search results."""
        key = f"content:{pattern}:{directory}"
        return self._get(key)
    
    def set_content_search(self, pattern: str, directory: str, results: List):
        """Cache content search results."""
        key = f"content:{pattern}:{directory}"
        self._set(key, results)
    
    def _get(self, key: str) -> Optional[Any]:
        """Get from cache with TTL check."""
        if key in self.cache:
            entry = self.cache[key]
            cached_time = datetime.fromisoformat(entry["timestamp"])
            if datetime.now() - cached_time < self.ttl:
                return entry["data"]
            else:
                del self.cache[key]
        return None
    
    def _set(self, key: str, data: Any):
        """Set cache entry."""
        self.cache[key] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        self._save()
    
    def invalidate_directory(self, directory: str):
        """Invalidate all cache entries for a directory."""
        keys_to_remove = [
            key for key in self.cache.keys()
            if directory in key
        ]
        for key in keys_to_remove:
            del self.cache[key]
        if keys_to_remove:
            self._save()


# Global cache instances
_response_cache = None
_search_cache = None


def get_response_cache() -> ResponseCache:
    """Get global response cache instance."""
    global _response_cache
    if _response_cache is None:
        _response_cache = ResponseCache()
    return _response_cache


def get_search_cache() -> SearchCache:
    """Get global search cache instance."""
    global _search_cache
    if _search_cache is None:
        _search_cache = SearchCache()
    return _search_cache


def show_cache_stats():
    """Display cache statistics."""
    from rich.table import Table
    from rich.console import Console
    from rich.panel import Panel
    
    cache = get_response_cache()
    stats = cache.get_stats()
    
    console = Console()
    
    # Create stats table
    table = Table(title="Cache Statistics", border_style="cyan")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bright_white")
    
    table.add_row("Cache Hits", str(stats["hits"]))
    table.add_row("Cache Misses", str(stats["misses"]))
    table.add_row("Hit Rate", stats["hit_rate"])
    table.add_row("Cached Entries", str(stats["cache_size"]))
    table.add_row("Cache File Size", stats["cache_file_size"])
    
    console.print(table)
    
    # Show benefits
    if stats["hits"] > 0:
        console.print(f"\n[green]✓ Saved ~{stats['hits']} AI API calls[/green]")
        console.print(f"[green]✓ Instant responses for {stats['hits']} queries[/green]")
