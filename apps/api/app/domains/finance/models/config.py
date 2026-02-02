from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, JSON

if TYPE_CHECKING:
    from app.domains.admission.models import EntranceExamResult
    from app.domains.admission.models import AdmissionSettings

class FeeHead(SQLModel, table=True):
    """Fee Heads Management - Types of fees (Tuition, Lab, etc.)"""
    __tablename__ = "fee_head"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    is_refundable: bool = Field(default=False)
    is_recurring: bool = Field(default=True)
    is_mandatory: bool = Field(default=True)
    
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class InstallmentPlan(SQLModel, table=True):
    """Installment Plan Management - Payment schedules"""
    __tablename__ = "installment_plan"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    number_of_installments: int = Field(default=4)
    installment_schedule: List[dict] = Field(default=[], sa_column=Column(JSON))
    
    late_fee_per_day: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    grace_period_days: int = Field(default=7)
    max_late_fee: Decimal = Field(default=Decimal("500.00"), sa_column=Column(DECIMAL(10, 2)))
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ScholarshipSlab(SQLModel, table=True):
    """Scholarship Slab Management - Merit-based discounts"""
    __tablename__ = "scholarship_slab"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    min_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    max_percentage: Decimal = Field(default=Decimal("100.00"), sa_column=Column(DECIMAL(5, 2)))
    
    discount_type: str = Field(default="PERCENTAGE")
    discount_value: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    max_discount_amount: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(10, 2)))
    
    applicable_fee_heads: List[str] = Field(default=[], sa_column=Column(JSON))
    
    academic_year_id: Optional[int] = Field(default=None, foreign_key="academic_year.id")
    program_id: Optional[int] = Field(default=None, foreign_key="program.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    results: List["EntranceExamResult"] = Relationship(back_populates="scholarship_slab")
