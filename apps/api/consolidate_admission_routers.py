#!/usr/bin/env python3
"""
Script to consolidate admission domain router files into a single router.py
"""

import os
from pathlib import Path

# Source directory
routers_dir = Path("app/domains/admission/routers")

# Router files to consolidate
router_files = [
    "application.py",
    "admin.py",
    "enhanced.py",
]

# Header for consolidated file
header = '''"""
Admission Domain Router

All API endpoints for the admission domain including:
- Application management
- Admin operations
- Enhanced admission features
"""

from fastapi import APIRouter

router = APIRouter()

'''

# Collect all content
consolidated_content = header

for router_file in router_files:
    file_path = routers_dir / router_file
    if not file_path.exists():
        print(f"Skipping {router_file} - not found")
        continue
    
    print(f"Processing {router_file}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove duplicate imports and router definitions
    lines = content.split('\n')
    filtered_lines = []
    skip_until_blank = False
    
    for line in lines:
        # Skip import blocks and router definitions at the top
        if line.startswith('from fastapi import') or line.startswith('from sqlmodel import') or line.startswith('from typing import'):
            continue
        if line.startswith('from app.'):
            continue
        if line.strip() == 'router = APIRouter()':
            continue
        if line.startswith('"""') and not filtered_lines:
            skip_until_blank = True
            continue
        if skip_until_blank:
            if line.strip() == '':
                skip_until_blank = False
            continue
        filtered_lines.append(line)
    
    # Add section separator
    section_name = router_file.replace('.py', '').replace('_', ' ').title()
    separator = f"\n\n# " + "=" * 70 + f"\n# {section_name} Endpoints\n# " + "=" * 70 + "\n\n"
    
    consolidated_content += separator + '\n'.join(filtered_lines)

# Write consolidated file
output_path = routers_dir.parent / "router.py"
with open(output_path, 'w') as f:
    f.write(consolidated_content)

print(f"\n✅ Created consolidated router.py ({len(consolidated_content)} bytes)")
print(f"   Location: {output_path}")
