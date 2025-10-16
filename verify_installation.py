#!/usr/bin/env python3
"""
Verification script for Prometheus installation.
Checks all new modules and dependencies.
"""

import sys
import importlib
from pathlib import Path

def test_import(module_name, package=None):
    """Test if a module can be imported."""
    try:
        if package:
            importlib.import_module(f"{package}.{module_name}")
        else:
            importlib.import_module(module_name)
        return True, "OK"
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run verification checks."""
    print("=" * 60)
    print("🔥 PROMETHEUS INSTALLATION VERIFICATION 🔥")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("📦 Checking Dependencies...")
    print("-" * 60)
    
    dependencies = [
        "rich",
        "prompt_toolkit",
        "pyqrcode",
        "pytz",
    ]
    
    all_deps_ok = True
    for dep in dependencies:
        success, msg = test_import(dep)
        status = "✅" if success else "❌"
        print(f"{status} {dep:20} {msg if not success else ''}")
        if not success:
            all_deps_ok = False
    
    print()
    
    # Check core modules
    print("🔧 Checking Core Modules...")
    print("-" * 60)
    
    core_modules = [
        ("model", "ai"),
        ("gemini_model", "ai"),
        ("context", "ai"),
        ("executor", "core"),
        ("history", "core"),
        ("config", "core"),
        ("plugins", "core"),
    ]
    
    all_core_ok = True
    for module, package in core_modules:
        success, msg = test_import(module, package)
        status = "✅" if success else "❌"
        print(f"{status} {package}.{module:20} {msg if not success else ''}")
        if not success:
            all_core_ok = False
    
    print()
    
    # Check new utility modules
    print("✨ Checking New Feature Modules...")
    print("-" * 60)
    
    new_modules = [
        ("quick_actions", "utils"),
        ("search", "utils"),
        ("keyboard", "utils"),
        ("smart_history", "utils"),
        ("context_commands", "utils"),
        ("safety", "utils"),
        ("ui", "utils"),
    ]
    
    all_new_ok = True
    for module, package in new_modules:
        success, msg = test_import(module, package)
        status = "✅" if success else "❌"
        marker = "🆕" if module in ["quick_actions", "search", "keyboard", "smart_history", "context_commands"] else "  "
        print(f"{status} {marker} {package}.{module:20} {msg if not success else ''}")
        if not success:
            all_new_ok = False
    
    print()
    
    # Check file structure
    print("📁 Checking File Structure...")
    print("-" * 60)
    
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "TERMINAL_FEATURES.md",
        "IMPLEMENTATION_SUMMARY.md",
        "ai/model.py",
        "core/executor.py",
        "core/plugins.py",
        "utils/quick_actions.py",
        "utils/search.py",
        "utils/keyboard.py",
        "utils/smart_history.py",
        "utils/context_commands.py",
    ]
    
    all_files_ok = True
    for file_path in required_files:
        path = Path(file_path)
        exists = path.exists()
        status = "✅" if exists else "❌"
        marker = "🆕" if "TERMINAL" in file_path or file_path in [
            "utils/quick_actions.py",
            "utils/search.py",
            "utils/keyboard.py",
            "utils/smart_history.py",
            "utils/context_commands.py",
            "core/plugins.py",
            "IMPLEMENTATION_SUMMARY.md"
        ] else "  "
        print(f"{status} {marker} {file_path}")
        if not exists:
            all_files_ok = False
    
    print()
    
    # Final summary
    print("=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    results = [
        ("Dependencies", all_deps_ok),
        ("Core Modules", all_core_ok),
        ("Feature Modules", all_new_ok),
        ("File Structure", all_files_ok),
    ]
    
    all_ok = all(result[1] for result in results)
    
    for name, ok in results:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{name:20} {status}")
    
    print()
    
    if all_ok:
        print("🎉 ALL CHECKS PASSED! 🎉")
        print()
        print("Prometheus is ready to use!")
        print()
        print("Quick start:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run system installer: sudo ./system-install.sh")
        print("  3. Start Prometheus: prom")
        print()
        print("For help:")
        print("  - Type 'help' in Prometheus")
        print("  - Read TERMINAL_FEATURES.md")
        print("  - Check NEW_FEATURES_DEMO.md")
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Check file paths")
        print("  3. Run verification again")
        return 1

if __name__ == "__main__":
    sys.exit(main())
