import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from sqlmodel import Session

def cleanup_db():
    print("Cleaning up legacy tables...")
    with Session(engine) as session:
        # Drop tables with CASCADE to handle dependencies
        tables_to_drop = [
            # Truly legacy tables (unused in new system)
            "student_credit_tracker", 
            "legacy_program_year", 
            "schedule", 
            "semester", 
            "program_year", 
            "academic_batch"
            # "section", # Keeping as it is used (recreated)
            # "practical_batch" # Keeping as it is used (recreated)
        ]
        
        for table in tables_to_drop:
            try:
                print(f"Dropping table {table}...")
                session.exec(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                session.commit()
            except Exception as e:
                print(f"Error dropping {table}: {e}")
                session.rollback()
                
    print("Legacy tables dropped.")

if __name__ == "__main__":
    cleanup_db()
