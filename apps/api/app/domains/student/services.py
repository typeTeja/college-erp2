"""
Student Domain Services

Business logic for student domain.
Note: This is a simplified version. Full services can be added as needed.
"""

from typing import List, Optional
from sqlmodel import Session, select

from app.domains.student.models import Student, Parent, Enrollment, StudentDocument
from app.domains.student.schemas import (
    StudentCreate, ParentCreate, EnrollmentCreate, DocumentCreate
)
from app.domains.student.exceptions import (
    StudentNotFoundError, ParentNotFoundError,
    EnrollmentNotFoundError, DocumentNotFoundError
)


class StudentService:
    """Service for student domain operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ----------------------------------------------------------------------
    # Student Management
    # ----------------------------------------------------------------------
    
    def get_student(self, student_id: int) -> Student:
        """Get student by ID"""
        student = self.session.get(Student, student_id)
        if not student:
            raise StudentNotFoundError(f"Student with ID {student_id} not found")
        return student
    
    def list_students(self, batch_id: Optional[int] = None, status: Optional[str] = None) -> List[Student]:
        """List all students"""
        statement = select(Student)
        if batch_id:
            statement = statement.where(Student.batch_id == batch_id)
        if status:
            statement = statement.where(Student.status == status)
        return list(self.session.exec(statement).all())
    
    def create_student(self, student_data: StudentCreate) -> Student:
        """Create a new student"""
        student = Student(**student_data.model_dump())
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)
        return student
    
    # ----------------------------------------------------------------------
    # Parent Management
    # ----------------------------------------------------------------------
    
    def get_parent(self, parent_id: int) -> Parent:
        """Get parent by ID"""
        parent = self.session.get(Parent, parent_id)
        if not parent:
            raise ParentNotFoundError(f"Parent with ID {parent_id} not found")
        return parent
    
    def list_parents(self, student_id: int) -> List[Parent]:
        """List all parents for a student"""
        statement = select(Parent).where(Parent.student_id == student_id)
        return list(self.session.exec(statement).all())
    
    # ----------------------------------------------------------------------
    # Enrollment Management
    # ----------------------------------------------------------------------
    
    def get_enrollment(self, enrollment_id: int) -> Enrollment:
        """Get enrollment by ID"""
        enrollment = self.session.get(Enrollment, enrollment_id)
        if not enrollment:
            raise EnrollmentNotFoundError(f"Enrollment with ID {enrollment_id} not found")
        return enrollment
    
    def list_enrollments(self, student_id: Optional[int] = None) -> List[Enrollment]:
        """List all enrollments"""
        statement = select(Enrollment)
        if student_id:
            statement = statement.where(Enrollment.student_id == student_id)
        return list(self.session.exec(statement).all())
