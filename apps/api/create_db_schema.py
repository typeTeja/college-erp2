"""
Create fresh database schema by dropping all tables first

This ensures a clean slate for SQLModel create_all
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Load environment variables
load_dotenv()

def drop_all_tables():
    """Drop all existing tables"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found")
    
    engine = create_engine(database_url)
    
    print("🗑️  Dropping all existing tables...")
    
    with engine.connect() as conn:
        # Get all table names
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"Found {len(tables)} existing tables")
            
            # Drop all tables
            conn.execute(text("DROP SCHEMA public CASCADE"))
            conn.execute(text("CREATE SCHEMA public"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
            conn.commit()
            
            print("✅ All tables dropped successfully")
        else:
            print("No existing tables found")
    
    engine.dispose()

def create_schema():
    """Create all tables using SQLModel"""
    # Import SQLModel first
    from sqlmodel import SQLModel, create_engine
    
    # Import all models - this registers them with SQLModel.metadata
    print("\n📦 Importing all models...")
    
    try:
        from app.models import user, program, student, admissions, fee
        from app.models.academic import entrance_exam, internal_exam, hall_ticket, university_exam
        from app.models import documents, student_portal, payment_gateway, attendance
        from app.models import library, hostel, transport, placement, hr, enhanced_admission
        print("✅ All models imported successfully")
    except Exception as e:
        print(f"⚠️  Warning during import: {e}")
        print("Continuing with available models...")
    
    database_url = os.getenv('DATABASE_URL')
    engine = create_engine(database_url, echo=False)
    
    print(f"\n🔨 Creating {len(SQLModel.metadata.tables)} tables...")
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    print("✅ Schema created successfully!")
    
    # List created tables
    inspector = inspect(engine)
    tables = sorted(inspector.get_table_names())
    
    print(f"\n📋 Created {len(tables)} tables:")
    for i, table in enumerate(tables, 1):
        print(f"  {i:2d}. {table}")
    
    engine.dispose()

if __name__ == "__main__":
    print("=" * 60)
    print("College ERP - Fresh Database Setup")
    print("=" * 60)
    
    try:
        # Step 1: Drop all existing tables
        drop_all_tables()
        
        # Step 2: Create fresh schema
        create_schema()
        
        print("\n" + "=" * 60)
        print("🎉 Database setup complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
