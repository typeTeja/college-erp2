"""
Finance Domain Models - Fee Configuration

Models for fee heads, installment plans, and scholarship slabs.
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, JSON

if TYPE_CHECKING:
    from app.domains.admission.models import EntranceExamResult
    from app.domains.admission.models import AdmissionSettings


class FeeHead(SQLModel, table=True):
    """
    Fee Heads Management - Types of fees (Tuition, Lab, etc.)
    """
    __tablename__ = "fee_head"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # Tuition Fee, Lab Fee, etc.
    code: str = Field(unique=True, index=True)  # TF, LF, etc.
    description: Optional[str] = None
    category: str = Field(default="ACADEMIC")  # ACADEMIC, HOSTEL, TRANSPORT, etc.
    is_mandatory: bool = Field(default=True)
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class InstallmentPlan(SQLModel, table=True):
    """
    Installment Plan Management - Payment schedules
    """
    __tablename__ = "installment_plan"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # "3 Installments", "Semester-wise"
    code: str = Field(unique=True, index=True)  # "3INST", "SEMWISE"
    description: Optional[str] = None
    number_of_installments: int = Field(ge=1, le=12)
    
    # JSON structure: [{"installment_no": 1, "percentage": 40, "due_days": 0}, ...]
    installment_config: List[dict] = Field(default=[], sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ScholarshipSlab(SQLModel, table=True):
    """
    Scholarship Slab Management - Merit-based discounts
    """
    __tablename__ = "scholarship_slab"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # "Gold", "Silver", "Bronze"
    code: str = Field(unique=True, index=True)  # "GOLD", "SILVER", "BRONZE"
    description: Optional[str] = None
    
    # Eligibility criteria
    min_rank: Optional[int] = None
    max_rank: Optional[int] = None
    min_percentage: Optional[float] = None
    
    # Discount
    discount_type: str = Field(default="PERCENTAGE")  # PERCENTAGE, FIXED_AMOUNT
    discount_value: float  # 50 (for 50%) or 10000 (for ₹10,000)
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    results: List["EntranceExamResult"] = Relationship(back_populates="scholarship_slab")
