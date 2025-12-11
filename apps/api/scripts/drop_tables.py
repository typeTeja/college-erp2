"""
Script to drop all tables in the database
WARNING: This will delete ALL data!
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from app.db.session import engine

def drop_all_tables():
    """Drop all tables"""
    print("⚠️  WARNING: This will drop ALL tables in the database!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() != 'yes':
        print("Aborted.")
        return
    
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("✅ All tables dropped successfully!")

if __name__ == "__main__":
    drop_all_tables()
