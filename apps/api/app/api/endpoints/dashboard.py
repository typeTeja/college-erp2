from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func

from app.api import deps
from app.db.session import get_session
from app.models.user import User
from app.models.role import Role

router = APIRouter()

@router.get("/stats")
def get_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get dashboard statistics
    """
    total_users = session.exec(select(func.count(User.id))).one()
    active_users = session.exec(select(func.count(User.id)).where(User.is_active == True)).one()
    # Placeholder for student/faculty counts until those models are migrated
    total_students = 0 
    total_faculty = 0
    pending_admissions = 0
    
    return {
        "totalStudents": total_students, # Mocked for now
        "totalFaculty": total_faculty,   # Mocked for now
        "pendingAdmissions": pending_admissions, # Mocked for now
        "activeStudents": active_users, # Using active users as proxy
    }

@router.get("/recent-admissions")
def get_recent_admissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get recent admission applications
    """
    # Return empty list until Admissions module is migrated
    return []
