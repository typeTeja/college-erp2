import json
from typing import List, Optional
from datetime import datetime, date
from sqlmodel import Session, select, and_
from fastapi import HTTPException

from .models.exam import (
    UniversityExam, 
    UniversityExamRegistration, 
    UniversityExamResult,
    SemesterResult
)
from .schemas import (
    UniversityExamCreate,
    UniversityExamRegistrationCreate,
    UniversityExamResultCreate
)

class UniversityExamService:
    """Service for managing University Examinations & Results"""

    @staticmethod
    def create_exam(session: Session, data: UniversityExamCreate, user_id: Optional[int] = None) -> UniversityExam:
        """Setup a new university examination cycle"""
        db_exam = UniversityExam(**data.model_dump())
        if user_id:
            db_exam.created_by = user_id
        session.add(db_exam)
        session.commit()
        session.refresh(db_exam)
        return db_exam

    @staticmethod
    def register_student(session: Session, data: UniversityExamRegistrationCreate) -> UniversityExamRegistration:
        """Register a student for a university exam"""
        # Logic for registration number generation
        reg_count = session.exec(select(UniversityExamRegistration)).all()
        reg_no = f"REG-{date.today().year}-{len(reg_count) + 1:04d}"

        # Subjects need to be stringified for JSON column if not handled by SQLModel
        subjects_json = json.dumps(data.subjects_registered)

        db_reg = UniversityExamRegistration(
            registration_number=reg_no,
            **data.model_dump(exclude={"subjects_registered"})
        )
        db_reg.subjects_registered = subjects_json

        session.add(db_reg)
        session.commit()
        session.refresh(db_reg)
        return db_reg

    @staticmethod
    def generate_hall_tickets(session: Session, university_exam_id: int) -> List[UniversityExamRegistration]:
        """Generate hall ticket numbers for all eligible registered students"""
        registrations = session.exec(
            select(UniversityExamRegistration).where(
                and_(
                    UniversityExamRegistration.university_exam_id == university_exam_id,
                    UniversityExamRegistration.is_eligible == True,
                    UniversityExamRegistration.fee_paid == True
                )
            )
        ).all()

        for i, reg in enumerate(registrations):
            if not reg.hall_ticket_number:
                reg.hall_ticket_number = f"HT-{university_exam_id}-{reg.student_id}-{i+1:03d}"
                reg.hall_ticket_generated = True
                session.add(reg)
        
        session.commit()
        return registrations

    @staticmethod
    def record_result(session: Session, data: UniversityExamResultCreate) -> UniversityExamResult:
        """Record/import a student's result for a subject"""
        db_result = UniversityExamResult(**data.model_dump())
        session.add(db_result)
        session.commit()
        session.refresh(db_result)
        return db_result

university_exam_service = UniversityExamService()
