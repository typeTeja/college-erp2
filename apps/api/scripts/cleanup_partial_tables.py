import sys
import os
from sqlalchemy import create_engine, text

# Add project root to path
sys.path.append(os.getcwd())
from app.config.settings import settings

def cleanup_tables():
    engine = create_engine(str(settings.DATABASE_URL))
    
    tables_to_drop = [
        "application_address",
        "application_bank_details",
        "application_document", # New table
        "application_education",
        "application_parent",
        "application_health"
    ]
    
    with engine.connect() as conn:
        print("Dropping tables if they exist...")
        for table in tables_to_drop:
            try:
                # Use CASCADE to remove dependent foreign keys from other tables slightly safer for cleanup
                conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Error dropping {table}: {e}")
        
        # Also drop the old applicationdocument table if it exists? 
        # The migration does that. If I drop it here, the migration might fail on drop_table.
        # But wait, checking if application_document (new) exists.
        
        conn.commit()
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup_tables()
