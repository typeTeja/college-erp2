"""
Quick setup script to create initial admin user and roles
Run this after running migrations
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.core.security import get_password_hash

def create_initial_data():
    """Create initial roles and admin user"""
    with Session(engine) as session:
        # Check if roles exist
        existing_roles = session.exec(select(Role)).all()
        if existing_roles:
            print("✓ Roles already exist")
        else:
            # Create roles
            roles_data = [
                {"name": "SUPER_ADMIN", "description": "Super Administrator with full access"},
                {"name": "ADMIN", "description": "Administrator"},
                {"name": "FACULTY", "description": "Faculty Member"},
                {"name": "STUDENT", "description": "Student"},
                {"name": "APPLICANT", "description": "Applicant (Pre-admission)"},
                {"name": "PARENT", "description": "Parent/Guardian"},
                {"name": "STAFF", "description": "Administrative Staff"},
            ]
            
            for role_data in roles_data:
                role = Role(**role_data)
                session.add(role)
            
            session.commit()
            print("✓ Created default roles")
        
        # Check if admin user exists
        admin = session.exec(select(User).where(User.username == "admin")).first()
        if admin:
            print("✓ Admin user already exists")
        else:
            # Create admin user
            admin = User(
                username="admin",
                email="admin@college.edu",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                is_superuser=True,
                is_active=True
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
            
            # Assign SUPER_ADMIN role
            super_admin_role = session.exec(
                select(Role).where(Role.name == "SUPER_ADMIN")
            ).first()
            
            if super_admin_role:
                user_role = UserRole(user_id=admin.id, role_id=super_admin_role.id)
                session.add(user_role)
                session.commit()
            
            print("✓ Created admin user")
            print("  Username: admin")
            print("  Password: admin123")
            print("  ⚠️  CHANGE THIS PASSWORD IN PRODUCTION!")

if __name__ == "__main__":
    print("Creating initial data...")
    create_initial_data()
    print("\n✅ Setup complete!")
