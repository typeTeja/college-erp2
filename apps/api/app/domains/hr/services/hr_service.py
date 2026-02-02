from typing import Dict, List, Optional
from datetime import date
from sqlmodel import Session, select, func
from fastapi import HTTPException

from ..models.staff import Staff
from ..models.faculty import Faculty
from ..models.designation import Designation

class HRService:
    """Service for People & HR operations (Principal Identity Owner)"""
    
    @staticmethod
    def get_staff(session: Session, staff_id: int) -> Staff:
        staff = session.get(Staff, staff_id)
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
        return staff

    @staticmethod
    def get_faculty(session: Session, faculty_id: int) -> Faculty:
        faculty = session.get(Faculty, faculty_id)
        if not faculty:
            raise HTTPException(status_code=404, detail="Faculty member not found")
        return faculty

    @staticmethod
    def list_staff(session: Session, department: Optional[str] = None) -> List[Staff]:
        stmt = select(Staff)
        if department:
            stmt = stmt.where(Staff.department == department)
        return session.exec(stmt).all()

    @staticmethod
    def list_faculty(session: Session, department: Optional[str] = None) -> List[Faculty]:
        stmt = select(Faculty)
        if department:
            stmt = stmt.where(Faculty.department == department)
        return session.exec(stmt).all()

    @staticmethod
    def calculate_salary(
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
    
    @staticmethod
    def get_hr_statistics(session: Session) -> Dict:
        """Get overall employee statistics"""
        staff_count = session.exec(select(func.count(Staff.id))).one()
        faculty_count = session.exec(select(func.count(Faculty.id))).one()
        
        return {
            "total_staff": staff_count,
            "total_faculty": faculty_count,
            "total_employees": staff_count + faculty_count,
            "active_employees": staff_count + faculty_count, # Simplified
        }

hr_service = HRService()
