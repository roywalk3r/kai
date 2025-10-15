"""Tests for configuration module."""

import unittest
import tempfile
import shutil
from pathlib import Path
from core.config import Config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def setUp(self):
        """Create temporary config directory."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.config = Config()
        self.config.config_dir = self.temp_dir
        self.config.config_file = self.temp_dir / "config.json"
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)
    
    def test_default_config(self):
        """Test that default config is loaded."""
        for key, value in DEFAULT_CONFIG.items():
            self.assertEqual(self.config.get(key), value)
    
    def test_set_and_get(self):
        """Test setting and getting config values."""
        self.config.set("timeout_seconds", 30)
        self.assertEqual(self.config.get("timeout_seconds"), 30)
        
        self.config.set("dry_run", True)
        self.assertTrue(self.config.get("dry_run"))
    
    def test_save_and_load(self):
        """Test saving and loading config."""
        self.config.set("timeout_seconds", 30)
        self.config.set("dry_run", True)
        self.config.save()
        
        # Create new config instance to load from file
        new_config = Config()
        new_config.config_dir = self.temp_dir
        new_config.config_file = self.temp_dir / "config.json"
        new_config.config = new_config._load_config()
        
        self.assertEqual(new_config.get("timeout_seconds"), 30)
        self.assertTrue(new_config.get("dry_run"))
    
    def test_reset(self):
        """Test resetting config to defaults."""
        self.config.set("timeout_seconds", 30)
        self.config.reset()
        self.assertEqual(self.config.get("timeout_seconds"), DEFAULT_CONFIG["timeout_seconds"])

if __name__ == "__main__":
    unittest.main()
