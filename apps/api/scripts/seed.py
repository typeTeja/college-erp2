import sys
import os
import json
from datetime import datetime, date

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
from app.models.master_data import (
    AcademicYear, Section, Designation, ScholarshipSlab
)
from app.models.subject import Subject
from app.models.hostel import HostelBlock, HostelRoom, RoomType
from app.models.library import Book
from app.models.odc import ODCHotel
from app.models.academic.entrance_exam import EntranceTestConfig

def load_json(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data", filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found in {filepath}, skipping.")
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)

def get_or_create(session, model, defaults=None, **kwargs):
    stmt = select(model).filter_by(**kwargs)
    instance = session.exec(stmt).first()
    if instance:
        return instance, False
    
    params = dict(kwargs)
    if defaults:
        params.update(defaults)
    instance = model(**params)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance, True

def seed_users(session):
    print("--- Seeding Users and Roles ---")
    data = load_json("users.json")
    if not data: return
    
    for role_group in data:
        role_name = role_group["role_name"]
        role, _ = get_or_create(session, Role, name=role_name, defaults={"description": f"{role_name} Role"})
        
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
                    is_active=user_data.get("is_active", True)
                )
                session.add(user)
                session.commit()
                session.refresh(user)
                
                user_role = UserRole(user_id=user.id, role_id=role.id)
                session.add(user_role)
                session.commit()
                print(f"Created User: {user.full_name} ({role.name})")
            else:
                # Update phone if missing
                mobile = user_data.get("mobile")
                if mobile and not user.phone:
                    user.phone = mobile
                    session.add(user)
                    session.commit()
                    print(f"Updated User Phone: {user.full_name}")

def seed_academic(session):
    print("--- Seeding Academic Data ---")
    data = load_json("academic.json")
    
    # Years
    for year_data in data.get("academic_years", []):
        y_data = year_data.copy()
        y_data["start_date"] = datetime.strptime(y_data["start_date"], "%Y-%m-%d").date()
        y_data["end_date"] = datetime.strptime(y_data["end_date"], "%Y-%m-%d").date()
        get_or_create(session, AcademicYear, name=y_data["name"], defaults=y_data)
        print(f"Academic Year: {y_data['name']}")

    # Designations
    for desig in data.get("designations", []):
        get_or_create(session, Designation, name=desig["name"], code=desig["code"], defaults=desig)
        
    # Departments
    dept_map = {}
    for dept in data.get("departments", []):
        d, created = get_or_create(session, Department, code=dept["code"], defaults={"name": dept["name"]})
        dept_map[dept["code"]] = d
        if created: print(f"Department: {dept['name']}")

    # Programs
    for prog in data.get("programs", []):
        dept = dept_map.get(prog.get("department_code"))
        if dept:
            p_data = {
                "name": prog["name"],
                "department_id": dept.id,
                "duration_years": prog.get("duration_years", 3)
            }
            get_or_create(session, Program, code=prog["code"], defaults=p_data)
            print(f"Program: {prog['name']}")

    # Subjects
    for subj in data.get("subjects", []):
        get_or_create(session, Subject, code=subj["code"], defaults=subj)
        
    # Sections (Generic)
    for sec in data.get("sections", []):
        # Linking sections to Batches logic is complex without explicit batch seed. 
        # Skipping section creation for now as it depends on BatchSemester which is dynamic.
        pass

def seed_hostel(session):
    print("--- Seeding Hostel Data ---")
    data = load_json("hostel.json")
    
    for block_data in data.get("blocks", []):
        rooms_data = block_data.pop("rooms", [])
        block, created = get_or_create(session, HostelBlock, name=block_data["name"], defaults=block_data)
        if created: print(f"Hostel Block: {block.name}")
        
        for r in rooms_data:
            # Check room existence
            existing = session.exec(
                select(HostelRoom).where(HostelRoom.room_number == r["room_number"], HostelRoom.block_id == block.id)
            ).first()
            if not existing:
                room = HostelRoom(block_id=block.id, **r)
                session.add(room)
                session.commit()

def seed_library(session):
    print("--- Seeding Library Data ---")
    data = load_json("library.json")
    for book in data.get("books", []):
        get_or_create(session, Book, isbn=book["isbn"], defaults=book)

def seed_odc(session):
    print("--- Seeding ODC Data ---")
    data = load_json("odc.json")
    for hotel in data.get("hotels", []):
        get_or_create(session, ODCHotel, name=hotel["name"], defaults=hotel)

def seed_entrance(session):
    print("--- Seeding Entrance Exam Data ---")
    data = load_json("entrance_exam.json")
    
    for test in data.get("tests", []):
        t_data = test.copy()
        t_data["test_date"] = datetime.strptime(t_data["test_date"], "%Y-%m-%d").date()
        get_or_create(session, EntranceTestConfig, test_code=t_data["test_code"], defaults=t_data)

    for slab in data.get("scholarship_slabs", []):
        get_or_create(session, ScholarshipSlab, code=slab["code"], defaults=slab)

def seed_data():
    with Session(engine) as session:
        seed_users(session)
        seed_academic(session)
        seed_hostel(session)
        seed_library(session)
        seed_odc(session)
        seed_entrance(session)
        
        print("\n✅ All seed data populated successfully!")

if __name__ == "__main__":
    seed_data()
