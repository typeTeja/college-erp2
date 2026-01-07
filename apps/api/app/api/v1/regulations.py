"""
Regulation API Endpoints

SAFETY RULES:
- Locked regulations CANNOT be modified or deleted
- Optimistic locking prevents concurrent updates
- Admin-only for create/update/delete operations
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from datetime import datetime

from app.api import deps
from app.models.user import User
from app.models.academic.regulation import (
    Regulation,
    RegulationSubject,
    RegulationSemester,
    RegulationPromotionRule
)
from app.schemas.academic.regulation import (
    RegulationCreate,
    RegulationUpdate,
    RegulationRead,
    RegulationWithDetails,
    RegulationSubjectCreate,
    RegulationSubjectUpdate,
    RegulationSubjectRead,
    RegulationSemesterCreate,
    RegulationSemesterRead,
    RegulationPromotionRuleCreate,
    RegulationPromotionRuleRead
)

router = APIRouter()


def check_admin(current_user: User):
    """Check if user has admin privileges"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True


# ============================================================================
# Regulation Endpoints
# ============================================================================

@router.get("/", response_model=List[RegulationRead], tags=["Regulations"])
def list_regulations(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    program_id: Optional[int] = None,
    is_locked: Optional[bool] = None,
    is_active: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """List all regulations with optional filters"""
    stmt = select(Regulation)
    
    if program_id:
        stmt = stmt.where(Regulation.program_id == program_id)
    if is_locked is not None:
        stmt = stmt.where(Regulation.is_locked == is_locked)
    if is_active is not None:
        stmt = stmt.where(Regulation.is_active == is_active)
    
    stmt = stmt.offset(skip).limit(limit).order_by(Regulation.created_at.desc())
    
    return session.exec(stmt).all()


@router.get("/{id}", response_model=RegulationWithDetails, tags=["Regulations"])
def get_regulation(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Get regulation with all details"""
    regulation = session.get(Regulation, id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    return regulation


@router.post("/", response_model=RegulationRead, tags=["Regulations"])
def create_regulation(
    data: RegulationCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new regulation (admin only)"""
    check_admin(current_user)
    
    # Check for duplicate regulation_code
    existing = session.exec(
        select(Regulation).where(Regulation.regulation_code == data.regulation_code)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Regulation code '{data.regulation_code}' already exists"
        )
    
    regulation = Regulation(
        **data.model_dump(),
        created_by=current_user.id,
        updated_by=current_user.id
    )
    
    session.add(regulation)
    session.commit()
    session.refresh(regulation)
    
    return regulation


@router.patch("/{id}", response_model=RegulationRead, tags=["Regulations"])
def update_regulation(
    id: int,
    data: RegulationUpdate,
    version: int = Query(..., description="Current version for optimistic locking"),
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update regulation (admin only)
    
    SAFETY CHECKS:
    - Cannot update if is_locked = True
    - Optimistic locking with version check
    """
    check_admin(current_user)
    
    regulation = session.get(Regulation, id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # CRITICAL: Check if locked
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Academic data is locked for this regulation and cannot be modified. "
                   "This regulation is already in use by one or more batches."
        )
    
    # CRITICAL: Optimistic locking check
    if regulation.version != version:
        raise HTTPException(
            status_code=409,
            detail=f"Regulation has been modified by another user. "
                   f"Current version: {regulation.version}, your version: {version}"
        )
    
    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(regulation, key, value)
    
    # Update metadata
    regulation.version += 1
    regulation.updated_at = datetime.utcnow()
    regulation.updated_by = current_user.id
    
    session.add(regulation)
    session.commit()
    session.refresh(regulation)
    
    return regulation


@router.delete("/{id}", tags=["Regulations"])
def delete_regulation(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete regulation (admin only)
    
    SAFETY CHECK: Cannot delete if is_locked = True
    """
    check_admin(current_user)
    
    regulation = session.get(Regulation, id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # CRITICAL: Check if locked
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Academic data is locked for this regulation and cannot be deleted. "
                   "This regulation is already in use by one or more batches."
        )
    
    session.delete(regulation)
    session.commit()
    
    return {"status": "success", "message": "Regulation deleted"}


@router.post("/{id}/lock", response_model=RegulationRead, tags=["Regulations"])
def lock_regulation(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Manually lock a regulation (admin only)
    
    NOTE: This is usually done automatically when first batch is created
    """
    check_admin(current_user)
    
    regulation = session.get(Regulation, id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    if regulation.is_locked:
        raise HTTPException(status_code=400, detail="Regulation is already locked")
    
    regulation.is_locked = True
    regulation.locked_at = datetime.utcnow()
    regulation.locked_by = current_user.id
    regulation.version += 1
    
    session.add(regulation)
    session.commit()
    session.refresh(regulation)
    
    return regulation


# ============================================================================
# Regulation Subject Endpoints
# ============================================================================

@router.get("/regulations/{regulation_id}/subjects", response_model=List[RegulationSubjectRead], tags=["Regulation Subjects"])
def list_regulation_subjects(
    regulation_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    semester_no: Optional[int] = None
):
    """List subjects for a regulation"""
    # Verify regulation exists
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    stmt = select(RegulationSubject).where(RegulationSubject.regulation_id == regulation_id)
    
    if semester_no:
        stmt = stmt.where(RegulationSubject.semester_no == semester_no)
    
    stmt = stmt.order_by(RegulationSubject.semester_no, RegulationSubject.subject_code)
    
    return session.exec(stmt).all()


@router.post("/regulations/{regulation_id}/subjects", response_model=RegulationSubjectRead, tags=["Regulation Subjects"])
def create_regulation_subject(
    regulation_id: int,
    data: RegulationSubjectCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create subject for regulation (admin only, regulation must not be locked)"""
    check_admin(current_user)
    
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # CRITICAL: Check if locked
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Cannot add subjects to locked regulation"
        )
    
    # Check for duplicate subject_code
    existing = session.exec(
        select(RegulationSubject)
        .where(RegulationSubject.regulation_id == regulation_id)
        .where(RegulationSubject.subject_code == data.subject_code)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Subject code '{data.subject_code}' already exists in this regulation"
        )
    
    subject = RegulationSubject(**data.model_dump())
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return subject


@router.patch("/regulations/{regulation_id}/subjects/{subject_id}", response_model=RegulationSubjectRead, tags=["Regulation Subjects"])
def update_regulation_subject(
    regulation_id: int,
    subject_id: int,
    data: RegulationSubjectUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update subject (admin only, regulation must not be locked)"""
    check_admin(current_user)
    
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # CRITICAL: Check if locked
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Cannot modify subjects of locked regulation"
        )
    
    subject = session.get(RegulationSubject, subject_id)
    if not subject or subject.regulation_id != regulation_id:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(subject, key, value)
    
    subject.updated_at = datetime.utcnow()
    
    session.add(subject)
    session.commit()
    session.refresh(subject)
    
    return subject


@router.delete("/regulations/{regulation_id}/subjects/{subject_id}", tags=["Regulation Subjects"])
def delete_regulation_subject(
    regulation_id: int,
    subject_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete subject (admin only, regulation must not be locked)"""
    check_admin(current_user)
    
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # CRITICAL: Check if locked
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete subjects from locked regulation"
        )
    
    subject = session.get(RegulationSubject, subject_id)
    if not subject or subject.regulation_id != regulation_id:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    session.delete(subject)
    session.commit()
    
    return {"status": "success", "message": "Subject deleted"}


# ============================================================================
# Regulation Semester Endpoints
# ============================================================================

@router.get("/regulations/{regulation_id}/semesters", response_model=List[RegulationSemesterRead], tags=["Regulation Semesters"])
def list_regulation_semesters(
    regulation_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """List semesters for a regulation"""
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    stmt = select(RegulationSemester).where(
        RegulationSemester.regulation_id == regulation_id
    ).order_by(RegulationSemester.semester_no)
    
    return session.exec(stmt).all()


@router.post("/regulations/{regulation_id}/semesters", response_model=RegulationSemesterRead, tags=["Regulation Semesters"])
def create_regulation_semester(
    regulation_id: int,
    data: RegulationSemesterCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create semester for regulation (admin only, regulation must not be locked)"""
    check_admin(current_user)
    
    regulation = session.get(Regulation, regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    if regulation.is_locked:
        raise HTTPException(
            status_code=400,
            detail="Cannot add semesters to locked regulation"
        )
    
    semester = RegulationSemester(**data.model_dump())
    session.add(semester)
    session.commit()
    session.refresh(semester)
    
    return semester
