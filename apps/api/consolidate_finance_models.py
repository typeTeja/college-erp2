#!/usr/bin/env python3
"""
Script to consolidate finance domain model files into a single models.py
"""

from pathlib import Path

# Source directory
models_dir = Path("app/domains/finance/models")

# Model files to consolidate
model_files = [
    "config.py",  # Fee configuration
    "fee.py",  # Fee management
    "gateway.py",  # Payment gateway
]

# Header for consolidated file
header = '''"""
Finance Domain Models

All database models for the finance domain including:
- Fee configuration and management
- Payment gateway integration
- Online payment tracking
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
