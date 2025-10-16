"""Configuration management for Prometheus."""

import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG = {
    "timeout_seconds": 300,  # Default timeout (5 minutes)
    "short_timeout": 30,     # For quick commands
    "long_timeout": 1800,    # For long operations (30 minutes)
    "default_model": "llama3",
    "auto_confirm_safe": False,
    "history_size": 100,
    "color_scheme": "default",
    "dry_run": False,
    "log_level": "INFO",
    "ollama_host": "http://localhost:11434",
    "use_gemini": True,
    "gemini_model": "gemini-2.0-flash-exp"
}

class Config:
    """Configuration manager for Prometheus."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".prometheus"
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**DEFAULT_CONFIG, **loaded}
            except Exception as e:
                print(f"Warning: Could not load config: {e}. Using defaults.")
                return DEFAULT_CONFIG.copy()
        else:
            return DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save current configuration to file."""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self.config[key] = value
    
    def reset(self):
        """Reset configuration to defaults."""
        self.config = DEFAULT_CONFIG.copy()
        self.save()
    
    def display(self) -> str:
        """Return formatted configuration string."""
        lines = ["Current Configuration:"]
        for key, value in sorted(self.config.items()):
            lines.append(f"  {key}: {value}")
        return "\n".join(lines)

# Global config instance
_config = None

def get_config() -> Config:
    """Get global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
