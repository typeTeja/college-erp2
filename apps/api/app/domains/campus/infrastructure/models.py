"""
Infrastructure Domain Models

Facility and maintenance models for campus infrastructure management.
"""

from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL
from app.shared.enums import RoomType


if TYPE_CHECKING:
    from app.models.department import Department


# ======================================================================
# Facility Models
# ======================================================================

class MasterClassroom(SQLModel, table=True):
    """Classroom Management - Facility Structure"""
    __tablename__ = "master_classroom"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Room 101", "Computer Lab 1"
    code: str = Field(unique=True, index=True)
    
    room_type: RoomType = Field(default=RoomType.CLASSROOM)
    building: Optional[str] = None
    floor: Optional[int] = None
    
    capacity: int = Field(default=40)
    
    has_projector: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    has_smart_board: bool = Field(default=False)
    has_computer: bool = Field(default=False)
    
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ======================================================================
# Maintenance Models
# ======================================================================

class AssetMaintenance(SQLModel, table=True):
    """Maintenance history for specific assets - Maintenance Lifecycle Owner"""
    __tablename__ = "asset_maintenance"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    
    maintenance_date: date
    description: str
    cost: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    performed_by: Optional[str] = None
    next_due_date: Optional[date] = None
    
    # Relationships
    # Reference to Asset (owned by Inventory)
    asset: "Asset" = Relationship(
        back_populates="maintenance_records",
        sa_relationship_kwargs={"primaryjoin": "AssetMaintenance.asset_id == Asset.id"}
    )
