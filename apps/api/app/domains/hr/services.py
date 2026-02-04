"""
HR Domain Services

Business logic for HR domain including:
- Designation management
- Staff management
- Faculty management
- HR statistics and reporting
"""

from typing import Dict, List, Optional
from datetime import date
from sqlmodel import Session, select, func

from app.domains.hr.models import Designation, Staff, Faculty, Department, Shift
from app.domains.hr.schemas import (
    DesignationCreate, DesignationUpdate,
    StaffCreate, StaffUpdate,
    FacultyCreate, FacultyUpdate
)
from app.domains.hr.exceptions import (
    DesignationNotFoundError, StaffNotFoundError, FacultyNotFoundError,
    DuplicateEmailError, DuplicateMobileError
)


class HRService:
    """Service for People & HR operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ----------------------------------------------------------------------
    # Department Management
    # ----------------------------------------------------------------------
    
    def list_departments(self) -> List[Department]:
        """List all departments"""
        from app.domains.hr.models import Department
        statement = select(Department).where(Department.is_active == True)
        return list(self.session.exec(statement).all())
    
    # ----------------------------------------------------------------------
    # Shift Management
    # ----------------------------------------------------------------------
    
    def list_shifts(self) -> List[Shift]:
        """List all shifts"""
        from app.domains.hr.models import Shift
        return list(self.session.exec(select(Shift).where(Shift.is_active == True)).all())

    # ----------------------------------------------------------------------
    # Designation Management
    # ----------------------------------------------------------------------
    
    def get_designation(self, designation_id: int) -> Designation:
        """Get designation by ID"""
        designation = self.session.get(Designation, designation_id)
        if not designation:
            raise DesignationNotFoundError(f"Designation with ID {designation_id} not found")
        return designation
    
    def list_designations(self, is_teaching: Optional[bool] = None) -> List[Designation]:
        """List all designations"""
        statement = select(Designation)
        if is_teaching is not None:
            statement = statement.where(Designation.is_teaching == is_teaching)
        statement = statement.order_by(Designation.display_order)
        return list(self.session.exec(statement).all())
    
    def create_designation(self, designation_data: DesignationCreate) -> Designation:
        """Create a new designation"""
        designation = Designation(**designation_data.model_dump())
        self.session.add(designation)
        self.session.commit()
        self.session.refresh(designation)
        return designation
    
    def update_designation(self, designation_id: int, designation_data: DesignationUpdate) -> Designation:
        """Update a designation"""
        designation = self.get_designation(designation_id)
        
        update_data = designation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(designation, key, value)
        
        self.session.add(designation)
        self.session.commit()
        self.session.refresh(designation)
        return designation
    
    # ----------------------------------------------------------------------
    # Staff Management
    # ----------------------------------------------------------------------
    
    def get_staff(self, staff_id: int) -> Staff:
        """Get staff by ID"""
        staff = self.session.get(Staff, staff_id)
        if not staff:
            raise StaffNotFoundError(f"Staff member with ID {staff_id} not found")
        return staff
    
    def list_staff(self, department: Optional[str] = None, is_active: Optional[bool] = None) -> List[Staff]:
        """List all staff"""
        statement = select(Staff)
        if department:
            statement = statement.where(Staff.department == department)
        if is_active is not None:
            statement = statement.where(Staff.is_active == is_active)
        return list(self.session.exec(statement).all())
    
    def create_staff(self, staff_data: StaffCreate) -> Staff:
        """Create a new staff member"""
        # Check for duplicate email
        existing_email = self.session.exec(
            select(Staff).where(Staff.email == staff_data.email)
        ).first()
        if existing_email:
            raise DuplicateEmailError(f"Staff with email {staff_data.email} already exists")
        
        # Check for duplicate mobile
        existing_mobile = self.session.exec(
            select(Staff).where(Staff.mobile == staff_data.mobile)
        ).first()
        if existing_mobile:
            raise DuplicateMobileError(f"Staff with mobile {staff_data.mobile} already exists")
        
        staff = Staff(**staff_data.model_dump())
        self.session.add(staff)
        self.session.commit()
        self.session.refresh(staff)
        return staff
    
    def update_staff(self, staff_id: int, staff_data: StaffUpdate) -> Staff:
        """Update a staff member"""
        staff = self.get_staff(staff_id)
        
        update_data = staff_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(staff, key, value)
        
        self.session.add(staff)
        self.session.commit()
        self.session.refresh(staff)
        return staff
    
    # ----------------------------------------------------------------------
    # Faculty Management
    # ----------------------------------------------------------------------
    
    def get_faculty(self, faculty_id: int) -> Faculty:
        """Get faculty by ID"""
        faculty = self.session.get(Faculty, faculty_id)
        if not faculty:
            raise FacultyNotFoundError(f"Faculty member with ID {faculty_id} not found")
        return faculty
    
    def list_faculty(self, department: Optional[str] = None) -> List[Faculty]:
        """List all faculty"""
        statement = select(Faculty)
        if department:
            statement = statement.where(Faculty.department == department)
        return list(self.session.exec(statement).all())
    
    def create_faculty(self, faculty_data: FacultyCreate) -> Faculty:
        """Create a new faculty member"""
        # Check for duplicate email if provided
        if faculty_data.email:
            existing_email = self.session.exec(
                select(Faculty).where(Faculty.email == faculty_data.email)
            ).first()
            if existing_email:
                raise DuplicateEmailError(f"Faculty with email {faculty_data.email} already exists")
        
        faculty = Faculty(**faculty_data.model_dump())
        self.session.add(faculty)
        self.session.commit()
        self.session.refresh(faculty)
        return faculty
    
    def update_faculty(self, faculty_id: int, faculty_data: FacultyUpdate) -> Faculty:
        """Update a faculty member"""
        faculty = self.get_faculty(faculty_id)
        
        update_data = faculty_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(faculty, key, value)
        
        self.session.add(faculty)
        self.session.commit()
        self.session.refresh(faculty)
        return faculty
    
    # ----------------------------------------------------------------------
    # HR Statistics
    # ----------------------------------------------------------------------
    
    def get_hr_statistics(self) -> Dict:
        """Get overall employee statistics"""
        staff_count = self.session.exec(select(func.count(Staff.id))).one()
        faculty_count = self.session.exec(select(func.count(Faculty.id))).one()
        active_staff = self.session.exec(
            select(func.count(Staff.id)).where(Staff.is_active == True)
        ).one()
        
        return {
            "total_staff": staff_count,
            "total_faculty": faculty_count,
            "total_employees": staff_count + faculty_count,
            "active_staff": active_staff,
        }
    
    def calculate_salary(
        self,
        basic_salary: float,
        allowances: Dict[str, float],
        deductions: Dict[str, float]
    ) -> Dict:
        """Calculate net salary for payroll components"""
        total_allowances = sum(allowances.values()) if allowances else 0
        total_deductions = sum(deductions.values()) if deductions else 0
        
        gross_salary = basic_salary + total_allowances
        net_salary = gross_salary - total_deductions
        
        return {
            "basic_salary": basic_salary,
            "total_allowances": total_allowances,
            "total_deductions": total_deductions,
            "gross_salary": gross_salary,
            "net_salary": net_salary
        }
