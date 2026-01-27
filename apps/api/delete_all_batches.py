"""
Standalone script to delete all academic batches
Reads database URL directly from .env file

Usage from apps/api directory:
    python3 delete_all_batches.py
"""

import os
from pathlib import Path
from sqlmodel import Session, select, create_engine

# Read DATABASE_URL from .env
env_path = Path(__file__).parent / '.env'
database_url = None

if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.startswith('DATABASE_URL='):
                database_url = line.split('=', 1)[1].strip().strip('"').strip("'")
                break

if not database_url:
    print("❌ Error: Could not find DATABASE_URL in .env file")
    exit(1)

# Import models after setting up path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from app.models.academic.batch import AcademicBatch

def main():
    print("=" * 60)
    print("🗑️  Delete All Academic Batches")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Get all batches
        batches = session.exec(select(AcademicBatch)).all()
        
        if not batches:
            print("✅ No batches found to delete!")
            return
        
        print(f"📋 Found {len(batches)} batch(es):\n")
        for batch in batches:
            print(f"  ID: {batch.id}")
            print(f"  Code: {batch.batch_code}")
            print(f"  Name: {batch.batch_name}")
            print(f"  Students: {batch.total_students}")
            print("-" * 50)
        
        print()
        print(f"⚠️  WARNING: This will delete ALL {len(batches)} batch(es)!")
        print("This will also delete all related:")
        print("  - Program Years")
        print("  - Semesters")
        print("  - Sections")
        print("  - Lab Groups")
        print("  - Batch Subjects")
        print()
        
        confirm = input("Type 'DELETE ALL' to confirm: ")
        
        if confirm != "DELETE ALL":
            print("\n❌ Deletion cancelled.")
            return
        
        print(f"\n🗑️  Deleting {len(batches)} batch(es)...\n")
        
        # Delete all batches (cascade will handle related records)
        for batch in batches:
            print(f"Deleting batch {batch.id} ({batch.batch_code})... ", end="", flush=True)
            session.delete(batch)
            print("✅")
        
        session.commit()
        
        print()
        print("=" * 60)
        print(f"✅ Successfully deleted all {len(batches)} batches!")
        print("=" * 60)
        print()
        print("You can now create new batches with the updated structure:")
        print("  - Go to /academics/bulk-setup")
        print("  - Use 'Lab Groups per Semester' (not per section)")
        print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
