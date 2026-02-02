#!/usr/bin/env python3
"""
Script to consolidate student domain model files into a single models.py
"""

import os
from pathlib import Path

# Source directory
models_dir = Path("app/domains/student/models")

# Model files to consolidate (in logical order)
model_files = [
    "student.py",  # Core student model
    "parent.py",  # Parent information
    "enrollment.py",  # Student enrollment
    "document.py",  # Document management
    "odc.py",  # ODC (On Duty Certificate) system
    "portal.py",  # Student portal
]

# Header for consolidated file
header = '''"""
Student Domain Models

All database models for the student domain including:
- Student core information
- Parent/guardian information
- Enrollment management
- Document management and verification
- ODC (On Duty Certificate) system
- Student portal functionality
"""

'''

# Collect all content
consolidated_content = header

for model_file in model_files:
    file_path = models_dir / model_file
    if not file_path.exists():
        print(f"Skipping {model_file} - not found")
        continue
    
    print(f"Processing {model_file}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add section separator
    section_name = model_file.replace('.py', '').replace('_', ' ').title()
    separator = f"\n\n# " + "=" * 70 + f"\n# {section_name}\n# " + "=" * 70 + "\n\n"
    
    consolidated_content += separator + content

# Write consolidated file
output_path = models_dir.parent / "models.py"
with open(output_path, 'w') as f:
    f.write(consolidated_content)

print(f"\n✅ Created consolidated models.py ({len(consolidated_content)} bytes)")
print(f"   Location: {output_path}")
