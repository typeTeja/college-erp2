from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL

if TYPE_CHECKING:
    from .student import Student
    from .program import Program

class FeeCategory(str, Enum):
    """Fee category types"""
    GENERAL = "GENERAL"
    MANAGEMENT = "MANAGEMENT"
    NRI = "NRI"
    SCHOLARSHIP = "SCHOLARSHIP"

class PaymentMode(str, Enum):
    """Payment modes"""
    ONLINE = "ONLINE"
    CASH = "CASH"
    CHEQUE = "CHEQUE"
    DD = "DD"
    UPI = "UPI"

class PaymentStatus(str, Enum):
    """Payment status"""
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class FeeStructure(SQLModel, table=True):
    """Fee structure for a program and academic year with scholarship slab support"""
    __tablename__ = "fee_structure"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    academic_year: str = Field(index=True)  # e.g., "2024-2025"
    year: int  # Which year of the program (1, 2, 3, 4)
    
    # Scholarship slab (A, B, C, D, or GENERAL)
    slab: str = Field(default="GENERAL", max_length=20)  # A, B, C, D, GENERAL
    
    # Fee heads (Annual amounts)
    tuition_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    library_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    lab_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    uniform_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    caution_deposit: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    digital_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    miscellaneous_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    
    # Total and installments
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    # Legacy field for backward compatibility
    category: FeeCategory = Field(default=FeeCategory.GENERAL)
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))  # Same as total_annual_fee
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    program: "Program" = Relationship(back_populates="fee_structures")
    components: List["FeeComponent"] = Relationship(back_populates="fee_structure", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    installments: List["FeeInstallment"] = Relationship(back_populates="fee_structure", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    student_fees: List["StudentFee"] = Relationship(back_populates="fee_structure")

class FeeComponent(SQLModel, table=True):
    """Individual fee components (Tuition, Library, Lab, etc.)"""
    __tablename__ = "fee_component"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    fee_head_id: Optional[int] = Field(default=None, foreign_key="fee_head.id", index=True)  # Link to master fee head
    name: str  # e.g., "Tuition Fee", "Library Fee"
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    is_refundable: bool = Field(default=False)
    
    # Relationships
    fee_structure: "FeeStructure" = Relationship(back_populates="components")

class FeeInstallment(SQLModel, table=True):
    """Installment schedule for a fee structure (template)"""
    __tablename__ = "fee_installment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    installment_number: int  # 1, 2, 3, etc.
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    description: Optional[str] = None  # e.g., "First Installment"
    
    # Relationships
    fee_structure: "FeeStructure" = Relationship(back_populates="installments")

class StudentFee(SQLModel, table=True):
    """Links a student to their fee structure for an academic year with detailed tracking"""
    __tablename__ = "student_fee"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    fee_structure_id: int = Field(foreign_key="fee_structure.id", index=True)
    academic_year: str = Field(index=True)
    
    # Fee amounts
    total_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    concession_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    net_annual_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))  # After concession
    
    # Installment configuration
    number_of_installments: int = Field(default=4)
    installment_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    # Fee heads breakdown (JSON for head-wise clearance)
    # Example: {"tuition": {"amount": 50000, "cleared": 25000, "pending": 25000}}
    fee_heads: Optional[str] = None  # JSON
    
    # Old dues from previous years
    old_dues: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    
    # Totals
    total_paid: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    total_pending: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    # Legacy fields for backward compatibility
    total_fee: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))  # Same as total_annual_fee
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))  # Same as total_paid
    
    is_blocked: bool = Field(default=False)  # Block exam/promotion if dues pending
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    fee_structure: "FeeStructure" = Relationship(back_populates="student_fees")
    payments: List["FeePayment"] = Relationship(back_populates="student_fee", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    concessions: List["FeeConcession"] = Relationship(back_populates="student_fee", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    fines: List["FeeFine"] = Relationship(back_populates="student_fee", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    student_installments: List["StudentFeeInstallment"] = Relationship(back_populates="student_fee", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class FeePayment(SQLModel, table=True):
    """Individual payment transactions"""
    __tablename__ = "fee_payment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    payment_mode: PaymentMode
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    
    # Payment gateway details
    transaction_id: Optional[str] = Field(default=None, index=True)  # Easebuzz transaction ID
    gateway_response: Optional[str] = None  # JSON response from gateway
    
    # Offline payment details
    reference_number: Optional[str] = None  # Cheque/DD number
    bank_name: Optional[str] = None
    
    payment_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    remarks: Optional[str] = None
    
    # Relationships
    student_fee: "StudentFee" = Relationship(back_populates="payments")

class FeeConcession(SQLModel, table=True):
    """Fee concessions/scholarships applied to students"""
    __tablename__ = "fee_concession"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    
    concession_type: str  # e.g., "Merit Scholarship", "Sports Quota"
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    percentage: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(5, 2)))
    
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    remarks: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student_fee: "StudentFee" = Relationship(back_populates="concessions")

class FeeFine(SQLModel, table=True):
    """Late payment fines"""
    __tablename__ = "fee_fine"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    
    installment_number: int
    fine_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    reason: str  # e.g., "Late payment for Installment 1"
    
    waived: bool = Field(default=False)
    waived_by: Optional[str] = None
    waived_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student_fee: "StudentFee" = Relationship(back_populates="fines")

class StudentFeeInstallment(SQLModel, table=True):
    """Individual student installments with fine tracking"""
    __tablename__ = "student_fee_installment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    student_fee_id: int = Field(foreign_key="student_fee.id", index=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    installment_number: int  # 1, 2, 3, 4
    
    # Amount details
    amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    due_date: date
    
    # Additional fees for this installment
    individual_fee_heads: Optional[str] = None  # JSON: [{"head": "Exam Fee", "amount": 500}]
    bulk_fee_heads: Optional[str] = None  # JSON: [{"head": "Event Fee", "amount": 200}]
    supply_exam_fee: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    old_dues_included: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    
    # Total for this installment
    total_amount: Decimal = Field(sa_column=Column(DECIMAL(10, 2)))
    
    # Payment tracking
    paid_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    payment_status: str = Field(default="pending")  # pending, partial, paid, overdue
    payment_date: Optional[date] = None
    
    # Fine management
    fine_amount: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(10, 2)))
    fine_waived: bool = Field(default=False)
    fine_waived_by: Optional[int] = Field(default=None, foreign_key="user.id")
    fine_waived_date: Optional[datetime] = None
    fine_waiver_reason: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student_fee: "StudentFee" = Relationship(back_populates="student_installments")
