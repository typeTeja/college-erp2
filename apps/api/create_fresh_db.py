"""
Create fresh database on remote PostgreSQL server
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connection parameters
HOST = "72.61.242.232"
PORT = 5432
USER = "postgres"
PASSWORD = "rIMqouYR2F0rylFIqGbdAtPjqoFo4gToJik67rQsvpLxqGCj4ZB1qbOo1xP3vtnP"
NEW_DB_NAME = "college_erp_fresh"

def create_database():
    """Create the fresh database"""
    try:
        # Connect to default postgres database
        print(f"Connecting to PostgreSQL server at {HOST}...")
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database="postgres"  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (NEW_DB_NAME,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"⚠️  Database '{NEW_DB_NAME}' already exists. Dropping it...")
            cursor.execute(f"DROP DATABASE {NEW_DB_NAME}")
            print(f"✅ Database '{NEW_DB_NAME}' dropped successfully!")
        
        # Create database
        print(f"Creating database '{NEW_DB_NAME}'...")
        cursor.execute(f'CREATE DATABASE {NEW_DB_NAME}')
        print(f"✅ Database '{NEW_DB_NAME}' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Test connection to new database
        print(f"\nTesting connection to '{NEW_DB_NAME}'...")
        test_conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=NEW_DB_NAME
        )
        test_conn.close()
        print(f"✅ Connection to '{NEW_DB_NAME}' successful!")
        
        print(f"\n🎉 Database setup complete!")
        print(f"\nUpdate your .env file with:")
        print(f"DATABASE_URL=postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NEW_DB_NAME}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_database()
