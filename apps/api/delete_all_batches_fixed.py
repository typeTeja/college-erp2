"""
Fixed script to delete all academic batches
Deletes orphaned labs first, then batches

Usage from apps/api directory:
    python3 delete_all_batches_fixed.py
"""

import os
from pathlib import Path
from sqlmodel import Session, select, create_engine, text

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
    print("🗑️  Delete All Academic Batches (Fixed)")
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
        
        print(f"\n🗑️  Deleting academic data...\n")
        
        # Step 1: Delete orphaned practical batches (labs with null batch_semester_id)
        print("Step 1: Cleaning up orphaned lab groups... ", end="", flush=True)
        result = session.exec(text("DELETE FROM practical_batch WHERE batch_semester_id IS NULL"))
        session.commit()
        print("✅")
        
        # Step 2: Delete all practical batches
        print("Step 2: Deleting all lab groups... ", end="", flush=True)
        result = session.exec(text("DELETE FROM practical_batch"))
        session.commit()
        print("✅")
        
        # Step 3: Delete all sections
        print("Step 3: Deleting all sections... ", end="", flush=True)
        result = session.exec(text("DELETE FROM section"))
        session.commit()
        print("✅")
        
        # Step 4: Delete all batch subjects
        print("Step 4: Deleting all batch subjects... ", end="", flush=True)
        result = session.exec(text("DELETE FROM batch_subjects"))
        session.commit()
        print("✅")
        
        # Step 5: Delete all batch semesters
        print("Step 5: Deleting all batch semesters... ", end="", flush=True)
        result = session.exec(text("DELETE FROM batch_semesters"))
        session.commit()
        print("✅")
        
        # Step 6: Delete all program years
        print("Step 6: Deleting all program years... ", end="", flush=True)
        result = session.exec(text("DELETE FROM program_years"))
        session.commit()
        print("✅")
        
        # Step 7: Delete all batches
        print("Step 7: Deleting all batches... ", end="", flush=True)
        result = session.exec(text("DELETE FROM academic_batches"))
        session.commit()
        print("✅")
        
        print()
        print("=" * 60)
        print(f"✅ Successfully deleted all academic data!")
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
