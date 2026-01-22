import sys
import os
from sqlalchemy import text
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from app.db.session import engine
from sqlmodel import Session

def run_migration():
    print("Running migration for BatchSemester dates...")
    with Session(engine) as session:
        try:
            # Check if column exists
            session.exec(text("SELECT start_date FROM batch_semesters LIMIT 1"))
            print("Columns already exist.")
        except Exception:
            session.rollback()
            print("Adding columns...")
            try:
                session.exec(text("ALTER TABLE batch_semesters ADD COLUMN start_date DATE"))
                session.exec(text("ALTER TABLE batch_semesters ADD COLUMN end_date DATE"))
                session.exec(text("ALTER TABLE batch_semesters ADD COLUMN is_active BOOLEAN DEFAULT FALSE"))
                session.commit()
                print("Migration successful.")
            except Exception as e:
                print(f"Migration failed: {e}")
                session.rollback()

if __name__ == "__main__":
    run_migration()
