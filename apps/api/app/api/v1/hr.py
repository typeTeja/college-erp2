"""
HR & Payroll API Endpoints

Provides HR and payroll functionality
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from pydantic import BaseModel
from datetime import date

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.services.hr_service import HRService

router = APIRouter(prefix="/hr", tags=["HR & Payroll"])


# Schemas
class EmployeeCreate(BaseModel):
    employee_code: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    join_date: date


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None
    status: str = "PRESENT"


class LeaveRequest(BaseModel):
    employee_id: int
    leave_type: str
    from_date: date
    to_date: date
    reason: str


class SalarySlipCreate(BaseModel):
    employee_id: int
    month: int
    year: int
    basic_salary: float
    allowances: Optional[dict] = None
    deductions: Optional[dict] = None


# ============================================================================
# Employee Management Endpoints
# ============================================================================

@router.post("/employees")
def create_employee(
    *,
    session: Session = Depends(get_session),
    employee_data: EmployeeCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create employee"""
    return {"message": "Employee created", "data": employee_data.model_dump()}


@router.get("/employees")
def list_employees(
    *,
    session: Session = Depends(get_session),
    department: Optional[str] = Query(None),
    active_only: bool = Query(True)
):
    """List employees"""
    return {"employees": []}


# ============================================================================
# Attendance Endpoints
# ============================================================================

@router.post("/attendance")
def mark_attendance(
    *,
    session: Session = Depends(get_session),
    attendance_data: AttendanceCreate
):
    """Mark employee attendance"""
    return {"message": "Attendance marked", "data": attendance_data.model_dump()}


@router.get("/attendance/{employee_id}")
def get_employee_attendance(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    month: Optional[int] = Query(None),
    year: Optional[int] = Query(None)
):
    """Get employee attendance"""
    return {"attendance": []}


# ============================================================================
# Leave Management Endpoints
# ============================================================================

@router.post("/leave")
def apply_leave(
    *,
    session: Session = Depends(get_session),
    leave_data: LeaveRequest
):
    """Apply for leave"""
    total_days = (leave_data.to_date - leave_data.from_date).days + 1
    return {
        "message": "Leave application submitted",
        "total_days": total_days
    }


@router.get("/leave")
def list_leave_requests(
    *,
    session: Session = Depends(get_session),
    status: Optional[str] = Query(None),
    employee_id: Optional[int] = Query(None)
):
    """List leave requests"""
    return {"leave_requests": []}


@router.post("/leave/{leave_id}/approve")
def approve_leave(
    *,
    session: Session = Depends(get_session),
    leave_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """Approve leave request"""
    return {"message": "Leave approved"}


# ============================================================================
# Payroll Endpoints
# ============================================================================

@router.post("/salary-slips")
def generate_salary_slip(
    *,
    session: Session = Depends(get_session),
    salary_data: SalarySlipCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Generate salary slip"""
    calculation = HRService.calculate_salary(
        salary_data.basic_salary,
        salary_data.allowances or {},
        salary_data.deductions or {}
    )
    
    return {
        "message": "Salary slip generated",
        "calculation": calculation
    }


@router.get("/salary-slips/{employee_id}")
def get_employee_salary_slips(
    *,
    session: Session = Depends(get_session),
    employee_id: int,
    year: Optional[int] = Query(None)
):
    """Get employee salary slips"""
    return {"salary_slips": []}


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/summary")
def get_hr_statistics(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get HR statistics"""
    return HRService.get_hr_statistics(session)
