"""
Script to forcefully drop ALL tables in the database.
Handles foreign key constraints by disabling checks.
"""
import sys
import os
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine

def nuke_database():
    """Drop all tables avoiding FK constraints"""
    print("⚠️  WARNING: This will delete ALL data in the database!")
    print("Connecting to database...")
    
    with engine.connect() as connection:
        # Disable FK checks
        print("Disabling foreign key checks...")
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        # Get all table names
        print("Fetching table list...")
        result = connection.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        
        if not tables:
            print("Database is empty.")
        else:
            print(f"Found {len(tables)} tables: {', '.join(tables)}")
            
            # Drop each table
            for table in tables:
                print(f"Dropping table: {table}...")
                connection.execute(text(f"DROP TABLE IF EXISTS `{table}`"))
        
        # Re-enable FK checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        connection.commit()
        
    print("✅ All tables dropped successfully!")

if __name__ == "__main__":
    nuke_database()
