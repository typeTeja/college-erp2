#!/usr/bin/env python3
"""
Script to consolidate finance domain service files into a single services.py
"""

from pathlib import Path

# Source directory
services_dir = Path("app/domains/finance/services")

# Service files to consolidate
service_files = [
    "fee.py",
    "gateway.py",
    "easebuzz.py",
]

# Header for consolidated file
header = '''"""
Finance Domain Services

Business logic for finance domain including:
- Fee management
- Payment gateway integration
- Easebuzz payment processing
"""

'''

# Collect all content
consolidated_content = header

for service_file in service_files:
    file_path = services_dir / service_file
    if not file_path.exists():
        print(f"Skipping {service_file} - not found")
        continue
    
    print(f"Processing {service_file}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add section separator
    section_name = service_file.replace('.py', '').replace('_', ' ').title()
    separator = f"\n\n# " + "=" * 70 + f"\n# {section_name}\n# " + "=" * 70 + "\n\n"
    
    consolidated_content += separator + content

# Write consolidated file
output_path = services_dir.parent / "services.py"
with open(output_path, 'w') as f:
    f.write(consolidated_content)

print(f"\n✅ Created consolidated services.py ({len(consolidated_content)} bytes)")
print(f"   Location: {output_path}")
