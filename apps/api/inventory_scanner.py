#!/usr/bin/env python3
"""
Domain Migration Inventory Scanner

Scans apps/api/app/ directory and generates inventory of all Python files
with categorization, domain assignment, and migration actions.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import csv


class InventoryScanner:
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Get script directory and construct path to app/
            script_dir = Path(__file__).parent
            self.base_path = script_dir / "app"
        else:
            self.base_path = Path(base_path)
        
        print(f"📁 Scanning directory: {self.base_path.absolute()}\n")
        
        self.inventory = []
        
        # Domain mapping patterns
        self.domain_patterns = {
            'student': [
                r'student', r'parent', r'enrollment', r'portal', 
                r'document(?!ation)', r'odc'
            ],
            'admission': [
                r'admission', r'application', r'scholarship', r'merit', r'entrance'
            ],
            'academic': [
                r'batch', r'section', r'subject', r'exam', r'attendance',
                r'timetable', r'regulation', r'hall_ticket', r'internal_exam',
                r'university_exam', r'assignment', r'allocation', r'lesson'
            ],
            'finance': [
                r'fee', r'payment', r'easebuzz', r'gateway', r'transaction'
            ],
            'hr': [
                r'faculty', r'staff', r'designation', r'employee'
            ],
            'campus': [
                r'hostel', r'library', r'inventory', r'transport',
                r'infrastructure', r'facility', r'logistics', r'asset',
                r'resource', r'circulation', r'maintenance'
            ],
            'communication': [
                r'circular', r'notification', r'sms', r'email', r'communication'
            ],
            'system': [
                r'user(?!_role)', r'role', r'permission', r'settings?',
                r'audit', r'import', r'file', r'institute'
            ]
        }
    
    def scan_directory(self) -> List[Dict]:
        """Recursively scan directory for Python files."""
        for root, dirs, files in os.walk(self.base_path):
            # Skip __pycache__ and alembic versions
            dirs[:] = [d for d in dirs if d != '__pycache__']
            if 'alembic/versions' in root:
                continue
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    self.analyze_file(file_path)
        
        return self.inventory
    
    def categorize_layer(self, file_path: Path) -> str:
        """Determine current layer (legacy/domain/core)."""
        rel_path = str(file_path.relative_to(self.base_path))
        
        if rel_path.startswith('domains/'):
            return 'domain'
        elif any(rel_path.startswith(p) for p in ['models/', 'schemas/', 'services/', 'api/v1/']):
            return 'legacy'
        elif any(rel_path.startswith(p) for p in ['core/', 'config/', 'utils/', 'db/', 'middleware/']):
            return 'core'
        else:
            return 'mixed'
    
    def assign_domain(self, file_path: Path) -> str:
        """Assign target domain based on file name and path."""
        rel_path = str(file_path.relative_to(self.base_path))
        file_name = file_path.stem.lower()
        
        # Already in domain
        if rel_path.startswith('domains/'):
            domain_match = re.match(r'domains/([^/]+)/', rel_path)
            if domain_match:
                return domain_match.group(1)
        
        # Core infrastructure
        if any(rel_path.startswith(p) for p in ['core/', 'config/', 'db/', 'middleware/']):
            return 'core'
        
        # Match against domain patterns
        for domain, patterns in self.domain_patterns.items():
            for pattern in patterns:
                if re.search(pattern, file_name, re.IGNORECASE):
                    return domain
        
        # Special cases
        if 'main.py' in file_name or 'routers.py' in file_name:
            return 'core'
        
        return 'unknown'
    
    def determine_action(self, file_path: Path, layer: str, domain: str) -> str:
        """Determine required action (MOVE/MERGE/DELETE/KEEP)."""
        file_name = file_path.name
        
        # __init__.py files - keep or update
        if file_name == '__init__.py':
            return 'KEEP'
        
        # Core infrastructure - keep
        if layer == 'core' or domain == 'core':
            return 'KEEP'
        
        # Already in correct domain location
        if layer == 'domain':
            rel_path = str(file_path.relative_to(self.base_path))
            # Check if it's in a subdirectory that should be consolidated
            if '/models/' in rel_path or '/schemas/' in rel_path or '/services/' in rel_path or '/routers/' in rel_path:
                return 'MERGE'
            return 'KEEP'
        
        # Check if file is empty/stub
        try:
            size = file_path.stat().st_size
            if size < 200:  # Less than 200 bytes likely stub
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Check if mostly imports/comments
                    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
                    if len(lines) < 5:
                        return 'DELETE'
        except:
            pass
        
        # Legacy files need to move
        if layer == 'legacy':
            # Check if domain version already exists
            if domain != 'unknown':
                domain_path = self.base_path / 'domains' / domain
                if domain_path.exists():
                    # Might need merge
                    return 'MERGE'
                else:
                    return 'MOVE'
            return 'MOVE'
        
        return 'REVIEW'
    
    def get_file_stats(self, file_path: Path) -> Tuple[int, int]:
        """Get file size and import count."""
        try:
            size = file_path.stat().st_size
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                import_count = len(re.findall(r'^\s*(?:from|import)\s+', content, re.MULTILINE))
            return size, import_count
        except:
            return 0, 0
    
    def analyze_file(self, file_path: Path):
        """Analyze a single file and add to inventory."""
        rel_path = str(file_path.relative_to(self.base_path))
        layer = self.categorize_layer(file_path)
        domain = self.assign_domain(file_path)
        action = self.determine_action(file_path, layer, domain)
        size, imports = self.get_file_stats(file_path)
        
        self.inventory.append({
            'file_path': rel_path,
            'layer': layer,
            'domain': domain,
            'action': action,
            'size': size,
            'imports': imports,
            'notes': self.get_notes(file_path, layer, domain, action)
        })
    
    def get_notes(self, file_path: Path, layer: str, domain: str, action: str) -> str:
        """Generate notes for file."""
        notes = []
        
        if domain == 'unknown':
            notes.append('Domain assignment unclear')
        
        if action == 'MERGE':
            notes.append('May conflict with existing domain file')
        
        if action == 'REVIEW':
            notes.append('Requires manual review')
        
        size, imports = self.get_file_stats(file_path)
        if size > 10000:
            notes.append('Large file (>10KB)')
        if imports > 20:
            notes.append('High coupling (>20 imports)')
        
        return '; '.join(notes) if notes else ''
    
    def generate_csv(self, output_path: str = 'docs/migration_inventory.csv'):
        """Generate CSV report."""
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'file_path', 'layer', 'domain', 'action', 'size', 'imports', 'notes'
            ])
            writer.writeheader()
            writer.writerows(self.inventory)
        
        print(f"✅ CSV report generated: {output_path}")
    
    def generate_markdown(self, output_path: str = 'docs/migration_inventory.md'):
        """Generate Markdown report."""
        # Calculate statistics
        total_files = len(self.inventory)
        by_layer = {}
        by_domain = {}
        by_action = {}
        
        for item in self.inventory:
            by_layer[item['layer']] = by_layer.get(item['layer'], 0) + 1
            by_domain[item['domain']] = by_domain.get(item['domain'], 0) + 1
            by_action[item['action']] = by_action.get(item['action'], 0) + 1
        
        # Generate markdown
        with open(output_path, 'w') as f:
            f.write("# Domain Migration Inventory\n\n")
            f.write(f"**Generated:** {Path.cwd()}\n\n")
            f.write("---\n\n")
            
            # Summary
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Total Files:** {total_files}\n")
            f.write(f"- **Legacy Files:** {by_layer.get('legacy', 0)}\n")
            f.write(f"- **Domain Files:** {by_layer.get('domain', 0)}\n")
            f.write(f"- **Core Files:** {by_layer.get('core', 0)}\n\n")
            
            # By action
            f.write("### Files by Action\n\n")
            for action in sorted(by_action.keys()):
                f.write(f"- **{action}:** {by_action[action]} files\n")
            f.write("\n")
            
            # By domain
            f.write("### Files by Domain\n\n")
            for domain in sorted(by_domain.keys()):
                f.write(f"- **{domain}:** {by_domain[domain]} files\n")
            f.write("\n---\n\n")
            
            # High-risk files
            f.write("## High-Risk Files (Require Manual Review)\n\n")
            high_risk = [item for item in self.inventory if 
                        item['action'] in ['MERGE', 'REVIEW'] or 
                        item['size'] > 10000 or 
                        item['imports'] > 20]
            
            if high_risk:
                f.write("| File | Layer | Domain | Action | Notes |\n")
                f.write("|------|-------|--------|--------|-------|\n")
                for item in high_risk:
                    f.write(f"| {item['file_path']} | {item['layer']} | {item['domain']} | {item['action']} | {item['notes']} |\n")
            else:
                f.write("*No high-risk files identified.*\n")
            
            f.write("\n---\n\n")
            
            # Files to delete
            f.write("## Files Marked for Deletion\n\n")
            to_delete = [item for item in self.inventory if item['action'] == 'DELETE']
            if to_delete:
                for item in to_delete:
                    f.write(f"- `{item['file_path']}` - {item['notes']}\n")
            else:
                f.write("*No files marked for deletion.*\n")
            
            f.write("\n---\n\n")
            
            # Complete inventory
            f.write("## Complete Inventory\n\n")
            f.write("| File Path | Layer | Domain | Action |\n")
            f.write("|-----------|-------|--------|--------|\n")
            for item in sorted(self.inventory, key=lambda x: (x['domain'], x['file_path'])):
                f.write(f"| {item['file_path']} | {item['layer']} | {item['domain']} | {item['action']} |\n")
        
        print(f"✅ Markdown report generated: {output_path}")


def main():
    print("🔍 Starting domain migration inventory scan...\n")
    
    scanner = InventoryScanner()
    inventory = scanner.scan_directory()
    
    print(f"\n📊 Scanned {len(inventory)} files\n")
    
    # Generate reports
    scanner.generate_csv()
    scanner.generate_markdown()
    
    print("\n✅ Inventory complete!")
    print("\nNext steps:")
    print("1. Review docs/migration_inventory.md")
    print("2. Verify high-risk files")
    print("3. Proceed to Step 1.5 (Dependency Graph)")


if __name__ == '__main__':
    main()
