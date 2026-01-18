"""
University Exam Service Layer

Handles business logic for university exams including:
- Registration management
- Eligibility checking
- Result import and processing
- SGPA/CGPA calculation
- Backlog tracking
"""
from typing import List, Optional, Dict
from datetime import datetime, date
from sqlmodel import Session, select, func
from fastapi import HTTPException

from app.models.academic.university_exam import (
    UniversityExam, UniversityExamRegistration, UniversityExamResult,
    SemesterResult, ExamResultStatus
)
from app.models.student import Student
from app.models.fee import StudentFee


class GradeCalculator:
    """University grade and GPA calculation"""
    
    # Grade scale (percentage-based)
    GRADE_SCALE = [
        (90, 100, "O", 10.0),   # Outstanding
        (80, 89, "A+", 9.0),
        (70, 79, "A", 8.0),
        (60, 69, "B+", 7.0),
        (50, 59, "B", 6.0),
        (45, 49, "C", 5.0),
        (40, 44, "D", 4.0),
        (0, 39, "F", 0.0),      # Fail
    ]
    
    @staticmethod
    def calculate_grade(percentage: float) -> tuple[str, float]:
        """Calculate grade and grade points from percentage"""
        for min_pct, max_pct, grade, points in GradeCalculator.GRADE_SCALE:
            if min_pct <= percentage <= max_pct:
                return grade, points
        return "F", 0.0


class UniversityExamService:
    """Service for university exam operations"""
    
    @staticmethod
    def check_eligibility(
        session: Session,
        student_id: int,
        exam_id: int
    ) -> Dict:
        """Check if student is eligible for university exam"""
        student = session.get(Student, student_id)
        exam = session.get(UniversityExam, exam_id)
        
        if not student or not exam:
            raise HTTPException(status_code=404, detail="Student or exam not found")
        
        issues = []
        is_eligible = True
        
        # Check fee dues
        stmt = select(StudentFee).where(
            StudentFee.student_id == student_id,
            StudentFee.total_pending > 0
        )
        fee_dues = session.exec(stmt).all()
        
        if fee_dues:
            total_pending = sum(f.total_pending for f in fee_dues)
            if total_pending > 0:
                is_eligible = False
                issues.append({
                    "type": "fee_dues",
                    "amount": float(total_pending),
                    "description": f"Pending fee: ₹{total_pending}"
                })
        
        # Check attendance (placeholder - would need attendance tracking)
        # if student.attendance_percentage < exam.min_attendance_percentage:
        #     is_eligible = False
        #     issues.append({
        #         "type": "attendance_shortage",
        #         "attendance": student.attendance_percentage,
        #         "required": exam.min_attendance_percentage
        #     })
        
        return {
            "student_id": student_id,
            "exam_id": exam_id,
            "is_eligible": is_eligible,
            "issues": issues
        }
    
    @staticmethod
    def register_student(
        session: Session,
        student_id: int,
        exam_id: int,
        batch_semester_id: int,
        subject_ids: List[int],
        force: bool = False
    ) -> UniversityExamRegistration:
        """Register student for university exam"""
        # Check eligibility
        if not force:
            eligibility = UniversityExamService.check_eligibility(session, student_id, exam_id)
            if not eligibility["is_eligible"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Student not eligible: {eligibility['issues']}"
                )
        
        exam = session.get(UniversityExam, exam_id)
        student = session.get(Student, student_id)
        
        # Generate registration number
        count = len(session.exec(select(UniversityExamRegistration).where(
            UniversityExamRegistration.university_exam_id == exam_id
        )).all())
        reg_number = f"REG-{exam.exam_code}-{str(count + 1).zfill(6)}"
        
        # Check if late registration
        today = date.today()
        is_late = today > exam.registration_end
        
        # Calculate fees
        exam_fee = exam.exam_fee
        late_fee = exam.late_fee if is_late else 0.0
        total_fee = exam_fee + late_fee
        
        # Create registration
        registration = UniversityExamRegistration(
            student_id=student_id,
            university_exam_id=exam_id,
            batch_semester_id=batch_semester_id,
            registration_number=reg_number,
            is_late_registration=is_late,
            subjects_registered=str(subject_ids),  # JSON
            exam_fee=exam_fee,
            late_fee=late_fee,
            total_fee=total_fee
        )
        
        session.add(registration)
        session.commit()
        session.refresh(registration)
        return registration
    
    @staticmethod
    def import_results(
        session: Session,
        results_data: List[Dict],
        imported_by: int
    ) -> List[UniversityExamResult]:
        """Import university exam results"""
        results = []
        
        for data in results_data:
            # Calculate percentage
            total_marks = data["total_marks"]
            total_max = data["total_max_marks"]
            percentage = (total_marks / total_max * 100) if total_max > 0 else 0
            
            # Calculate grade
            grade, grade_points = GradeCalculator.calculate_grade(percentage)
            
            # Determine credits earned
            credits = data["credits"]
            credits_earned = credits if percentage >= 40 else 0
            
            # Determine result status
            result_status = ExamResultStatus.PASS if percentage >= 40 else ExamResultStatus.FAIL
            
            result = UniversityExamResult(
                **data,
                percentage=percentage,
                grade=grade,
                grade_points=grade_points,
                credits_earned=credits_earned,
                result_status=result_status,
                imported_by=imported_by,
                imported_at=datetime.utcnow()
            )
            
            session.add(result)
            results.append(result)
        
        session.commit()
        return results
    
    @staticmethod
    def calculate_semester_result(
        session: Session,
        student_id: int,
        batch_semester_id: int,
        academic_year: str
    ) -> SemesterResult:
        """Calculate consolidated semester result with SGPA/CGPA"""
        # Get all results for this semester
        stmt = select(UniversityExamResult).where(
            UniversityExamResult.student_id == student_id
        )
        results = session.exec(stmt).all()
        
        # Filter results for this semester (would need better filtering)
        semester_results = results  # Placeholder
        
        # Calculate totals
        total_credits = sum(r.credits for r in semester_results)
        credits_earned = sum(r.credits_earned for r in semester_results)
        credits_failed = total_credits - credits_earned
        
        # Calculate SGPA (Semester GPA)
        total_grade_points = sum(r.grade_points * r.credits for r in semester_results)
        sgpa = (total_grade_points / total_credits) if total_credits > 0 else 0.0
        
        # Calculate CGPA (would need all previous semesters)
        # For now, just use SGPA
        cgpa = sgpa
        
        # Calculate marks
        total_marks_max = sum(r.total_max_marks for r in semester_results)
        marks_obtained = sum(r.total_marks for r in semester_results)
        percentage = (marks_obtained / total_marks_max * 100) if total_marks_max > 0 else 0
        
        # Determine result status
        result_status = ExamResultStatus.PASS if credits_failed == 0 else ExamResultStatus.FAIL
        
        # Track backlogs
        backlog_subjects = []
        for r in semester_results:
            if r.result_status == ExamResultStatus.FAIL:
                backlog_subjects.append({
                    "subject_id": r.batch_subject_id,
                    "marks": r.total_marks,
                    "percentage": r.percentage
                })
        
        # Check if exists
        stmt = select(SemesterResult).where(
            SemesterResult.student_id == student_id,
            SemesterResult.batch_semester_id == batch_semester_id,
            SemesterResult.academic_year == academic_year
        )
        semester_result = session.exec(stmt).first()
        
        if semester_result:
            # Update existing
            semester_result.total_credits = total_credits
            semester_result.credits_earned = credits_earned
            semester_result.credits_failed = credits_failed
            semester_result.sgpa = sgpa
            semester_result.cgpa = cgpa
            semester_result.total_marks = total_marks_max
            semester_result.marks_obtained = marks_obtained
            semester_result.percentage = percentage
            semester_result.result_status = result_status
            semester_result.backlog_subjects = str(backlog_subjects)
            semester_result.updated_at = datetime.utcnow()
        else:
            # Create new
            semester_result = SemesterResult(
                student_id=student_id,
                batch_semester_id=batch_semester_id,
                academic_year=academic_year,
                semester=1,  # Would need to determine actual semester
                total_credits=total_credits,
                credits_earned=credits_earned,
                credits_failed=credits_failed,
                sgpa=sgpa,
                cgpa=cgpa,
                total_marks=total_marks_max,
                marks_obtained=marks_obtained,
                percentage=percentage,
                result_status=result_status,
                backlog_subjects=str(backlog_subjects)
            )
            session.add(semester_result)
        
        session.commit()
        session.refresh(semester_result)
        
        # Calculate ranks
        UniversityExamService.calculate_ranks(session, batch_semester_id, academic_year)
        
        return semester_result
    
    @staticmethod
    def calculate_ranks(
        session: Session,
        batch_semester_id: int,
        academic_year: str
    ):
        """Calculate ranks for semester"""
        stmt = select(SemesterResult).where(
            SemesterResult.batch_semester_id == batch_semester_id,
            SemesterResult.academic_year == academic_year
        ).order_by(SemesterResult.sgpa.desc())
        
        results = session.exec(stmt).all()
        
        for rank, result in enumerate(results, start=1):
            result.rank = rank
        
        session.commit()
