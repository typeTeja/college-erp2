"""
Internal Exam Service Layer

Handles business logic for internal exams including:
- Exam creation and configuration
- Marks entry and validation
- Grade calculation
- GPA calculation
- Result consolidation
- Rank calculation
"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlmodel import Session, select, func
from fastapi import HTTPException

from app.domains.academic.models import (
    InternalExam, InternalExamSubject, StudentInternalMarks,
    InternalMarksConsolidated, ExamType, ResultStatus, BatchSemester
)
from app.models.student import Student


class GradeCalculator:
    """Grade and GPA calculation utility"""
    
    # Grade boundaries (percentage-based)
    GRADE_SCALE = [
        (90, 100, "A+", 10.0),
        (80, 89, "A", 9.0),
        (70, 79, "B+", 8.0),
        (60, 69, "B", 7.0),
        (50, 59, "C+", 6.0),
        (40, 49, "C", 5.0),
        (0, 39, "F", 0.0),
    ]
    
    @staticmethod
    def calculate_grade(percentage: float) -> tuple[str, float]:
        """Calculate grade and GPA from percentage"""
        for min_pct, max_pct, grade, gpa in GradeCalculator.GRADE_SCALE:
            if min_pct <= percentage <= max_pct:
                return grade, gpa
        return "F", 0.0


class InternalExamService:
    """Service for internal exam operations"""
    
    @staticmethod
    def create_exam(
        session: Session,
        exam_data: dict,
        user_id: int
    ) -> InternalExam:
        """Create a new internal exam"""
        exam = InternalExam(
            **exam_data,
            created_by=user_id
        )
        session.add(exam)
        session.commit()
        session.refresh(exam)
        return exam
    
    @staticmethod
    def add_subjects_to_exam(
        session: Session,
        exam_id: int,
        subjects_data: List[dict]
    ) -> List[InternalExamSubject]:
        """Add subjects to an internal exam"""
        exam = session.get(InternalExam, exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        subjects = []
        for subject_data in subjects_data:
            subject = InternalExamSubject(
                internal_exam_id=exam_id,
                **subject_data
            )
            session.add(subject)
            subjects.append(subject)
        
        session.commit()
        return subjects
    
    @staticmethod
    def enter_marks(
        session: Session,
        marks_data: List[dict],
        entered_by: int
    ) -> List[StudentInternalMarks]:
        """Bulk marks entry"""
        marks_records = []
        
        for data in marks_data:
            # Check if marks already exist
            stmt = select(StudentInternalMarks).where(
                StudentInternalMarks.student_id == data["student_id"],
                StudentInternalMarks.internal_exam_subject_id == data["internal_exam_subject_id"]
            )
            existing = session.exec(stmt).first()
            
            if existing:
                # Update existing marks
                existing.marks_obtained = data.get("marks_obtained")
                existing.is_absent = data.get("is_absent", False)
                existing.remarks = data.get("remarks")
                existing.entered_by = entered_by
                existing.entered_at = datetime.utcnow()
                existing.updated_at = datetime.utcnow()
                marks_records.append(existing)
            else:
                # Create new marks record
                marks = StudentInternalMarks(
                    **data,
                    entered_by=entered_by,
                    entered_at=datetime.utcnow()
                )
                session.add(marks)
                marks_records.append(marks)
        
        session.commit()
        return marks_records
    
    @staticmethod
    def verify_marks(
        session: Session,
        marks_ids: List[int],
        verified_by: int
    ) -> List[StudentInternalMarks]:
        """Verify entered marks"""
        marks_records = []
        
        for marks_id in marks_ids:
            marks = session.get(StudentInternalMarks, marks_id)
            if marks:
                marks.is_verified = True
                marks.verified_by = verified_by
                marks.verified_at = datetime.utcnow()
                marks_records.append(marks)
        
        session.commit()
        return marks_records
    
    @staticmethod
    def consolidate_marks(
        session: Session,
        student_id: int,
        batch_semester_id: int,
        academic_year: str
    ) -> InternalMarksConsolidated:
        """Consolidate marks for a student in a semester"""
        # Get all internal exams for the semester
        stmt = select(InternalExam).where(
            InternalExam.batch_semester_id == batch_semester_id,
            InternalExam.academic_year == academic_year,
            InternalExam.is_published == True
        )
        exams = session.exec(stmt).all()
        
        total_max_marks = 0.0
        total_obtained = 0.0
        
        for exam in exams:
            # Get exam subjects
            for exam_subject in exam.subjects:
                # Get student marks
                stmt = select(StudentInternalMarks).where(
                    StudentInternalMarks.student_id == student_id,
                    StudentInternalMarks.internal_exam_subject_id == exam_subject.id
                )
                marks = session.exec(stmt).first()
                
                if marks and not marks.is_absent:
                    total_max_marks += exam_subject.max_marks
                    total_obtained += marks.marks_obtained or 0.0
        
        # Calculate percentage
        percentage = (total_obtained / total_max_marks * 100) if total_max_marks > 0 else 0.0
        
        # Calculate grade and GPA
        grade, gpa = GradeCalculator.calculate_grade(percentage)
        
        # Determine result status
        result_status = ResultStatus.PASS if percentage >= 40 else ResultStatus.FAIL
        
        # Check if consolidated record exists
        stmt = select(InternalMarksConsolidated).where(
            InternalMarksConsolidated.student_id == student_id,
            InternalMarksConsolidated.batch_semester_id == batch_semester_id,
            InternalMarksConsolidated.academic_year == academic_year
        )
        consolidated = session.exec(stmt).first()
        
        if consolidated:
            # Update existing
            consolidated.total_max_marks = total_max_marks
            consolidated.total_marks_obtained = total_obtained
            consolidated.percentage = percentage
            consolidated.grade = grade
            consolidated.gpa = gpa
            consolidated.result_status = result_status
            consolidated.updated_at = datetime.utcnow()
        else:
            # Create new
            consolidated = InternalMarksConsolidated(
                student_id=student_id,
                batch_semester_id=batch_semester_id,
                academic_year=academic_year,
                total_max_marks=total_max_marks,
                total_marks_obtained=total_obtained,
                percentage=percentage,
                grade=grade,
                gpa=gpa,
                result_status=result_status
            )
            session.add(consolidated)
        
        session.commit()
        session.refresh(consolidated)
        
        # Calculate rank
        InternalExamService.calculate_ranks(session, batch_semester_id, academic_year)
        
        return consolidated
    
    @staticmethod
    def calculate_ranks(
        session: Session,
        batch_semester_id: int,
        academic_year: str
    ):
        """Calculate ranks for all students in a semester"""
        # Get all consolidated marks ordered by percentage
        stmt = select(InternalMarksConsolidated).where(
            InternalMarksConsolidated.batch_semester_id == batch_semester_id,
            InternalMarksConsolidated.academic_year == academic_year
        ).order_by(InternalMarksConsolidated.percentage.desc())
        
        results = session.exec(stmt).all()
        
        # Assign ranks
        for rank, result in enumerate(results, start=1):
            result.rank = rank
        
        session.commit()
    
    @staticmethod
    def publish_results(
        session: Session,
        exam_id: int,
        published_by: int
    ) -> InternalExam:
        """Publish exam results"""
        exam = session.get(InternalExam, exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        exam.is_published = True
        exam.published_at = datetime.utcnow()
        exam.published_by = published_by
        
        session.commit()
        session.refresh(exam)
        
        # Consolidate marks for all students
        # Get all students in the batch
        stmt = select(Student).where(Student.batch_semester_id == exam.batch_semester_id)
        students = session.exec(stmt).all()
        
        for student in students:
            InternalExamService.consolidate_marks(
                session,
                student.id,
                exam.batch_semester_id,
                exam.academic_year
            )
        
        return exam
    
    @staticmethod
    def get_student_results(
        session: Session,
        student_id: int,
        academic_year: Optional[str] = None
    ) -> List[InternalMarksConsolidated]:
        """Get consolidated results for a student"""
        stmt = select(InternalMarksConsolidated).where(
            InternalMarksConsolidated.student_id == student_id
        )
        
        if academic_year:
            stmt = stmt.where(InternalMarksConsolidated.academic_year == academic_year)
        
        return session.exec(stmt).all()
    
    @staticmethod
    def get_exam_statistics(
        session: Session,
        exam_id: int
    ) -> Dict:
        """Get statistics for an exam"""
        exam = session.get(InternalExam, exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        
        # Get all marks for this exam
        total_students = 0
        present_students = 0
        total_marks = 0.0
        
        for exam_subject in exam.subjects:
            stmt = select(StudentInternalMarks).where(
                StudentInternalMarks.internal_exam_subject_id == exam_subject.id
            )
            marks_list = session.exec(stmt).all()
            
            total_students += len(marks_list)
            present_students += sum(1 for m in marks_list if not m.is_absent)
            total_marks += sum(m.marks_obtained or 0 for m in marks_list if not m.is_absent)
        
        avg_marks = total_marks / present_students if present_students > 0 else 0
        
        return {
            "exam_id": exam_id,
            "exam_name": exam.name,
            "total_students": total_students,
            "present_students": present_students,
            "absent_students": total_students - present_students,
            "average_marks": round(avg_marks, 2),
            "attendance_percentage": round((present_students / total_students * 100) if total_students > 0 else 0, 2)
        }
