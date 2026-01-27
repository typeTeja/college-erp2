"""
Simple script to delete batches using the existing app context
Run from apps/api directory: python delete_batches_simple.py
"""
import sys
import os

# Ensure we're in the right directory
if not os.path.exists('app'):
    print("❌ Error: Please run this from the apps/api directory")
    print("   cd apps/api")
    print("   python delete_batches_simple.py")
    sys.exit(1)

from sqlmodel import Session, select
from app.core.db import engine
from app.models.academic.batch import AcademicBatch

def main():
    print("=" * 60)
    print("🗑️  Delete All Academic Batches")
    print("=" * 60)
    print()
    
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
