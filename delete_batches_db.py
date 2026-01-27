"""
Direct Database Script to Delete All Academic Batches

This script connects directly to the database and deletes all batches.
Run this from the apps/api directory with your virtual environment activated.

Usage:
    cd apps/api
    python ../../delete_batches_db.py
"""

import os
import sys
from sqlmodel import Session, select, create_engine

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'api'))

from app.core.config import settings
from app.models.academic.batch import AcademicBatch

def main():
    print("=" * 60)
    print("🗑️  Delete All Academic Batches (Direct DB)")
    print("=" * 60)
    print()
    
    # Create engine
    engine = create_engine(str(settings.DATABASE_URL))
    
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
            print(f"Deleting batch {batch.id} ({batch.batch_code})... ", end="")
            session.delete(batch)
            print("✅")
        
        session.commit()
        
        print()
        print("=" * 60)
        print(f"✅ Successfully deleted all {len(batches)} batches!")
        print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
