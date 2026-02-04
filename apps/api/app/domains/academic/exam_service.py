from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlmodel import Session, select, and_
from fastapi import HTTPException

from app.domains.academic.models.exam import (
    InternalExam, 
    InternalExamSubject, 
    StudentInternalMarks
)
from app.domains.academic.schemas import (
    InternalExamCreate,
    StudentInternalMarksCreate
)
from app.shared.enums import ExamType, ExamStatus

class ExamService:
    """Service for handling examination operations"""
    
    @staticmethod
    def create_internal_exam(session: Session, data: InternalExamCreate) -> InternalExam:
        """Create a new internal exam cycle"""
        
        # Check if code already exists
        existing = session.exec(select(InternalExam).where(InternalExam.exam_code == data.exam_code)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Internal exam with this code already exists")
            
        db_exam = InternalExam(
            name=data.name,
            exam_code=data.exam_code,
            academic_year=data.academic_year,
            batch_id=data.batch_id,
            batch_semester_id=data.batch_semester_id,
            exam_type=data.exam_type,
            start_date=data.start_date,
            end_date=data.end_date,
            total_marks=data.total_marks,
            passing_marks=data.passing_marks,
            weightage=data.weightage
        )
        
        session.add(db_exam)
        session.commit()
        session.refresh(db_exam)
        return db_exam

    @staticmethod
    def schedule_exam_subject(
        session: Session, 
        internal_exam_id: int, 
        batch_subject_id: int, 
        exam_date: date,
        exam_time: str,
        max_marks: int,
        passing_marks: int
    ) -> InternalExamSubject:
        """Schedule a specific subject in an internal exam"""
        
        db_subject = InternalExamSubject(
            internal_exam_id=internal_exam_id,
            batch_subject_id=batch_subject_id,
            exam_date=exam_date,
            exam_time=exam_time,
            max_marks=max_marks,
            passing_marks=passing_marks
        )
        
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return db_subject

    @staticmethod
    def mark_student_marks(session: Session, data: StudentInternalMarksCreate) -> StudentInternalMarks:
        """Record marks for a student in a subject"""
        
        # Check if record already exists
        existing = session.exec(
            select(StudentInternalMarks).where(
                and_(
                    StudentInternalMarks.student_id == data.student_id,
                    StudentInternalMarks.internal_exam_subject_id == data.internal_exam_subject_id
                )
            )
        ).first()
        
        if existing:
            existing.marks_obtained = data.marks_obtained
            existing.is_absent = data.is_absent
            existing.remarks = data.remarks
            existing.updated_at = datetime.utcnow()
            db_marks = existing
        else:
            db_marks = StudentInternalMarks(
                student_id=data.student_id,
                internal_exam_subject_id=data.internal_exam_subject_id,
                marks_obtained=data.marks_obtained,
                is_absent=data.is_absent,
                remarks=data.remarks
            )
            session.add(db_marks)
            
        session.commit()
        session.refresh(db_marks)
        return db_marks

    @staticmethod
    def get_internal_exam_details(session: Session, internal_exam_id: int) -> Dict[str, Any]:
        """Get full details of an internal exam including subjects"""
        exam = session.get(InternalExam, internal_exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Internal exam not found")
            
        return {
            "exam": exam,
            "subjects": exam.subjects
        }

exam_service = ExamService()
