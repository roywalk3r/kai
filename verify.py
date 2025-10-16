#!/usr/bin/env python3
"""
Verification script for Prometheus installation.
Checks that all components are properly installed and configured.
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (requires 3.8+)")
        return False

def check_ollama():
    """Check if Ollama is installed."""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ Ollama installed")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    print("✗ Ollama not found")
    return False

def check_llama3_model():
    """Check if llama3 model is available."""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=5)
        if 'llama3' in result.stdout:
            print("✓ llama3 model available")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    print("✗ llama3 model not found")
    return False

def check_dependencies():
    """Check if required Python packages are installed."""
    required = ['rich', 'prompt_toolkit', 'yaml']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"✗ {package} not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_project_structure():
    """Check if all required files and directories exist."""
    required_paths = [
        'ai/__init__.py',
        'ai/model.py',
        'ai/context.py',
        'core/__init__.py',
        'core/executor.py',
        'core/config.py',
        'core/history.py',
        'utils/__init__.py',
        'utils/safety.py',
        'utils/ui.py',
        'utils/suggestions.py',
        'main.py',
        'requirements.txt',
        'README.md',
    ]
    
    all_exist = True
    for path in required_paths:
        if Path(path).exists():
            print(f"✓ {path}")
        else:
            print(f"✗ {path} missing")
            all_exist = False
    
    return all_exist

def check_prometheus_directory():
    """Check if ~/.prometheus directory exists."""
    prometheus_dir = Path.home() / '.prometheus'
    if prometheus_dir.exists():
        print(f"✓ ~/.prometheus directory exists")
        return True
    else:
        print(f"ℹ ~/.prometheus directory will be created on first run")
        return True

def main():
    """Run all verification checks."""
    print("=" * 50)
    print("Prometheus Installation Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Ollama", check_ollama),
        ("llama3 Model", check_llama3_model),
        ("Python Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Prometheus Directory", check_prometheus_directory),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\nPrometheus is ready to use! Run: python main.py")
        return 0
    else:
        print(f"⚠️  {passed}/{total} checks passed")
        print("\nPlease fix the issues above before running Prometheus.")
        
        if not results[1]:  # Ollama check
            print("\nTo install Ollama:")
            print("  Visit: https://ollama.ai/")
            print("  Then run: ollama pull llama3")
        
        if not results[3]:  # Dependencies check
            print("\nTo install dependencies:")
            print("  pip install -r requirements.txt")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
