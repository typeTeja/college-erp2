#!/usr/bin/env python3
"""
Script to consolidate academic domain model files into a single models.py
"""

import os
from pathlib import Path

# Source directory
models_dir = Path("app/domains/academic/models")

# Model files to consolidate (in logical order)
model_files = [
    "setup.py",  # Foundation: AcademicYear, Section, etc.
    "regulation.py",  # Regulation system
    "batch.py",  # Academic batches
    "assignment.py",  # Student assignments
    "allocation.py",  # Allocations
    "student_history.py",  # Student history tracking
    "attendance.py",  # Attendance
    "timetable.py",  # Timetable
    "exam.py",  # General exams
    "internal_exam.py",  # Internal exams
    "university_exam.py",  # University exams
    "hall_ticket.py",  # Hall tickets
    "entrance_exam.py",  # Entrance exams (if exists)
]

# Header for consolidated file
header = '''"""
Academic Domain Models

All database models for the academic domain including:
- Academic setup (years, sections, practical batches)
- Regulations and program structure
- Academic batches and semesters
- Student assignments and allocations
- Attendance tracking
- Timetable management
- Exam management (internal, university, hall tickets)
- Student academic history
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
