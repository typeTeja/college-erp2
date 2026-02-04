"""
Script to recreate the database schema from scratch and seed initial admin data.
This is used to sync the database with SQLModel definitions during development.
"""
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel, Session, select, text
from app.db.session import engine
from app.core.security import get_password_hash
from app.models import *  # Ensure all models are registered in SQLModel metadata

def load_json(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data", filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found in {filepath}, skipping.")
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)

def recreate_db():
    print("⚠️  WARNING: This will drop ALL tables and recreate them!")
    
    print("Dropping all tables with CASCADE...")
    with engine.connect() as conn:
        # PostgreSQL specific way to drop all tables with cascade
        conn.execute(text("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """))
        conn.commit()
    print("✅ All tables dropped successfully!")
    
    print("Recreating all tables based on current SQLModel definitions...")
    SQLModel.metadata.create_all(engine)
    print("✅ All tables recreated successfully!")
    
    print("Seeding initial data...")
    with Session(engine) as session:
        # 1. Seed Roles and Permissions (System defaults)
        # Assuming we have a standard way to seed roles
        # For now, let's at least ensure SUPER_ADMIN exists
        from app.models import Role, User, UserRole
        
        roles_data = [
            {"name": "SUPER_ADMIN", "description": "Full System Access", "is_system": True},
            {"name": "ADMIN", "description": "Administrative Access", "is_system": True},
            {"name": "FACULTY", "description": "Faculty Access", "is_system": True},
            {"name": "STUDENT", "description": "Student Access", "is_system": True},
            {"name": "PARENT", "description": "Parent Access", "is_system": True},
        ]
        
        created_roles = {}
        for r_data in roles_data:
            role = session.exec(select(Role).where(Role.name == r_data["name"])).first()
            if not role:
                role = Role(**r_data)
                session.add(role)
            created_roles[r_data["name"]] = role
        
        session.commit()
        print("✅ Core roles seeded.")

        # 2. Seed Admin User
        users_data = load_json("users.json")
        if users_data:
            for role_group in users_data:
                role_name = role_group["role_name"]
                if role_name not in created_roles:
                    continue
                
                target_role = created_roles[role_name]
                
                for user_data in role_group["users"]:
                    email = user_data["email"]
                    user = session.exec(select(User).where(User.email == email)).first()
                    if not user:
                        user = User(
                            email=email,
                            username=email.split('@')[0],
                            full_name=user_data["full_name"],
                            hashed_password=get_password_hash(user_data.get("password", "password123")),
                            is_active=True,
                            is_superuser=(role_name == "SUPER_ADMIN")
                        )
                        session.add(user)
                        session.commit()
                        session.refresh(user)
                        
                        user_role = UserRole(user_id=user.id, role_id=target_role.id)
                        session.add(user_role)
                        session.commit()
                        print(f"✅ Created User: {user.full_name} ({email}) with role {role_name}")
        else:
            print("⚠️ No users.json found for seeding.")

    print("\n🎉 Database schema recreation and initial seeding complete!")

if __name__ == "__main__":
    recreate_db()
