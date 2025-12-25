from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from app.api.deps import get_session, get_current_user
from app.models.user import User
from app.models.role import Role
from app.models.staff import Staff
from app.schemas.staff import StaffRead, StaffCreate, StaffUpdate
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[StaffRead])
def get_staff(
    session: Session = Depends(get_session),
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    offset: int = 0
):
    query = select(Staff)
    if department:
        query = query.where(Staff.department == department)
        
    return session.exec(query.offset(offset).limit(limit)).all()

@router.post("/", response_model=StaffRead)
def create_staff(
    staff_in: StaffCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Check if staff with email/mobile exists
    existing_staff = session.exec(select(Staff).where((Staff.email == staff_in.email) | (Staff.mobile == staff_in.mobile))).first()
    if existing_staff:
        raise HTTPException(status_code=400, detail="Staff with this email or mobile already exists")

    # 1. Create User Account
    # Default password policy: "Staff@123"
    hashed_password = get_password_hash("Staff@123")
    
    # Get or Create STAFF role
    staff_role = session.exec(select(Role).where(Role.name == "STAFF")).first()
    if not staff_role:
        staff_role = Role(name="STAFF", description="Non-Teaching Staff")
        session.add(staff_role)
        session.commit()
        session.refresh(staff_role)

    # Check for existing user (to avoid constraint error if user exists but not staff)
    existing_user = session.exec(select(User).where(User.email == staff_in.email)).first()
    
    if existing_user:
        # If user exists, just ensure they have the STAFF role
        if staff_role not in existing_user.roles:
            existing_user.roles.append(staff_role)
            session.add(existing_user)
            session.commit()
        new_user = existing_user
    else:
        new_user = User(
            email=staff_in.email,
            username=staff_in.email, # Use email as username
            hashed_password=hashed_password,
            full_name=staff_in.name,
            is_active=True
        )
        new_user.roles = [staff_role]
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    # 2. Create Staff Profile
    new_staff = Staff.from_orm(staff_in)
    new_staff.user_id = new_user.id
    
    session.add(new_staff)
    session.commit()
    session.refresh(new_staff)
    
    return new_staff

@router.get("/{staff_id}", response_model=StaffRead)
def get_staff_by_id(
    staff_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.put("/{staff_id}", response_model=StaffRead)
def update_staff(
    staff_id: int,
    staff_update: StaffUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
        
    staff_data = staff_update.dict(exclude_unset=True)
    for key, value in staff_data.items():
        setattr(staff, key, value)
        
    session.add(staff)
    session.commit()
    session.refresh(staff)
    return staff

@router.delete("/{staff_id}")
def delete_staff(
    staff_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Soft delete logic ideally, but for now hard delete or deactivation
    # Deactivate User
    if staff.user_id:
        user = session.get(User, staff.user_id)
        if user:
            user.is_active = False
            session.add(user)
            
    staff.is_active = False
    session.add(staff)
    session.commit()
    return {"message": "Staff deactivated successfully"}
