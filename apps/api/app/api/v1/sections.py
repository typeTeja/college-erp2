"""
Section API Service - PATCH endpoint for inline editing
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.api import deps
from app.models.user import User
from app.models.master_data import Section
from app.schemas.master_data import SectionUpdate, SectionRead
from app.utils.audit import log_update
from app.utils.academic_validation import validate_capacity_change, validate_faculty_assignment

router = APIRouter()


def check_admin(current_user: User):
    """Check if user has admin privileges"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True


@router.patch("/{id}", response_model=SectionRead, tags=["Sections"])
def update_section(
    id: int,
    data: SectionUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update section details (inline editing)
    
    Supports updating:
    - max_strength (with validation)
    - name
    - code
    - faculty_id
    """
    check_admin(current_user)
    
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Store old values for audit
    old_values = {
        "name": section.name,
        "code": section.code,
        "max_strength": section.max_strength,
        "faculty_id": section.faculty_id
    }
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Validate capacity change
    if "max_strength" in update_data:
        validate_capacity_change(section.current_strength or 0, update_data["max_strength"])
    
    # Validate faculty assignment
    if "faculty_id" in update_data and update_data["faculty_id"] is not None:
        validate_faculty_assignment(session, update_data["faculty_id"])
    
    # Check uniqueness of code within batch_semester
    if "code" in update_data:
        existing = session.exec(
            select(Section)
            .where(Section.batch_semester_id == section.batch_semester_id)
            .where(Section.code == update_data["code"])
            .where(Section.id != id)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Section code '{update_data['code']}' already exists in this semester"
            )
    
    # Apply updates
    for key, value in update_data.items():
        setattr(section, key, value)
    
    session.add(section)
    session.commit()
    session.refresh(section)
    
    # Log update
    new_values = {
        "name": section.name,
        "code": section.code,
        "max_strength": section.max_strength,
        "faculty_id": section.faculty_id
    }
    
    log_update(
        session=session,
        table_name="section",
        record_id=id,
        old_values=old_values,
        new_values=new_values,
        user_id=current_user.id,
        request=None
    )
    
    return section
