#!/usr/bin/env python3
"""
Update Enum Imports

Updates all files to import enums from app.shared.enums instead of local definitions.
"""

import re
from pathlib import Path
from typing import List, Set


# All enum names from consolidated file
ENUM_NAMES = [
    'Gender', 'BloodGroup', 'RoomType', 'TopicStatus', 'QuestionType',
    'TicketStatus', 'ProgramType', 'ProgramStatus', 'SettingGroup',
    'AuditLogAction', 'ImportRowStatus', 'AttendanceStatus', 'SessionStatus',
    'ExamType', 'ExamStatus', 'DayOfWeek', 'SlotType', 'AdjustmentStatus',
    'AcademicYearStatus', 'SubjectType', 'GenderPreference', 'ODCStatus',
    'PayoutStatus', 'BillingStatus', 'StudentStatus', 'ApplicationPaymentStatus',
    'ApplicationStatus', 'ScholarshipCategory', 'FeeCategory', 'PaymentMode',
    'PaymentStatus', 'PaymentMethod', 'CircularTarget', 'NotificationType',
    'NotificationChannel', 'HostelType', 'GatePassType', 'GatePassStatus',
    'ComplaintStatus', 'AssetCategory', 'AllocationStatus', 'UniformSize',
    'IssueStatus', 'BookStatus', 'MemberType', 'CreatedFrom', 'DifficultyLevel',
    'TicketPriority'
]


class ImportUpdater:
    def __init__(self, base_path: str = "app"):
        self.base_path = Path(base_path)
        self.updated_files = []
        self.enum_names_set = set(ENUM_NAMES)
    
    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped."""
        path_str = str(file_path)
        
        # Skip the consolidated enums file itself
        if 'shared/enums.py' in path_str:
            return True
        
        # Skip __pycache__
        if '__pycache__' in path_str:
            return True
        
        # Skip alembic versions
        if 'alembic/versions' in path_str:
            return True
        
        return False
    
    def find_enum_usage(self, content: str) -> Set[str]:
        """Find which enums from our list are used in the file."""
        used_enums = set()
        
        for enum_name in ENUM_NAMES:
            # Check if enum is used (not just defined)
            # Look for: EnumName.VALUE or : EnumName or = EnumName or (EnumName)
            patterns = [
                rf'\b{enum_name}\.',  # EnumName.VALUE
                rf':\s*{enum_name}\b',  # : EnumName
                rf'=\s*{enum_name}\b',  # = EnumName
                rf'\({enum_name}\)',  # (EnumName)
                rf'\[{enum_name}\]',  # [EnumName]
            ]
            
            for pattern in patterns:
                if re.search(pattern, content):
                    used_enums.add(enum_name)
                    break
        
        return used_enums
    
    def update_imports(self, file_path: Path) -> bool:
        """Update imports in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except:
            return False
        
        content = original_content
        
        # Find which enums are used in this file
        used_enums = self.find_enum_usage(content)
        
        if not used_enums:
            return False
        
        # Remove old enum class definitions
        for enum_name in used_enums:
            # Remove class definition
            pattern = rf'class\s+{enum_name}\s*\([^)]*Enum[^)]*\):\s*\n(?:\s+\w+\s*=\s*[^\n]+\n)+'
            content = re.sub(pattern, '', content)
        
        # Remove old enum imports
        # Pattern: from app.models.enums import Gender, BloodGroup
        # Pattern: from app.domains.*.models import ExamType
        old_import_patterns = [
            r'from\s+app\.models\.enums\s+import\s+[^\n]+\n',
            r'from\s+app\.domains\.[^.]+\.models\s+import\s+[^\n]+\n',
            r'from\s+\.models\s+import\s+[^\n]+\n',
            r'from\s+\.\.models\s+import\s+[^\n]+\n',
        ]
        
        for pattern in old_import_patterns:
            # Only remove if it imports one of our enums
            matches = re.finditer(pattern, content)
            for match in matches:
                import_line = match.group(0)
                # Check if any of our enums are in this import
                if any(enum in import_line for enum in used_enums):
                    content = content.replace(import_line, '')
        
        # Add new import at the top (after other imports)
        enum_list = ', '.join(sorted(used_enums))
        new_import = f'from app.shared.enums import {enum_list}\n'
        
        # Find the last import statement
        import_pattern = r'^(?:from|import)\s+.+$'
        import_matches = list(re.finditer(import_pattern, content, re.MULTILINE))
        
        if import_matches:
            # Insert after last import
            last_import = import_matches[-1]
            insert_pos = last_import.end()
            content = content[:insert_pos] + '\n' + new_import + content[insert_pos:]
        else:
            # No imports found, add at top after docstring
            # Find docstring
            docstring_pattern = r'^"""[\s\S]*?"""\s*\n'
            docstring_match = re.search(docstring_pattern, content)
            if docstring_match:
                insert_pos = docstring_match.end()
            else:
                insert_pos = 0
            content = content[:insert_pos] + new_import + '\n' + content[insert_pos:]
        
        # Clean up multiple blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def update_all_files(self):
        """Update all Python files in the codebase."""
        for file_path in self.base_path.rglob('*.py'):
            if self.should_skip_file(file_path):
                continue
            
            if self.update_imports(file_path):
                rel_path = file_path.relative_to(self.base_path)
                self.updated_files.append(str(rel_path))
                print(f"✅ Updated: {rel_path}")
    
    def generate_report(self):
        """Generate report of updated files."""
        print(f"\n📊 Summary:")
        print(f"   Files updated: {len(self.updated_files)}")
        
        if self.updated_files:
            print(f"\n✅ Updated files:")
            for file in sorted(self.updated_files):
                print(f"   - {file}")


def main():
    print("🔄 Updating enum imports across codebase...\n")
    
    updater = ImportUpdater()
    updater.update_all_files()
    updater.generate_report()
    
    print("\n✅ Import update complete!")
    print("\nNext steps:")
    print("1. Test the application")
    print("2. Delete old enum definition files")


if __name__ == '__main__':
    main()
