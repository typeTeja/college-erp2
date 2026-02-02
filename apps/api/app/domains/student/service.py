from typing import Any, List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select, func
from .models.student import Student
from app.domains.academic.service import academic_validation_service

class StudentService:
    """Consolidated service for Student operations"""

    @staticmethod
    def get_students(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        program_id: Optional[int] = None,
        semester_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[dict]:
        """Retrieve students with basic filters"""
        query = select(Student)
        if program_id:
            query = query.where(Student.program_id == program_id)
        if semester_id:
            query = query.where(Student.batch_semester_id == semester_id)
        if search:
            query = query.where(Student.name.contains(search) | Student.admission_number.contains(search))
        
        students = session.exec(query.offset(skip).limit(limit)).all()
        
        results = []
        for s in students:
            student_data = s.model_dump()
            student_data["program_name"] = s.program.name if s.program else "Unknown"
            # Optional: Add batch code, etc.
            results.append(student_data)
            
        return results

    @staticmethod
    def create_student(
        session: Session,
        student_in_data: dict,
        current_user_id: int
    ) -> Student:
        """Create a new student with hierarchy validation"""
        # Validate hierarchy
        academic_validation_service.validate_hierarchy(
            session=session,
            batch_id=student_in_data.get("batch_id"),
            program_year_id=student_in_data.get("program_year_id"),
            batch_semester_id=student_in_data.get("batch_semester_id"),
            section_id=student_in_data.get("section_id")
        )
        
        # Check admission number uniqueness
        existing = session.exec(select(Student).where(Student.admission_number == student_in_data.get("admission_number"))).first()
        if existing:
            raise HTTPException(status_code=400, detail="Admission number already exists")

        db_student = Student(**student_in_data)
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        return db_student

student_service = StudentService()
