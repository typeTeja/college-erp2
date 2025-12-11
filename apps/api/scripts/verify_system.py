import sys
import os
from sqlalchemy import inspect
from sqlmodel import Session, select

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from app.models.user import User
from app.models.role import Role
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate

def check_database():
    print("\n🔍 Analyzing Database Tables...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Found {len(tables)} tables:")
    for table in tables:
        columns = [col['name'] for col in inspector.get_columns(table)]
        print(f"  - {table}: {', '.join(columns)}")

    print("\n🔍 Checking Authentication...")
    with Session(engine) as session:
        # Check Roles
        roles = session.exec(select(Role)).all()
        print(f"\nRoles found: {len(roles)}")
        for r in roles:
            print(f"  - {r.name}")

        # Check Users
        users = session.exec(select(User)).all()
        print(f"\nUsers found: {len(users)}")
        
        # Test User Creation (if no admin found, though setup_initial_data should handle it)
        auth_service = AuthService(session)
        admin = auth_service.get_user_by_email("admin@college.edu")
        
        if admin:
            print(f"\n✅ Admin user found: {admin.username} ({admin.email})")
            print("   Authentication system seems to be working!")
        else:
            print("\n⚠️  No admin user found. Run setup_initial_data.py")
            
if __name__ == "__main__":
    check_database()
