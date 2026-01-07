import sys
import os
from sqlalchemy import text
from sqlmodel import Session

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine

def fix_schema():
    print("Fixing subject table schema...")
    with Session(engine) as session:
        try:
            # Check if column exists
            print("Dropping semester_id from subject table...")
            session.exec(text("ALTER TABLE subject DROP COLUMN IF EXISTS semester_id"))
            session.commit()
            print("✅ Column dropped successfully")
        except Exception as e:
            print(f"Error: {e}")
            session.rollback()

if __name__ == "__main__":
    fix_schema()
