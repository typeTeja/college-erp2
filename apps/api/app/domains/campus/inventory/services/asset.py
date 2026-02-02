from typing import List, Optional, Dict
from datetime import datetime
from sqlmodel import Session, select, func
from fastapi import HTTPException

from ..models.asset import Asset, AssetAllocation, AssetAudit, UniformAllocation, AllocationStatus

class InventoryService:
    """Service for managing Physical Assets and Stock (Identity Owner)"""
    
    @staticmethod
    def create_asset(session: Session, asset_data: Dict) -> Asset:
        """Create a new asset in inventory"""
        asset = Asset.model_validate(asset_data)
        session.add(asset)
        session.commit()
        session.refresh(asset)
        return asset

    @staticmethod
    def get_assets(
        session: Session,
        category: Optional[str] = None,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Asset]:
        """List all assets with filtering"""
        statement = select(Asset)
        if category:
            statement = statement.where(Asset.category == category)
        if query:
            statement = statement.where(Asset.name.contains(query))
        
        return session.exec(statement.offset(skip).limit(limit)).all()

    @staticmethod
    def allocate_asset(session: Session, allocation_data: Dict) -> AssetAllocation:
        """Issue an asset to a student, faculty or department"""
        asset = session.get(Asset, allocation_data["asset_id"])
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        quantity = allocation_data.get("quantity", 1)
        if asset.available_stock < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        # Update stock
        asset.available_stock -= quantity
        asset.updated_at = datetime.utcnow()
        session.add(asset)
        
        allocation = AssetAllocation(**allocation_data)
        session.add(allocation)
        session.commit()
        session.refresh(allocation)
        return allocation

    @staticmethod
    def return_asset(
        session: Session,
        allocation_id: int,
        status: AllocationStatus = AllocationStatus.RETURNED
    ) -> AssetAllocation:
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

    @staticmethod
    def perform_audit(session: Session, audit_data: Dict) -> AssetAudit:
        """Record an inventory audit for an asset"""
        asset = session.get(Asset, audit_data["asset_id"])
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        
        actual_stock = audit_data["actual_stock"]
        expected_stock = asset.available_stock
        variance = actual_stock - expected_stock
        
        audit = AssetAudit(
            **audit_data,
            expected_stock=expected_stock,
            variance=variance
        )
        
        # Update asset available stock to actual count
        asset.available_stock = actual_stock
        asset.updated_at = datetime.utcnow()
        session.add(asset)
        
        session.add(audit)
        session.commit()
        session.refresh(audit)
        return audit

    @staticmethod
    def issue_uniform(session: Session, uniform_data: Dict) -> UniformAllocation:
        """Allocate a uniform to a student"""
        uniform = UniformAllocation(
            **uniform_data,
            issued_at=datetime.utcnow(),
            status="ISSUED"
        )
        session.add(uniform)
        session.commit()
        session.refresh(uniform)
        return uniform

inventory_service = InventoryService()
