from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, date
from decimal import Decimal

from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.fee import (
    FeeStructure,
    FeeComponent,
    FeeInstallment,
    StudentFee,
    FeePayment,
    FeeConcession,
    FeeFine,
    PaymentStatus,
)
from app.models.student import Student
from app.schemas.fee import (
    FeeStructureCreate,
    FeeStructureResponse,
    StudentFeeCreate,
    StudentFeeResponse,
    StudentFeeSummary,
    FeePaymentCreate,
    FeePaymentResponse,
    PaymentInitiateRequest,
    PaymentInitiateResponse,
    FeeConcessionCreate,
    FeeConcessionResponse,
    FeeFineCreate,
    FeeFineResponse,
    FeeDefaulter,
)

router = APIRouter()

# ============================================================================
# Fee Structure Management
# ============================================================================

@router.post("/structures", response_model=FeeStructureResponse, status_code=status.HTTP_201_CREATED)
def create_fee_structure(
    data: FeeStructureCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new fee structure with components and installments"""
    # Calculate total amount from components
    total_amount = sum(comp.amount for comp in data.components)
    
    # Create fee structure
    fee_structure = FeeStructure(
        program_id=data.program_id,
        academic_year=data.academic_year,
        year=data.year,
        category=data.category,
        total_amount=total_amount
    )
    session.add(fee_structure)
    session.flush()  # Get the ID
    
    # Create components
    for comp_data in data.components:
        component = FeeComponent(
            fee_structure_id=fee_structure.id,
            name=comp_data.name,
            amount=comp_data.amount,
            is_refundable=comp_data.is_refundable
        )
        session.add(component)
    
    # Create installments
    for inst_data in data.installments:
        installment = FeeInstallment(
            fee_structure_id=fee_structure.id,
            installment_number=inst_data.installment_number,
            amount=inst_data.amount,
            due_date=inst_data.due_date
        )
        session.add(installment)
    
    session.commit()
    session.refresh(fee_structure)
    
    return fee_structure

@router.get("/structures", response_model=List[FeeStructureResponse])
def get_fee_structures(
    program_id: int = None,
    academic_year: str = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all fee structures with optional filters"""
    query = select(FeeStructure)
    
    if program_id:
        query = query.where(FeeStructure.program_id == program_id)
    if academic_year:
        query = query.where(FeeStructure.academic_year == academic_year)
    
    structures = session.exec(query).all()
    return structures

@router.get("/structures/{structure_id}", response_model=FeeStructureResponse)
def get_fee_structure(
    structure_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific fee structure by ID"""
    structure = session.get(FeeStructure, structure_id)
    if not structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return structure

# ============================================================================
# Student Fee Management
# ============================================================================

@router.post("/student-fees", response_model=StudentFeeResponse, status_code=status.HTTP_201_CREATED)
def assign_fee_to_student(
    data: StudentFeeCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Assign a fee structure to a student"""
    # Verify student exists
    student = session.get(Student, data.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify fee structure exists
    fee_structure = session.get(FeeStructure, data.fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    
    # Create student fee record
    student_fee = StudentFee(
        student_id=data.student_id,
        fee_structure_id=data.fee_structure_id,
        academic_year=data.academic_year,
        total_fee=fee_structure.total_amount
    )
    session.add(student_fee)
    session.commit()
    session.refresh(student_fee)
    
    return student_fee

@router.get("/student/{student_id}", response_model=StudentFeeSummary)
def get_student_fee_summary(
    student_id: int,
    academic_year: str = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get detailed fee summary for a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get student fee record
    query = select(StudentFee).where(StudentFee.student_id == student_id)
    if academic_year:
        query = query.where(StudentFee.academic_year == academic_year)
    
    student_fee = session.exec(query).first()
    if not student_fee:
        raise HTTPException(status_code=404, detail="Fee record not found for this student")
    
    # Calculate balance
    balance = (
        student_fee.total_fee 
        - student_fee.concession_amount 
        + student_fee.fine_amount 
        - student_fee.paid_amount
    )
    
    # Get installment details
    fee_structure = session.get(FeeStructure, student_fee.fee_structure_id)
    installments = []
    for inst in fee_structure.installments:
        installments.append({
            "installment_number": inst.installment_number,
            "amount": float(inst.amount),
            "due_date": inst.due_date.isoformat(),
            "status": "paid" if student_fee.paid_amount >= inst.amount else "pending"
        })
    
    # Get payment history
    payments = []
    for payment in student_fee.payments:
        payments.append({
            "id": payment.id,
            "amount": float(payment.amount),
            "payment_mode": payment.payment_mode,
            "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
            "status": payment.payment_status
        })
    
    return StudentFeeSummary(
        student_id=student.id,
        student_name=student.name,
        admission_number=student.admission_number,
        academic_year=student_fee.academic_year,
        total_fee=student_fee.total_fee,
        concession_amount=student_fee.concession_amount,
        fine_amount=student_fee.fine_amount,
        paid_amount=student_fee.paid_amount,
        balance=balance,
        is_blocked=student_fee.is_blocked,
        installments=installments,
        payments=payments
    )

# ============================================================================
# Payment Management
# ============================================================================

@router.post("/payments", response_model=FeePaymentResponse, status_code=status.HTTP_201_CREATED)
def record_fee_payment(
    data: FeePaymentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Record a fee payment (offline or manual entry)"""
    student_fee = session.get(StudentFee, data.student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee record not found")
    
    # Create payment record
    payment = FeePayment(
        student_fee_id=data.student_fee_id,
        amount=data.amount,
        payment_mode=data.payment_mode,
        payment_status=PaymentStatus.SUCCESS,
        reference_number=data.reference_number,
        bank_name=data.bank_name,
        payment_date=datetime.utcnow(),
        remarks=data.remarks
    )
    session.add(payment)
    
    # Update student fee paid amount
    student_fee.paid_amount += data.amount
    student_fee.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(payment)
    
    return payment

@router.post("/payments/initiate", response_model=PaymentInitiateResponse)
def initiate_online_payment(
    data: PaymentInitiateRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Initiate online payment via Easebuzz"""
    student_fee = session.get(StudentFee, data.student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee record not found")
    
    # Create pending payment record
    transaction_id = f"TXN{student_fee.student_id}{int(datetime.utcnow().timestamp())}"
    
    payment = FeePayment(
        student_fee_id=data.student_fee_id,
        amount=data.amount,
        payment_mode="ONLINE",
        payment_status=PaymentStatus.PENDING,
        transaction_id=transaction_id
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)
    
    # TODO: Integrate with Easebuzz API to get actual payment URL
    payment_url = f"https://payment-gateway.example.com/pay?txn={transaction_id}"
    
    return PaymentInitiateResponse(
        payment_id=payment.id,
        transaction_id=transaction_id,
        payment_url=payment_url,
        amount=data.amount
    )

@router.post("/payments/webhook")
def payment_webhook(
    transaction_id: str,
    status: str,
    amount: float,
    session: Session = Depends(get_session)
):
    """Handle payment gateway webhook"""
    # Find payment by transaction ID
    payment = session.exec(
        select(FeePayment).where(FeePayment.transaction_id == transaction_id)
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Update payment status
    if status.upper() == "SUCCESS":
        payment.payment_status = PaymentStatus.SUCCESS
        payment.payment_date = datetime.utcnow()
        
        # Update student fee
        student_fee = session.get(StudentFee, payment.student_fee_id)
        student_fee.paid_amount += payment.amount
        student_fee.updated_at = datetime.utcnow()
    else:
        payment.payment_status = PaymentStatus.FAILED
    
    session.commit()
    
    return {"message": "Webhook processed successfully"}

# ============================================================================
# Concession Management
# ============================================================================

@router.post("/concessions", response_model=FeeConcessionResponse, status_code=status.HTTP_201_CREATED)
def apply_fee_concession(
    data: FeeConcessionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Apply a fee concession to a student"""
    student_fee = session.get(StudentFee, data.student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee record not found")
    
    # Calculate concession amount
    if data.amount:
        concession_amount = data.amount
    elif data.percentage:
        concession_amount = (student_fee.total_fee * data.percentage) / 100
    else:
        raise HTTPException(status_code=400, detail="Either amount or percentage must be provided")
    
    # Create concession record
    concession = FeeConcession(
        student_fee_id=data.student_fee_id,
        concession_type=data.concession_type,
        amount=concession_amount,
        percentage=data.percentage,
        approved_by=current_user.username,
        approved_at=datetime.utcnow(),
        remarks=data.remarks
    )
    session.add(concession)
    
    # Update student fee
    student_fee.concession_amount += concession_amount
    student_fee.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(concession)
    
    return concession

# ============================================================================
# Fine Management
# ============================================================================

@router.post("/fines", response_model=FeeFineResponse, status_code=status.HTTP_201_CREATED)
def apply_fee_fine(
    data: FeeFineCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Apply a late payment fine"""
    student_fee = session.get(StudentFee, data.student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee record not found")
    
    # Create fine record
    fine = FeeFine(
        student_fee_id=data.student_fee_id,
        installment_number=data.installment_number,
        fine_amount=data.fine_amount,
        reason=data.reason
    )
    session.add(fine)
    
    # Update student fee
    student_fee.fine_amount += data.fine_amount
    student_fee.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(fine)
    
    return fine

# ============================================================================
# Defaulters Report
# ============================================================================

@router.get("/defaulters", response_model=List[FeeDefaulter])
def get_fee_defaulters(
    academic_year: str = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get list of students with pending fee payments"""
    query = select(StudentFee).where(
        StudentFee.paid_amount < (StudentFee.total_fee - StudentFee.concession_amount + StudentFee.fine_amount)
    )
    
    if academic_year:
        query = query.where(StudentFee.academic_year == academic_year)
    
    defaulters = []
    for student_fee in session.exec(query).all():
        student = session.get(Student, student_fee.student_id)
        total_due = (
            student_fee.total_fee 
            - student_fee.concession_amount 
            + student_fee.fine_amount 
            - student_fee.paid_amount
        )
        
        # Get last payment date
        last_payment = session.exec(
            select(FeePayment)
            .where(FeePayment.student_fee_id == student_fee.id)
            .where(FeePayment.payment_status == PaymentStatus.SUCCESS)
            .order_by(FeePayment.payment_date.desc())
        ).first()
        
        defaulters.append(FeeDefaulter(
            student_id=student.id,
            student_name=student.name,
            admission_number=student.admission_number,
            program=student.program.name if student.program else "Unknown",
            year=student.current_year,
            total_due=total_due,
            overdue_installments=0,  # TODO: Calculate based on installment due dates
            last_payment_date=last_payment.payment_date.date() if last_payment and last_payment.payment_date else None,
            days_overdue=0  # TODO: Calculate based on due dates
        ))
    
    return defaulters
