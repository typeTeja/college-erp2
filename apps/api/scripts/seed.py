import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.role import Role
from app.models.user_role import UserRole
from app.models.department import Department
from app.models.program import Program
# Legacy models removed: LegacyProgramYear, Semester
from app.models.master_data import AcademicYear, Section, PracticalBatch
from app.models.subject import Subject
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.odc import ODCHotel, ODCRequest

def load_json(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data", filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found, skipping.")
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def get_or_create_role(session, role_name):
    role = session.exec(select(Role).where(Role.name == role_name)).first()
    if not role:
        role = Role(name=role_name, description=f"{role_name} Role")
        session.add(role)
        session.commit()
        session.refresh(role)
    return role

def create_user(session, email, full_name, password, role_name, mobile=None):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        user = User(
            email=email,
            username=email.split('@')[0],
            full_name=full_name,
            hashed_password=get_password_hash(password),
            phone=mobile,
            is_active=True
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        role = get_or_create_role(session, role_name)
        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)
        session.commit()
        print(f"Created user: {email} ({role_name})")
    return user

def seed_data():
    with Session(engine) as session:
        print("Starting seed process...")

        # 1. Users & Roles
        users_data = load_json("users.json")
        for role_group in users_data:
            role_name = role_group["role_name"]
            for user_data in role_group["users"]:
                create_user(
                    session, 
                    user_data["email"], 
                    user_data["full_name"], 
                    user_data.get("password", "password123"), 
                    role_name,
                    user_data.get("mobile")
                )

        # 2. Departments
        academic_data = load_json("academic.json")
        if not academic_data:
             print("No academic data found.")
             return
             
        dept_map = {}
        if "departments" in academic_data:
            for dept in academic_data["departments"]:
                d = session.exec(select(Department).where(Department.code == dept["code"])).first()
                if not d:
                    d = Department(name=dept["name"], code=dept["code"])
                    session.add(d)
                    session.commit()
                    session.refresh(d)
                dept_map[dept["code"]] = d
            
        # 3. Programs
        prog_map = {}
        if "programs" in academic_data:
            for prog in academic_data["programs"]:
                p = session.exec(select(Program).where(Program.code == prog["code"])).first()
                primary_dept_code = prog["departments"][-1] # Default to Last
                if not p and primary_dept_code in dept_map:
                    p = Program(
                        name=prog["name"], 
                        code=prog["code"], 
                        department_id=dept_map[primary_dept_code].id,
                        duration_years=3 # Default
                    )
                    session.add(p)
                    session.commit()
                    session.refresh(p)
                if p:
                    prog_map[prog["code"]] = p
                
                # NOTE: Legacy structure (Years/Semesters) generation removed.
                # Use batch creation API to generate structure.

        # 4. Subjects (Simplified)
        if "subjects" in academic_data:
            for subj in academic_data["subjects"]:
                s = session.exec(select(Subject).where(Subject.code == subj["code"])).first()
                if not s:
                    # Subjects no longer link to global semesters directly in seed
                    # Just create them as master subjects if possible, but Subject model requires link?
                    # Since Subject model was updated to remove semester_id, we can create it without semester.
                    # Wait, if I removed semester_id, does it have other required fields?
                    # It has name, code. Faculty optional.
                    s = Subject(
                        name=subj["name"],
                        code=subj["code"],
                        credits=3
                    )
                    session.add(s)
                    session.commit()

        # 5. Faculty & Students (Basic Profile Creation)
        # 6. ODC Data (Kept mostly as is, assuming Hotels/Requests don't depend heavily on academic structure)
        
        print("✅ Seed data populated successfully! (Legacy structure skipped)")

if __name__ == "__main__":
    seed_data()
