from typing import TYPE_CHECKING, Optional
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL

if TYPE_CHECKING:
    # Use string references for sibling relations to avoid circular/sibling imports
    pass

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
