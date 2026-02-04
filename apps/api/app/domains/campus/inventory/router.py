from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from pydantic import BaseModel
from decimal import Decimal

from app.api.deps import get_session, get_current_active_superuser
from app.models import User
from ..models import Asset, AssetAllocation, AssetAudit, UniformAllocation, AssetCategory, AllocationStatus, UniformSize
from .services import inventory_service
from app.shared.enums import AllocationStatus, AssetCategory, UniformSize


router = APIRouter(tags=["Inventory & Assets"])

# Schemas
class AssetCreate(BaseModel):
    name: str
    category: AssetCategory
    description: Optional[str] = None
    qr_code: Optional[str] = None
    unit: str = "PCS"
    total_stock: int
    unit_price: Decimal = Decimal("0.00")

class AssetAllocationCreate(BaseModel):
    asset_id: int
    student_id: Optional[int] = None
    faculty_id: Optional[int] = None
    department_name: Optional[str] = None
    quantity: int = 1
    remarks: Optional[str] = None

class AssetAuditCreate(BaseModel):
    asset_id: int
    actual_stock: int
    audited_by: str
    remarks: Optional[str] = None

class UniformAllocationCreate(BaseModel):
    student_id: int
    item_name: str
    size: UniformSize
    quantity: int = 1

# ============================================================================
# Asset Management Endpoints
# ============================================================================

@router.post("/assets", response_model=Asset)
def create_asset(
    *,
    session: Session = Depends(get_session),
    asset_data: AssetCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Add a new asset to the institution's inventory"""
    data = asset_data.model_dump()
    data["available_stock"] = asset_data.total_stock
    return inventory_service.create_asset(session, data)

@router.get("/assets", response_model=List[Asset])
def list_assets(
    *,
    session: Session = Depends(get_session),
    category: Optional[AssetCategory] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100)
):
    """List assets with category filtering and search"""
    return inventory_service.get_assets(session, category=category, query=search, limit=limit)

# ============================================================================
# Allocation Endpoints
# ============================================================================

@router.post("/allocate", response_model=AssetAllocation)
def allocate_asset(
    *,
    session: Session = Depends(get_session),
    allocation_data: AssetAllocationCreate
):
    """Issue an asset to a person or department"""
    return inventory_service.allocate_asset(session, allocation_data.model_dump())

@router.put("/return/{allocation_id}", response_model=AssetAllocation)
def return_asset(
    allocation_id: int,
    status: AllocationStatus = AllocationStatus.RETURNED,
    session: Session = Depends(get_session)
):
    """Record the return of an issued asset"""
    return inventory_service.return_asset(session, allocation_id, status)

# ============================================================================
# Audit Endpoints
# ============================================================================

@router.post("/audit", response_model=AssetAudit)
def perform_audit(
    *,
    session: Session = Depends(get_session),
    audit_data: AssetAuditCreate
):
    """Perform a physical stock audit for an asset"""
    return inventory_service.perform_audit(session, audit_data.model_dump())

# ============================================================================
# Uniform Endpoints
# ============================================================================

@router.post("/uniforms", response_model=UniformAllocation)
def issue_uniform(
    *,
    session: Session = Depends(get_session),
    uniform_data: UniformAllocationCreate
):
    """Record uniform issuance to a student"""
    return inventory_service.issue_uniform(session, uniform_data.model_dump())

