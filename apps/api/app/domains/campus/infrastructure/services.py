from typing import List, Optional, Dict
from datetime import datetime, date
from sqlmodel import Session, select, func
from fastapi import HTTPException

from ..models.maintenance import AssetMaintenance
from .models import MasterClassroom, Designation

class InfrastructureService:
    """Service for facility lifecycle and maintenance management (Facility Owner)"""
    
    @staticmethod
    def record_maintenance(session: Session, maintenance_data: Dict) -> AssetMaintenance:
        """Record a maintenance activity for an asset"""
        # Note: asset_id is the foreign key to the Asset model in Inventory
        maintenance = AssetMaintenance(**maintenance_data)
        session.add(maintenance)
        session.commit()
        session.refresh(maintenance)
        return maintenance

    @staticmethod
    def get_maintenance_history(
        session: Session,
        asset_id: int
    ) -> List[AssetMaintenance]:
        """Get maintenance history for a specific asset"""
        stmt = select(AssetMaintenance).where(AssetMaintenance.asset_id == asset_id).order_by(AssetMaintenance.maintenance_date.desc())
        return session.exec(stmt).all()

    @staticmethod
    def create_classroom(session: Session, classroom_data: Dict) -> MasterClassroom:
        """Add a new classroom to the facility master"""
        classroom = MasterClassroom.model_validate(classroom_data)
        session.add(classroom)
        session.commit()
        session.refresh(classroom)
        return classroom

    @staticmethod
    def get_classrooms(
        session: Session,
        building: Optional[str] = None,
        is_active: bool = True
    ) -> List[MasterClassroom]:
        """List classrooms with filtering"""
        stmt = select(MasterClassroom).where(MasterClassroom.is_active == is_active)
        if building:
            stmt = stmt.where(MasterClassroom.building == building)
        return session.exec(stmt).all()

    @staticmethod
    def create_designation(session: Session, designation_data: Dict) -> Designation:
        """Add a new designation to the system master"""
        designation = Designation.model_validate(designation_data)
        session.add(designation)
        session.commit()
        session.refresh(designation)
        return designation

infrastructure_service = InfrastructureService()

