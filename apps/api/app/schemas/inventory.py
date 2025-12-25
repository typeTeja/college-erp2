from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel
from app.models.inventory import AssetCategory, AllocationStatus, UniformSize

# Asset Schemas
class AssetBase(BaseModel):
    name: str
    category: AssetCategory
    description: Optional[str] = None
    qr_code: Optional[str] = None
    unit: str = "PCS"
    total_stock: int = 0
    available_stock: int = 0
    reorder_level: int = 5
    unit_price: Decimal = Decimal("0.00")

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[AssetCategory] = None
    description: Optional[str] = None
    qr_code: Optional[str] = None
    unit: Optional[str] = None
    total_stock: Optional[int] = None
    available_stock: Optional[int] = None
    reorder_level: Optional[int] = None
    unit_price: Optional[Decimal] = None

class AssetRead(AssetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Allocation Schemas
class AssetAllocationBase(BaseModel):
    asset_id: int
    student_id: Optional[int] = None
    faculty_id: Optional[int] = None
    department_name: Optional[str] = None
    quantity: int = 1
    due_date: Optional[date] = None
    remarks: Optional[str] = None

class AssetAllocationCreate(AssetAllocationBase):
    pass

class AssetAllocationRead(AssetAllocationBase):
    id: int
    allocated_at: datetime
    returned_at: Optional[datetime] = None
    status: AllocationStatus

    class Config:
        from_attributes = True

# Maintenance Schemas
class AssetMaintenanceBase(BaseModel):
    asset_id: int
    maintenance_date: date
    description: str
    cost: Decimal = Decimal("0.00")
    performed_by: Optional[str] = None
    next_due_date: Optional[date] = None

class AssetMaintenanceCreate(AssetMaintenanceBase):
    pass

class AssetMaintenanceRead(AssetMaintenanceBase):
    id: int

    class Config:
        from_attributes = True

# Audit Schemas
class AssetAuditBase(BaseModel):
    asset_id: int
    actual_stock: int
    audited_by: str
    remarks: Optional[str] = None

class AssetAuditCreate(AssetAuditBase):
    pass

class AssetAuditRead(AssetAuditBase):
    id: int
    audit_date: datetime
    expected_stock: int
    variance: int

    class Config:
        from_attributes = True

# Uniform Allocation Schemas
class UniformAllocationBase(BaseModel):
    student_id: int
    item_name: str
    size: UniformSize
    quantity: int = 1
    is_paid: bool = False

class UniformAllocationCreate(UniformAllocationBase):
    pass

class UniformAllocationRead(UniformAllocationBase):
    id: int
    issued_at: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True
