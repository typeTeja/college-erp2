"""
Academic Dashboard API Endpoint
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_session, get_current_user
from app.models.user import User
from app.schemas.dashboard import AcademicDashboardResponse
from app.domains.academic.services.dashboard_service import AcademicDashboardService

router = APIRouter()


@router.get("/", response_model=AcademicDashboardResponse)
def get_academic_dashboard(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    program_id: Optional[int] = Query(None, description="Filter by program ID"),
    batch_id: Optional[int] = Query(None, description="Filter by batch ID")
):
    """
    Get academic dashboard with complete hierarchy
    
    Returns:
    - Batches with nested structure (Years → Semesters → Sections → Labs)
    - Student counts and capacity utilization
    - Faculty assignments
    - Summary statistics
    
    Filters:
    - program_id: Show only batches for specific program
    - batch_id: Show only specific batch
    """
    return AcademicDashboardService.get_dashboard_data(
        session=session,
        program_id=program_id,
        batch_id=batch_id
    )
