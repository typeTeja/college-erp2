import sys
import os
import json
from datetime import datetime, timedelta

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
from app.models.program_year import ProgramYear
from app.models.semester import Semester
from app.models.subject import Subject
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.odc import ODCHotel, ODCRequest, ODCStatus, GenderPreference

def load_json(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed_data", filename)
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

        # 2. Departments, Programs, Subjects
        academic_data = load_json("academic.json")
        
        # Departments
        dept_map = {}
        for dept in academic_data["departments"]:
            d = session.exec(select(Department).where(Department.code == dept["code"])).first()
            if not d:
                d = Department(name=dept["name"], code=dept["code"])
                session.add(d)
                session.commit()
                session.refresh(d)
            dept_map[dept["code"]] = d
            
        # Programs
        prog_map = {}
        for prog in academic_data["programs"]:
            p = session.exec(select(Program).where(Program.code == prog["code"])).first()
            # Determine dept from list - assume first one for primary mapping or find common
            # For simplicity, map to Management or the first one in list that exists
            primary_dept_code = prog["departments"][-1] # Default to Management/Last
            if not p:
                p = Program(
                    name=prog["name"], 
                    code=prog["code"], 
                    department_id=dept_map[primary_dept_code].id
                )
                session.add(p)
                session.commit()
                session.refresh(p)
            prog_map[prog["code"]] = p
            
            # Years and Semesters
            for year_data in prog["years"]:
                y_num = year_data["year"]
                # Create ProgramYear
                py = session.exec(select(ProgramYear).where(
                    ProgramYear.program_id == p.id, 
                    ProgramYear.year_number == y_num
                )).first()
                if not py:
                    py = ProgramYear(name=f"Year {y_num}", year_number=y_num, program_id=p.id)
                    session.add(py)
                    session.commit()
                    session.refresh(py)
                
                # Create Semesters
                for sem_num in year_data["semesters"]:
                    sem = session.exec(select(Semester).where(
                        Semester.program_year_id == py.id,
                        Semester.semester_number == sem_num
                    )).first()
                    if not sem:
                        sem = Semester(
                            name=f"Semester {sem_num}", 
                            semester_number=sem_num, 
                            program_year_id=py.id
                        )
                        session.add(sem)
                        session.commit()

        # Subjects
        # Need to find semester ID by loop
        for subj in academic_data["subjects"]:
            s = session.exec(select(Subject).where(Subject.code == subj["code"])).first()
            if not s:
                # Find semester - naive search for now (assuming uniqueness of sem number across active programs or just picking first found)
                # Better: Link specific subject to program sem. 
                # For this seed, we bind to BHM Semesters primarily
                bhm_prog = prog_map.get("BHM")
                # find BHM year for this sem
                target_sem = None
                # Scan BHM years
                py_stmt = select(ProgramYear).where(ProgramYear.program_id == bhm_prog.id)
                pys = session.exec(py_stmt).all()
                for py in pys:
                    sem_stmt = select(Semester).where(
                        Semester.program_year_id == py.id, 
                        Semester.semester_number == subj["sem"]
                    )
                    found_sem = session.exec(sem_stmt).first()
                    if found_sem:
                        target_sem = found_sem
                        break
                
                if target_sem:
                    s = Subject(
                        name=subj["name"],
                        code=subj["code"],
                        semester_id=target_sem.id,
                        credits=3
                    )
                    session.add(s)
                    session.commit()

        # 3. Faculty
        faculty_data = load_json("faculty.json")
        for fac in faculty_data:
            # Create User
            user = create_user(session, fac["email"], fac["full_name"], "password123", "FACULTY", fac["mobile"])
            
            # Create Faculty Profile
            f_profile = session.exec(select(Faculty).where(Faculty.user_id == user.id)).first()
            if not f_profile:
                f_profile = Faculty(
                    name=fac["full_name"],
                    user_id=user.id,
                    department=fac["department_code"], # Storing code as string per model
                    email=fac["email"],
                    phone=fac["mobile"],
                    qualification="PhD/Master in Hotel Mgmt"
                )
                session.add(f_profile)
                session.commit()
                session.refresh(f_profile)
            
            # Assign Subjects
            if "subjects" in fac:
                for subj_code in fac["subjects"]:
                    subj = session.exec(select(Subject).where(Subject.code == subj_code)).first()
                    if subj:
                        subj.faculty_id = f_profile.id
                        session.add(subj)
                session.commit()
        
        # 4. Students
        students_data = load_json("students.json")
        for stu in students_data:
            # Create User
            user = create_user(session, stu["email"], stu["full_name"], "password123", "STUDENT")
            
            # Create Student Profile
            s_profile = session.exec(select(Student).where(Student.user_id == user.id)).first()
            if not s_profile:
                # Find Program
                prog = prog_map.get(stu["program_code"])
                if prog and user.id:
                    s_profile = Student(
                        name=stu["full_name"],
                        email=stu["email"],
                        user_id=user.id,
                        program_id=prog.id,
                        current_year=stu["year"],
                        admission_number=f"ADM{datetime.now().year}{user.id:04d}", # Generate pseudo admission num
                        phone=f"999{user.id:07d}"
                    )
                    session.add(s_profile)
                    session.commit()

        # 5. ODC Data
        odc_data = load_json("odc.json")
        
        # Hotels
        hotel_objs = []
        for h in odc_data[0]["hotels"]:
            hotel = session.exec(select(ODCHotel).where(ODCHotel.name == h["name"])).first()
            if not hotel:
                hotel = ODCHotel(**h)
                session.add(hotel)
                session.commit()
                session.refresh(hotel)
            hotel_objs.append(hotel)
            
        # Requests
        # Get admin user for 'created_by'
        admin_user = session.exec(select(User).where(User.email == "admin@college.edu")).first()
        if admin_user:
            for req in odc_data[0]["requests"]:
                h_idx = req.pop("hotel_index")
                hotel = hotel_objs[h_idx] if h_idx < len(hotel_objs) else hotel_objs[0]
                
                # Check duplicate
                existing_req = session.exec(select(ODCRequest).where(
                    ODCRequest.event_name == req["event_name"],
                    ODCRequest.hotel_id == hotel.id
                )).first()
                
                if not existing_req:
                    # Calculate dates
                    offset = req.pop("event_date_offset")
                    evt_date = datetime.now().date() + timedelta(days=offset)
                    # Parse time
                    evt_time = datetime.strptime(req["event_time"], "%H:%M").time()
                    report_dt = datetime.combine(evt_date, evt_time)
                    
                    odc_req = ODCRequest(
                        hotel_id=hotel.id,
                        event_date=evt_date,
                        report_time=report_dt,
                        created_by_id=admin_user.id,
                        **req
                    )
                    session.add(odc_req)
            session.commit()

        print("✅ Seed data populated successfully!")

if __name__ == "__main__":
    seed_data()
