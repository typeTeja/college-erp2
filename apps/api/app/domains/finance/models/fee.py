from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL
from app.shared.enums import FeeCategory, PaymentMode, PaymentStatus


if TYPE_CHECKING:
    from app.models import Student
    from app.models.program import Program


class FeeStructure(SQLModel, table=True):
    __tablename__ = "fee_structure"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    academic_year: str = Field(index=True)
    year: int
    slab: str = Field(default="GENERAL", max_length=20)
    
    tuition_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    library_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    lab_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    uniform_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    caution_deposit: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    digital_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    miscellaneous_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    category: FeeCategory = Field(default=FeeCategory.GENERAL)
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    program: "Program" = Relationship(back_populates="fee_structures")
    components: List["FeeComponent"] = Relationship(back_populates="fee_structure")
    installments: List["FeeInstallment"] = Relationship(back_populates="fee_structure")
    student_fees: List["StudentFee"] = Relationship(back_populates="fee_structure")

class FeeComponent(SQLModel, table=True):
    __tablename__ = "fee_component"
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    fee_head_id: Optional[int] = Field(default=None, foreign_key="fee_head.id", index=True)
    name: str
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    is_refundable: bool = Field(default=False)
    fee_structure: "FeeStructure" = Relationship(back_populates="components")

class FeeInstallment(SQLModel, table=True):
    __tablename__ = "fee_installment"
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    installment_number: int
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    description: Optional[str] = None
    fee_structure: "FeeStructure" = Relationship(back_populates="installments")

class StudentFee(SQLModel, table=True):
    __tablename__ = "student_fee"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    academic_year: str = Field(index=True)
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    concession_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    net_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    fee_heads: Optional[str] = None
    old_dues: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_paid: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_pending: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    total_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    is_blocked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    student: "Student" = Relationship()
    fee_structure: "FeeStructure" = Relationship(back_populates="student_fees")
    payments: List["FeePayment"] = Relationship(back_populates="student_fee")
    concessions: List["FeeConcession"] = Relationship(back_populates="student_fee")
    fines: List["FeeFine"] = Relationship(back_populates="student_fee")
    student_installments: List["StudentFeeInstallment"] = Relationship(back_populates="student_fee")

class FeePayment(SQLModel, table=True):
    __tablename__ = "fee_payment"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    payment_mode: PaymentMode
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    transaction_id: Optional[str] = Field(default=None, index=True)
    gateway_response: Optional[str] = None
    reference_number: Optional[str] = None
    bank_name: Optional[str] = None
    payment_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    remarks: Optional[str] = None
    student_fee: "StudentFee" = Relationship(back_populates="payments")

class FeeConcession(SQLModel, table=True):
    __tablename__ = "fee_concession"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    concession_type: str
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    percentage: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(5, 2)))
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="concessions")

class FeeFine(SQLModel, table=True):
    __tablename__ = "fee_fine"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    installment_number: int
    fine_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    reason: str
    waived: bool = Field(default=False)
    waived_by: Optional[str] = None
    waived_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="fines")

class StudentFeeInstallment(SQLModel, table=True):
    __tablename__ = "student_fee_installment"
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    installment_number: int
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    individual_fee_heads: Optional[str] = None
    bulk_fee_heads: Optional[str] = None
    supply_exam_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    old_dues_included: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    payment_status: str = Field(default="pending")
    payment_date: Optional[date] = None
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    fine_waived: bool = Field(default=False)
    fine_waived_by: Optional[int] = Field(default=None, foreign_key="user.id")
    fine_waived_date: Optional[datetime] = None
    fine_waiver_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    student_fee: "StudentFee" = Relationship(back_populates="student_installments")
