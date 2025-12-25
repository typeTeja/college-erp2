from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL

if TYPE_CHECKING:
    from .student import Student
    from .faculty import Faculty

class AssetCategory(str, Enum):
    UNIFORM = "UNIFORM"
    IT_EQUIPMENT = "IT_EQUIPMENT"
    LAB_EQUIPMENT = "LAB_EQUIPMENT"
    FURNITURE = "FURNITURE"
    STATIONERY = "STATIONERY"
    OTHERS = "OTHERS"

class AllocationStatus(str, Enum):
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    DAMAGED = "DAMAGED"
    LOST = "LOST"

class Asset(SQLModel, table=True):
    """Main inventory and asset model"""
    __tablename__ = "asset"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: AssetCategory = Field(index=True)
    description: Optional[str] = None
    qr_code: Optional[str] = Field(default=None, unique=True, index=True)
    
    unit: str = Field(default="PCS")  # PCS, METER, SET, etc.
    total_stock: int = Field(default=0)
    available_stock: int = Field(default=0)
    reorder_level: int = Field(default=5)
    
    unit_price: Decimal = Field(default=0.0, sa_column=Column(DECIMAL(10, 2)))
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    allocations: List["AssetAllocation"] = Relationship(back_populates="asset")
    maintenance_records: List["AssetMaintenance"] = Relationship(back_populates="asset")
    audit_records: List["AssetAudit"] = Relationship(back_populates="asset")

class AssetAllocation(SQLModel, table=True):
    """Tracking asset allocation to students, staff, or departments"""
    __tablename__ = "asset_allocation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    
    # Can be allocated to a student OR faculty OR department
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", index=True)
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id", index=True)
    department_name: Optional[str] = None
    
    quantity: int = Field(default=1)
    allocated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[date] = None
    returned_at: Optional[datetime] = None
    
    status: AllocationStatus = Field(default=AllocationStatus.ISSUED)
    remarks: Optional[str] = None
    
    # Relationships
    asset: Asset = Relationship(back_populates="allocations")
    student: Optional["Student"] = Relationship()
    faculty: Optional["Faculty"] = Relationship()

class AssetMaintenance(SQLModel, table=True):
    """Maintenance history for specific assets"""
    __tablename__ = "asset_maintenance"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    
    maintenance_date: date
    description: str
    cost: Decimal = Field(default=0.0, sa_column=Column(DECIMAL(10, 2)))
    performed_by: Optional[str] = None
    next_due_date: Optional[date] = None
    
    # Relationships
    asset: Asset = Relationship(back_populates="maintenance_records")

class AssetAudit(SQLModel, table=True):
    """Inventory audit records"""
    __tablename__ = "asset_audit"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    
    audit_date: datetime = Field(default_factory=datetime.utcnow)
    expected_stock: int
    actual_stock: int
    variance: int  # actual - expected
    
    audited_by: str
    remarks: Optional[str] = None
    
    # Relationships
    asset: Asset = Relationship(back_populates="audit_records")

class UniformSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    CUSTOM = "CUSTOM"

class UniformAllocation(SQLModel, table=True):
    """Specialized allocation for student uniforms"""
    __tablename__ = "uniform_allocation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    item_name: str  # Blazer, Shirt, Trousers, etc.
    size: UniformSize
    quantity: int = Field(default=1)
    
    is_paid: bool = Field(default=False)
    issued_at: Optional[datetime] = None
    status: str = Field(default="PENDING")  # PENDING, ISSUED, EXCHANGED
    
    # Relationships
    student: "Student" = Relationship()
