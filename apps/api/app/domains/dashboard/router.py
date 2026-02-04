from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api import deps
from app.models import User
from app.api.deps import get_current_user
from app.db.session import get_session
from app.domains.dashboard.service import dashboard_service
from app.domains.dashboard.schemas import (
    PrincipalDashboardResponse, ParentDashboardResponse,
    StudentDashboardResponse, StaffDashboardResponse,
    FacultyDashboardResponse
)

router = APIRouter()

@router.get("/principal", response_model=PrincipalDashboardResponse)
def get_principal_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Get principal dashboard data.
    Requires Admin/Principal privileges.
    """
    # TODO: Add role check
    # if not current_user.is_superuser and "PRINCIPAL" not in current_user.roles:
    #     raise HTTPException(status_code=403, detail="Not authorized")
    
    return dashboard_service.get_principal_dashboard(db)

@router.get("/parent", response_model=ParentDashboardResponse)
def get_parent_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Get parent dashboard data.
    """
    return dashboard_service.get_parent_dashboard(db, current_user.id)

@router.get("/student", response_model=StudentDashboardResponse)
def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Get student dashboard data.
    """
    return dashboard_service.get_student_dashboard(db, current_user.id)

@router.get("/staff", response_model=StaffDashboardResponse)
def get_staff_dashboard(
    role: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Get staff dashboard data based on role.
    """
    return dashboard_service.get_staff_dashboard(db, role)

@router.get("/faculty", response_model=FacultyDashboardResponse)
def get_faculty_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Get faculty dashboard data.
    """
    return dashboard_service.get_faculty_dashboard(db, current_user.id)

@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
) -> Any:
    """
    Compatibility endpoint for legacy /dashboard/stats.
    """
    return dashboard_service.get_principal_dashboard(db)
