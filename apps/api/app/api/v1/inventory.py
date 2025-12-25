from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from app.api import deps
from app.models.inventory import Asset, AssetAllocation, AssetMaintenance, AssetAudit, UniformAllocation, AllocationStatus
from app.schemas.inventory import (
    AssetCreate, AssetRead, AssetUpdate,
    AssetAllocationCreate, AssetAllocationRead,
    AssetMaintenanceCreate, AssetMaintenanceRead,
    AssetAuditCreate, AssetAuditRead,
    UniformAllocationCreate, UniformAllocationRead
)
from datetime import datetime

router = APIRouter()

# Assets
@router.post("/assets", response_model=AssetRead)
def create_asset(
    *,
    session: Session = Depends(deps.get_session),
    asset_in: AssetCreate
):
    """Create a new asset in inventory"""
    asset = Asset.model_validate(asset_in)
    session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset

@router.get("/assets", response_model=List[AssetRead])
def get_assets(
    *,
    session: Session = Depends(deps.get_session),
    category: Optional[str] = None,
    query: Optional[str] = None,
    offset: int = 0,
    limit: int = 100
):
    """List all assets with filtering"""
    statement = select(Asset)
    if category:
        statement = statement.where(Asset.category == category)
    if query:
        statement = statement.where(Asset.name.contains(query))
    
    assets = session.exec(statement.offset(offset).limit(limit)).all()
    return assets

@router.get("/assets/{asset_id}", response_model=AssetRead)
def get_asset(
    asset_id: int,
    session: Session = Depends(deps.get_session)
):
    """Get single asset details"""
    asset = session.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# Allocations
@router.post("/allocate", response_model=AssetAllocationRead)
def allocate_asset(
    *,
    session: Session = Depends(deps.get_session),
    allocation_in: AssetAllocationCreate
):
    """Issue an asset to a student, faculty or department"""
    asset = session.get(Asset, allocation_in.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    if asset.available_stock < allocation_in.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # Update stock
    asset.available_stock -= allocation_in.quantity
    asset.updated_at = datetime.utcnow()
    session.add(asset)
    
    allocation = AssetAllocation(**allocation_in.dict())
    session.add(allocation)
    session.commit()
    session.refresh(allocation)
    return allocation

@router.put("/return/{allocation_id}", response_model=AssetAllocationRead)
def return_asset(
    allocation_id: int,
    status: AllocationStatus = AllocationStatus.RETURNED,
    session: Session = Depends(deps.get_session)
):
    """Record return of an allocated asset"""
    allocation = session.get(AssetAllocation, allocation_id)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation record not found")
    
    if allocation.status != AllocationStatus.ISSUED:
        raise HTTPException(status_code=400, detail="Asset already returned or lost")
    
    asset = allocation.asset
    if status == AllocationStatus.RETURNED:
        asset.available_stock += allocation.quantity
    
    asset.updated_at = datetime.utcnow()
    session.add(asset)
    
    allocation.returned_at = datetime.utcnow()
    allocation.status = status
    session.add(allocation)
    session.commit()
    session.refresh(allocation)
    return allocation

# Audits
@router.post("/audit", response_model=AssetAuditRead)
def perform_audit(
    *,
    session: Session = Depends(deps.get_session),
    audit_in: AssetAuditCreate
):
    """Record an inventory audit for an asset"""
    asset = session.get(Asset, audit_in.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    expected_stock = asset.available_stock
    variance = audit_in.actual_stock - expected_stock
    
    audit = AssetAudit(
        **audit_in.dict(),
        expected_stock=expected_stock,
        variance=variance
    )
    
    # Update asset available stock to actual count
    asset.available_stock = audit_in.actual_stock
    asset.updated_at = datetime.utcnow()
    session.add(asset)
    
    session.add(audit)
    session.commit()
    session.refresh(audit)
    return audit

# Uniforms
@router.post("/uniforms", response_model=UniformAllocationRead)
def issue_uniform(
    *,
    session: Session = Depends(deps.get_session),
    uniform_in: UniformAllocationCreate
):
    """Allocate a uniform to a student"""
    uniform = UniformAllocation(
        **uniform_in.dict(),
        issued_at=datetime.utcnow(),
        status="ISSUED"
    )
    session.add(uniform)
    session.commit()
    session.refresh(uniform)
    return uniform

@router.get("/uniforms/student/{student_id}", response_model=List[UniformAllocationRead])
def get_student_uniforms(
    student_id: int,
    session: Session = Depends(deps.get_session)
):
    """Get all uniform allocations for a specific student"""
    uniforms = session.exec(select(UniformAllocation).where(UniformAllocation.student_id == student_id)).all()
    return uniforms
