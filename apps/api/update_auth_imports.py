#!/usr/bin/env python3
"""
Script to update all imports from legacy app.models to auth domain
"""

import os
import re
from pathlib import Path

# Base directory
base_dir = Path("app")

# Import replacements
replacements = [
    # User imports
    (r"from app\.models\.user import User", "from app.models import User"),
    (r"from app\.models\.user import .*", "from app.models import User"),
    
    # Role imports
    (r"from app\.models\.role import Role", "from app.models import Role"),
    (r"from app\.models\.role import .*", "from app.models import Role"),
    
    # Permission imports
    (r"from app\.models\.permission import Permission", "from app.models import Permission"),
    (r"from app\.models\.permission import .*", "from app.models import Permission"),
    
    # UserRole imports
    (r"from app\.models\.user_role import UserRole", "from app.models import UserRole"),
    
    # RolePermission imports
    (r"from app\.models\.role_permission import RolePermission", "from app.models import RolePermission"),
]

def update_file(file_path: Path) -> bool:
    """Update imports in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all replacements
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Only write if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    updated_files = []
    
    # Find all Python files
    for py_file in base_dir.rglob("*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        if update_file(py_file):
            updated_files.append(py_file)
    
    print(f"\n✅ Updated {len(updated_files)} files:")
    for file in updated_files:
        print(f"   - {file}")
    
    if not updated_files:
        print("\n✅ No files needed updating")

if __name__ == "__main__":
    main()
