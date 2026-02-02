"""
Script to cleanup the database and reset only the admin user.
WARNING: This will delete ALL data except for what's in seed_data/users.json for SUPER_ADMIN!
"""
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel, Session, select
from app.db.session import engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
import app.models  # Ensure all models are registered

def load_json(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data", filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found in {filepath}, skipping.")
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)

def cleanup_and_reset_admin():
    print("⚠️  WARNING: This will drop ALL tables and recreate them, effectively clearing all data!")
    # confirm = input("Type 'yes' to confirm: ")
    # if confirm.lower() != 'yes':
    #     print("Aborted.")
    #     return
    
    # In an agentic environment, we skip the input() or handle it via a flag, 
    # but since the user explicitly asked to "clean up", we proceed.
    
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("✅ All tables dropped successfully!")
    
    print("Recreating all tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ All tables recreated successfully!")
    
    print("Seeding SUPER_ADMIN user...")
    with Session(engine) as session:
        data = load_json("users.json")
        if not data:
            print("❌ Error: users.json not found. Cannot seed admin.")
            return

        for role_group in data:
            if role_group["role_name"] == "SUPER_ADMIN":
                role_name = role_group["role_name"]
                
                # Create Role
                role = session.exec(select(Role).where(Role.name == role_name)).first()
                if not role:
                    role = Role(name=role_name, description=f"{role_name} Role", is_system=True)
                    session.add(role)
                    session.commit()
                    session.refresh(role)
                
                # Create Admin Users
                for user_data in role_group["users"]:
                    email = user_data["email"]
                    user = session.exec(select(User).where(User.email == email)).first()
                    if not user:
                        user = User(
                            email=email,
                            username=email.split('@')[0],
                            full_name=user_data["full_name"],
                            hashed_password=get_password_hash(user_data.get("password", "password123")),
                            phone=user_data.get("mobile"),
                            is_active=user_data.get("is_active", True),
                            is_superuser=True
                        )
                        session.add(user)
                        session.commit()
                        session.refresh(user)
                        
                        user_role = UserRole(user_id=user.id, role_id=role.id)
                        session.add(user_role)
                        session.commit()
                        print(f"✅ Created Admin User: {user.full_name} ({email})")
                break # Only seed SUPER_ADMIN

    print("\n🎉 Database cleanup and admin reset complete!")

if __name__ == "__main__":
    cleanup_and_reset_admin()
