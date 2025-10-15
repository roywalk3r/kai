"""Tests for safety module."""

import unittest
from utils.safety import (
    check_command_safety, validate_command, is_interactive_command,
    sanitize_command, SafetyLevel
)

class TestSafety(unittest.TestCase):
    """Test safety checks."""
    
    def test_safe_commands(self):
        """Test that safe commands are identified correctly."""
        safe_commands = ["ls -la", "pwd", "echo hello", "cat file.txt"]
        for cmd in safe_commands:
            level, _ = check_command_safety(cmd)
            self.assertEqual(level, SafetyLevel.SAFE)
    
    def test_dangerous_commands(self):
        """Test that dangerous commands are identified."""
        dangerous = ["rm -rf /", "dd if=/dev/zero", "mkfs.ext4 /dev/sda"]
        for cmd in dangerous:
            level, warning = check_command_safety(cmd)
            self.assertEqual(level, SafetyLevel.DANGEROUS)
            self.assertIsNotNone(warning)
    
    def test_long_running_commands(self):
        """Test that long-running commands are identified."""
        long_running = ["ping google.com", "find / -name test", "sleep 100"]
        for cmd in long_running:
            level, warning = check_command_safety(cmd)
            self.assertEqual(level, SafetyLevel.LONG_RUNNING)
            self.assertIsNotNone(warning)
    
    def test_interactive_commands(self):
        """Test that interactive commands are identified."""
        interactive = ["nano file.txt", "vim test.py", "top", "htop"]
        for cmd in interactive:
            self.assertTrue(is_interactive_command(cmd))
        
        non_interactive = ["cat file.txt", "ls -la", "grep test"]
        for cmd in non_interactive:
            self.assertFalse(is_interactive_command(cmd))
    
    def test_command_validation(self):
        """Test command validation."""
        # Valid commands
        valid = ["ls -la", "echo 'hello world'", "cat file.txt"]
        for cmd in valid:
            is_valid, error = validate_command(cmd)
            self.assertTrue(is_valid, f"Command should be valid: {cmd}")
            self.assertIsNone(error)
        
        # Invalid commands
        invalid = [
            ("echo 'unmatched", "Unmatched single quote"),
            ('echo "unmatched', "Unmatched double quote"),
            ("echo (test", "Unmatched parentheses"),
        ]
        for cmd, expected_error in invalid:
            is_valid, error = validate_command(cmd)
            self.assertFalse(is_valid)
            self.assertIn(expected_error.lower(), error.lower())
    
    def test_sanitize_command(self):
        """Test command sanitization."""
        self.assertEqual(sanitize_command("  ls -la  "), "ls -la")
        self.assertEqual(sanitize_command("ls    -la"), "ls -la")
        self.assertEqual(sanitize_command("\nls\n"), "ls")

if __name__ == "__main__":
    unittest.main()
