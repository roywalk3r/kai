#!/usr/bin/env python3
"""
Verify that all imported packages are in requirements.txt
"""

import os
import re
import sys
from pathlib import Path

# Standard library modules (don't need to be in requirements.txt)
STDLIB_MODULES = {
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'collections', 'copy',
    'datetime', 'enum', 'functools', 'glob', 'hashlib', 'io', 'itertools',
    'json', 'logging', 'math', 'os', 'pathlib', 'platform', 're', 'shutil',
    'signal', 'socket', 'string', 'subprocess', 'sys', 'tempfile', 'threading',
    'time', 'typing', 'unittest', 'urllib', 'uuid', 'warnings', 'weakref',
    'setuptools', 'distutils', 'pkg_resources'  # Usually included with Python
}

# Package name mappings (import name -> package name)
PACKAGE_MAPPINGS = {
    'google': 'google-genai',
    'yaml': 'pyyaml',
    'prompt_toolkit': 'prompt-toolkit',
}


def get_imports_from_file(filepath):
    """Extract all imports from a Python file."""
    imports = set()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all import statements
        import_pattern = r'^(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(import_pattern, content, re.MULTILINE)
        
        for match in matches:
            # Skip relative imports and local modules
            if match not in ['ai', 'core', 'utils', 'tests']:
                imports.add(match)
                
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}")
        
    return imports


def get_all_imports(root_dir):
    """Get all imports from all Python files."""
    all_imports = set()
    
    for py_file in Path(root_dir).rglob('*.py'):
        # Skip virtual environment and build directories
        if any(skip in str(py_file) for skip in ['.venv', 'venv', 'build', 'dist', '__pycache__']):
            continue
            
        imports = get_imports_from_file(py_file)
        all_imports.update(imports)
        
    return all_imports


def get_requirements(req_file):
    """Parse requirements.txt and get package names."""
    packages = set()
    
    if not os.path.exists(req_file):
        return packages
        
    with open(req_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            # Extract package name (before >= or ==)
            package = re.split(r'[><=!]', line)[0].strip()
            packages.add(package.lower())
            
    return packages


def main():
    """Main verification function."""
    script_dir = Path(__file__).parent
    
    print("🔍 Verifying requirements.txt...")
    print()
    
    # Get all imports
    all_imports = get_all_imports(script_dir)
    
    # Filter out standard library
    third_party = {imp for imp in all_imports if imp not in STDLIB_MODULES}
    
    # Map to package names
    required_packages = set()
    for imp in third_party:
        package = PACKAGE_MAPPINGS.get(imp, imp)
        required_packages.add(package.lower())
    
    # Get current requirements
    req_file = script_dir / 'requirements.txt'
    current_packages = get_requirements(req_file)
    
    # Check for missing packages
    missing = required_packages - current_packages
    
    # Check for unused packages (might be false positives)
    unused = current_packages - required_packages
    
    # Report results
    print(f"📦 Found {len(third_party)} third-party imports:")
    for imp in sorted(third_party):
        package = PACKAGE_MAPPINGS.get(imp, imp)
        print(f"  • {imp} → {package}")
    
    print()
    print(f"📋 Current requirements.txt has {len(current_packages)} packages:")
    for pkg in sorted(current_packages):
        print(f"  • {pkg}")
    
    print()
    
    if missing:
        print("❌ MISSING from requirements.txt:")
        for pkg in sorted(missing):
            print(f"  • {pkg}")
        print()
        print("Add these to requirements.txt!")
        return 1
    else:
        print("✅ All imports are in requirements.txt!")
    
    if unused:
        print()
        print("ℹ️  Packages in requirements.txt not directly imported:")
        print("   (These might be dependencies or used dynamically)")
        for pkg in sorted(unused):
            print(f"  • {pkg}")
    
    print()
    print("✨ Verification complete!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
