"""
Institute Information Router

API endpoints for institutional identity and contact details.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.system.services import SystemService
from app.domains.system.schemas import (
    InstituteInfoRead, InstituteInfoUpdate
)
from app.domains.auth.models import AuthUser as User

router = APIRouter()

@router.get("/", response_model=InstituteInfoRead)
def get_institute_info(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get institute information.
    Accessible to all authenticated users.
    """
    service = SystemService(session)
    return service.get_institute_info()

@router.put("/", response_model=InstituteInfoRead)
def update_institute_info(
    data: InstituteInfoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update institute information.
    Restricted to Admin/Super Admin.
    """
    # Simple check for Admin role
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update institute information"
        )
        
    service = SystemService(session)
    return service.update_institute_info(data)
