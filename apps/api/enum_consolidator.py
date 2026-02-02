#!/usr/bin/env python3
"""
Enum Consolidation Script

Scans all Python files for enum definitions and creates a consolidated
app/shared/enums.py file with all enums organized by domain.
"""

import re
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict


class EnumExtractor:
    def __init__(self, base_path: str = "app"):
        self.base_path = Path(base_path)
        self.enums = defaultdict(list)  # domain -> list of enum definitions
        self.files_with_enums = []
        
    def extract_enums_from_file(self, file_path: Path) -> List[Dict]:
        """Extract all enum definitions from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []
        
        enums = []
        
        # Pattern to match enum class definitions
        # Matches: class EnumName(str, Enum): or class EnumName(Enum):
        enum_pattern = r'class\s+(\w+)\s*\([^)]*Enum[^)]*\):\s*\n((?:\s+\w+\s*=\s*[^\n]+\n)+)'
        
        for match in re.finditer(enum_pattern, content):
            enum_name = match.group(1)
            enum_body = match.group(2)
            
            # Extract enum values
            values = []
            value_pattern = r'\s+(\w+)\s*=\s*([^\n]+)'
            for value_match in re.finditer(value_pattern, enum_body):
                field_name = value_match.group(1)
                field_value = value_match.group(2).strip()
                values.append((field_name, field_value))
            
            if values:
                enums.append({
                    'name': enum_name,
                    'values': values,
                    'file': str(file_path.relative_to(self.base_path))
                })
        
        return enums
    
    def categorize_enum(self, enum_name: str, file_path: str) -> str:
        """Categorize enum by domain based on name and file path."""
        name_lower = enum_name.lower()
        path_lower = file_path.lower()
        
        # Domain-specific patterns
        if any(x in name_lower for x in ['student', 'parent', 'enrollment', 'document', 'odc', 'portal']):
            return 'student'
        elif any(x in name_lower for x in ['admission', 'application', 'scholarship', 'merit']):
            return 'admission'
        elif any(x in name_lower for x in ['batch', 'section', 'subject', 'exam', 'attendance', 'timetable', 'academic', 'regulation', 'lesson']):
            return 'academic'
        elif any(x in name_lower for x in ['fee', 'payment', 'gateway', 'transaction', 'easebuzz']):
            return 'finance'
        elif any(x in name_lower for x in ['faculty', 'staff', 'designation']):
            return 'hr'
        elif any(x in name_lower for x in ['hostel', 'library', 'inventory', 'transport', 'asset', 'facility']):
            return 'campus'
        elif any(x in name_lower for x in ['notification', 'sms', 'email', 'communication']):
            return 'communication'
        elif any(x in name_lower for x in ['user', 'role', 'permission', 'audit', 'file', 'import', 'system', 'setting']):
            return 'system'
        
        # Check file path
        if 'student' in path_lower:
            return 'student'
        elif 'admission' in path_lower:
            return 'admission'
        elif 'academic' in path_lower:
            return 'academic'
        elif 'finance' in path_lower:
            return 'finance'
        elif 'hr' in path_lower:
            return 'hr'
        elif 'campus' in path_lower or 'hostel' in path_lower or 'library' in path_lower:
            return 'campus'
        elif 'communication' in path_lower:
            return 'communication'
        elif 'system' in path_lower:
            return 'system'
        
        # Generic enums (Gender, BloodGroup, etc.)
        if any(x in name_lower for x in ['gender', 'blood', 'status', 'type', 'mode']):
            return 'generic'
        
        return 'other'
    
    def scan_all_files(self):
        """Scan all Python files for enums."""
        files_to_scan = [
            'domains/academic/models/attendance.py',
            'domains/academic/models/exam.py',
            'domains/academic/models/hall_ticket.py',
            'domains/academic/models/internal_exam.py',
            'domains/academic/models/timetable.py',
            'domains/academic/models/university_exam.py',
            'domains/admission/models.py',
            'domains/campus/hostel/models/infrastructure.py',
            'domains/campus/hostel/models/operations.py',
            'domains/campus/inventory/models/asset.py',
            'domains/campus/library/models/circulation.py',
            'domains/campus/library/models/resource.py',
            'domains/communication/models/communication.py',
            'domains/finance/models/fee.py',
            'domains/finance/models/gateway.py',
            'domains/student/models/document.py',
            'domains/student/models/odc.py',
            'domains/student/models/portal.py',
            'domains/system/models/files.py',
            'domains/system/models/system.py',
            'domains/system/schemas/imports.py',
            'domains/system/schemas/system.py',
            'models/enums.py',
            'models/lesson.py',
            'models/operations.py',
            'models/program.py',
            'schemas/import_schema.py',
        ]
        
        for file_rel in files_to_scan:
            file_path = self.base_path / file_rel
            if not file_path.exists():
                continue
            
            enums = self.extract_enums_from_file(file_path)
            if enums:
                self.files_with_enums.append(file_rel)
                for enum in enums:
                    domain = self.categorize_enum(enum['name'], file_rel)
                    self.enums[domain].append(enum)
    
    def generate_consolidated_file(self, output_path: str = 'app/shared/enums.py'):
        """Generate consolidated enums.py file."""
        # Create shared directory if it doesn't exist
        shared_dir = Path('app/shared')
        shared_dir.mkdir(exist_ok=True)
        
        # Create __init__.py
        (shared_dir / '__init__.py').write_text('')
        
        lines = []
        lines.append('"""')
        lines.append('Consolidated Enums')
        lines.append('')
        lines.append('Single source of truth for all enum definitions across the ERP system.')
        lines.append('Organized by domain for clarity.')
        lines.append('"""')
        lines.append('')
        lines.append('from enum import Enum')
        lines.append('')
        lines.append('')
        
        # Domain order
        domain_order = [
            'generic',
            'system',
            'hr',
            'academic',
            'student',
            'admission',
            'finance',
            'communication',
            'campus',
            'other'
        ]
        
        domain_titles = {
            'generic': 'Generic Enums',
            'system': 'System Domain',
            'hr': 'HR Domain',
            'academic': 'Academic Domain',
            'student': 'Student Domain',
            'admission': 'Admission Domain',
            'finance': 'Finance Domain',
            'communication': 'Communication Domain',
            'campus': 'Campus Domain',
            'other': 'Other / Uncategorized'
        }
        
        # Track seen enums to avoid duplicates
        seen_enums = set()
        
        for domain in domain_order:
            if domain not in self.enums:
                continue
            
            lines.append(f'# {"-" * 70}')
            lines.append(f'# {domain_titles[domain]}')
            lines.append(f'# {"-" * 70}')
            lines.append('')
            
            for enum in self.enums[domain]:
                enum_name = enum['name']
                
                # Skip duplicates
                if enum_name in seen_enums:
                    print(f"⚠️  Skipping duplicate: {enum_name} (from {enum['file']})")
                    continue
                
                seen_enums.add(enum_name)
                
                # Write enum class
                lines.append(f'class {enum_name}(str, Enum):')
                for field_name, field_value in enum['values']:
                    lines.append(f'    {field_name} = {field_value}')
                lines.append('')
                lines.append('')
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Generated: {output_path}")
        print(f"   Total enums: {len(seen_enums)}")
        print(f"   Domains: {len([d for d in domain_order if d in self.enums])}")
    
    def generate_report(self, output_path: str = 'docs/enum_consolidation_report.md'):
        """Generate report of all enums found."""
        lines = []
        lines.append('# Enum Consolidation Report')
        lines.append('')
        lines.append(f'**Total files with enums:** {len(self.files_with_enums)}')
        lines.append('')
        
        # Count enums by domain
        total_enums = sum(len(enums) for enums in self.enums.values())
        lines.append(f'**Total enum definitions found:** {total_enums}')
        lines.append('')
        
        lines.append('## Enums by Domain')
        lines.append('')
        for domain in sorted(self.enums.keys()):
            lines.append(f'### {domain.title()} ({len(self.enums[domain])} enums)')
            lines.append('')
            for enum in self.enums[domain]:
                lines.append(f'- **{enum["name"]}** ({len(enum["values"])} values) - `{enum["file"]}`')
            lines.append('')
        
        lines.append('## Files with Enums')
        lines.append('')
        for file in sorted(self.files_with_enums):
            lines.append(f'- `{file}`')
        lines.append('')
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Generated: {output_path}")


def main():
    print("🔍 Scanning for enum definitions...\n")
    
    extractor = EnumExtractor()
    extractor.scan_all_files()
    
    print(f"\n📊 Found {len(extractor.files_with_enums)} files with enums\n")
    
    # Generate consolidated file
    extractor.generate_consolidated_file()
    
    # Generate report
    extractor.generate_report()
    
    print("\n✅ Enum consolidation complete!")
    print("\nNext steps:")
    print("1. Review app/shared/enums.py")
    print("2. Update imports across codebase")
    print("3. Delete old enum definitions")


if __name__ == '__main__':
    main()
