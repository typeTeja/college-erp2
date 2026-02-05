"""
Finance Domain Router

All API endpoints for the finance domain.

TODO: Implement finance endpoints:
- Fee management (fees)
- Payment gateway integration (gateway)
- Easebuzz payment processing (easebuzz)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.finance.services import fee_service
from app.domains.finance.schemas import (
    FeeHeadCreate, FeeHeadRead,
    ScholarshipSlabCreate, ScholarshipSlabRead
)
from app.domains.auth.models import AuthUser as User

router = APIRouter()

# ----------------------------------------------------------------------
# Fee Head Endpoints
# ----------------------------------------------------------------------

@router.get("/fee-heads", response_model=List[FeeHeadRead])
def list_fee_heads(
    is_active: Optional[bool] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all fee heads"""
    return fee_service.list_fee_heads(session, is_active)

@router.post("/fee-heads", response_model=FeeHeadRead, status_code=status.HTTP_201_CREATED)
def create_fee_head(
    data: FeeHeadCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new fee head"""
    return fee_service.create_fee_head(session, data.dict())

@router.patch("/fee-heads/{id}", response_model=FeeHeadRead)
def update_fee_head(
    id: int,
    data: dict, # Using dict for partial updates for now, could use specific schema
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a fee head"""
    return fee_service.update_fee_head(session, id, data)

@router.delete("/fee-heads/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fee_head(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a fee head"""
    fee_service.delete_fee_head(session, id)
    return None

# ----------------------------------------------------------------------
# Scholarship Slab Endpoints
# ----------------------------------------------------------------------

@router.get("/scholarship-slabs", response_model=List[ScholarshipSlabRead])
def list_scholarship_slabs(
    is_active: Optional[bool] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all scholarship slabs"""
    return fee_service.list_scholarship_slabs(session, is_active)

@router.post("/scholarship-slabs", response_model=ScholarshipSlabRead, status_code=status.HTTP_201_CREATED)
def create_scholarship_slab(
    data: ScholarshipSlabCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new scholarship slab"""
    return fee_service.create_scholarship_slab(session, data.model_dump())

@router.patch("/scholarship-slabs/{id}", response_model=ScholarshipSlabRead)
def update_scholarship_slab(
    id: int,
    data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a scholarship slab"""
    return fee_service.update_scholarship_slab(session, id, data)

@router.delete("/scholarship-slabs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scholarship_slab(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Delete a scholarship slab"""
    fee_service.delete_scholarship_slab(session, id)
    return None
