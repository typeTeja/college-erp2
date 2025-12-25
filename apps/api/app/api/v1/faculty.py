from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_current_user, get_session
from app.models.user import User
from app.models.faculty import Faculty
from app.models.role import Role
from app.schemas.faculty import FacultyRead, FacultyCreate
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/me", response_model=FacultyRead)
def get_current_faculty(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current logged-in faculty member's profile.
    """
    faculty = session.exec(select(Faculty).where(Faculty.user_id == current_user.id)).first()
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty profile not found")
    return faculty

@router.get("/", response_model=List[FacultyRead])
def get_faculties(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    department: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve faculty members.
    """
    statement = select(Faculty)
    if department:
        statement = statement.where(Faculty.department == department)
        
    faculties = session.exec(statement.offset(offset).limit(limit)).all()
    return faculties

@router.post("/", response_model=FacultyRead)
def create_faculty(
    *,
    session: Session = Depends(get_session),
    faculty_in: FacultyCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new faculty member.
    """
    # Check if faculty with email exists
    if faculty_in.email:
        existing_faculty = session.exec(select(Faculty).where(Faculty.email == faculty_in.email)).first()
        if existing_faculty:
            raise HTTPException(status_code=400, detail="Faculty with this email already exists")

    # 1. Create User Account
    hashed_password = get_password_hash("Faculty@123")
    
    # Get or Create FACULTY role
    faculty_role = session.exec(select(Role).where(Role.name == "FACULTY")).first()
    if not faculty_role:
        faculty_role = Role(name="FACULTY", description="Teaching Faculty")
        session.add(faculty_role)
        session.commit()
        session.refresh(faculty_role)

    # Check for existing user
    existing_user = None
    if faculty_in.email:
        existing_user = session.exec(select(User).where(User.email == faculty_in.email)).first()
    
    if existing_user:
        if faculty_role not in existing_user.roles:
            existing_user.roles.append(faculty_role)
            session.add(existing_user)
            session.commit()
        new_user = existing_user
    else:
        new_user = User(
            email=faculty_in.email,
            username=faculty_in.email or faculty_in.name.lower().replace(" ", "."),
            hashed_password=hashed_password,
            full_name=faculty_in.name,
            is_active=True
        )
        new_user.roles = [faculty_role]
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    # 2. Create Faculty Profile
    db_faculty = Faculty.model_validate(faculty_in)
    db_faculty.user_id = new_user.id
    
    session.add(db_faculty)
    session.commit()
    session.refresh(db_faculty)
    
    return db_faculty

@router.get("/{id}", response_model=FacultyRead)
def get_faculty_by_id(
    *,
    session: Session = Depends(get_session),
    id: int,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get faculty by ID.
    """
    faculty = session.get(Faculty, id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return faculty
