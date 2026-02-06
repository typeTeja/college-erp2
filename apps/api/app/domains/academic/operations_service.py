from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, and_
from fastapi import HTTPException

from .models.timetable import TimeSlot, Classroom, ClassSchedule
from .models.assignment import StudentSectionAssignment
from .schemas import (
    TimeSlotCreate, 
    ClassroomCreate, 
    ClassScheduleCreate,
    StudentSectionAssignmentCreate,
    AutoAssignRequest
)

class AcademicOperationsService:
    """Service for managing Academic Operations (Timetable & Assignments)"""

    @staticmethod
    def create_timeslot(session: Session, data: TimeSlotCreate) -> TimeSlot:
        """Define a new period/timeslot"""
        db_slot = TimeSlot(**data.model_dump())
        session.add(db_slot)
        session.commit()
        session.refresh(db_slot)
        return db_slot

    @staticmethod
    def create_classroom(session: Session, data: ClassroomCreate) -> Classroom:
        """Register a new classroom"""
        db_room = Classroom(**data.model_dump())
        session.add(db_room)
        session.commit()
        session.refresh(db_room)
        return db_room

    @staticmethod
    def create_timetable_entry(session: Session, data: ClassScheduleCreate) -> ClassSchedule:
        """
        Create a new timetable entry with conflict detection.
        Checks for Faculty, Room, and Section availability.
        """
        # 1. Faculty Conflict Check
        if data.faculty_id:
            faculty_conflict = session.exec(
                select(ClassSchedule).where(
                    and_(
                        ClassSchedule.day_of_week == data.day_of_week,
                        ClassSchedule.period_id == data.period_id,
                        ClassSchedule.faculty_id == data.faculty_id,
                        ClassSchedule.academic_year_id == data.academic_year_id
                    )
                )
            ).first()
            if faculty_conflict:
                raise HTTPException(status_code=400, detail="Faculty already assigned to another class in this slot")

        # 2. Room Conflict Check
        if data.room_id:
            room_conflict = session.exec(
                select(ClassSchedule).where(
                    and_(
                        ClassSchedule.day_of_week == data.day_of_week,
                        ClassSchedule.period_id == data.period_id,
                        ClassSchedule.room_id == data.room_id,
                        ClassSchedule.academic_year_id == data.academic_year_id
                    )
                )
            ).first()
            if room_conflict:
                raise HTTPException(status_code=400, detail="Classroom already occupied in this slot")

        # 3. Section Conflict Check
        if data.section_id:
            section_conflict = session.exec(
                select(ClassSchedule).where(
                    and_(
                        ClassSchedule.day_of_week == data.day_of_week,
                        ClassSchedule.period_id == data.period_id,
                        ClassSchedule.section_id == data.section_id,
                        ClassSchedule.academic_year_id == data.academic_year_id
                    )
                )
            ).first()
            if section_conflict:
                raise HTTPException(status_code=400, detail="Section already has another class scheduled in this slot")

        db_entry = ClassSchedule(**data.model_dump())
        session.add(db_entry)
        session.commit()
        session.refresh(db_entry)
        return db_entry

    @staticmethod
    def list_timeslots(session: Session) -> List[TimeSlot]:
        """List all defined periods/timeslots"""
        return session.exec(select(TimeSlot)).all()

    @staticmethod
    def list_classrooms(session: Session) -> List[Classroom]:
        """List all registered classrooms"""
        return session.exec(select(Classroom)).all()

    @staticmethod
    def list_timetable_entries(
        session: Session, 
        academic_year_id: int, 
        batch_semester_id: Optional[int] = None,
        section_id: Optional[int] = None
    ) -> List[ClassSchedule]:
        """Fetch timetable with filters"""
        statement = select(ClassSchedule).where(ClassSchedule.academic_year_id == academic_year_id)
        if batch_semester_id:
            statement = statement.where(ClassSchedule.batch_semester_id == batch_semester_id)
        if section_id:
            statement = statement.where(ClassSchedule.section_id == section_id)
        return session.exec(statement).all()

    @staticmethod
    def assign_student_to_section(session: Session, data: StudentSectionAssignmentCreate, user_id: Optional[int] = None) -> StudentSectionAssignment:
        """Assign or move a student to a section"""
        from app.domains.student.models import Student

        # 1. Deactivate existing active assignment for this student/semester context
        # Note: We assume one section per semester.
        existing = session.exec(
            select(StudentSectionAssignment).where(
                and_(
                    StudentSectionAssignment.student_id == data.student_id,
                    StudentSectionAssignment.is_active == True
                )
            )
        ).all()

        for assignment in existing:
            assignment.is_active = False
            session.add(assignment)

        # 2. Create new assignment history log
        db_assignment = StudentSectionAssignment(**data.model_dump())
        if user_id:
            db_assignment.assigned_by = user_id
        
        session.add(db_assignment)

        # 3. CRITICAL: Update the Student Entity to reflect current section
        student = session.get(Student, data.student_id)
        if student:
            student.section_id = data.section_id
            # We assume the section belongs to the correct batch_semester. 
            # Ideally we should validate this or fetch from section -> batch_semester
            from app.domains.academic.models.setup import Section
            section = session.get(Section, data.section_id)
            if section:
                student.batch_semester_id = section.batch_semester_id
            
            session.add(student)
        
        session.commit()
        session.refresh(db_assignment)
        return db_assignment

    @staticmethod
    def auto_assign_students(session: Session, batch_id: int, semester_no: int, user_id: Optional[int] = None) -> dict:
        """
        Auto-assign unassigned students to sections in a round-robin fashion.
        """
        from app.domains.student.models import Student
        from app.domains.academic.models.setup import Section
        from app.domains.academic.models.batch import BatchSemester
        
        # 1. Find the BatchSemester for this batch + semester_no
        batch_semester = session.exec(
            select(BatchSemester).where(
                and_(
                    BatchSemester.batch_id == batch_id,
                    BatchSemester.semester_no == semester_no
                )
            )
        ).first()

        if not batch_semester:
            raise HTTPException(status_code=404, detail="Batch Semester not found")

        # 2. Get available sections
        sections = session.exec(
            select(Section).where(
                and_(
                    Section.batch_semester_id == batch_semester.id,
                    Section.is_active == True
                )
            )
        ).all()

        if not sections:
            raise HTTPException(status_code=400, detail="No active sections found for this semester")

        # 3. Get unassigned students in this batch
        # Logic: Active students in batch, having NO section_id OR section_id not in current semester sections?
        # Simpler: Student.batch_id == batch_id AND Student.section_id IS NULL
        students = session.exec(
            select(Student).where(
                and_(
                    Student.batch_id == batch_id,
                    Student.status == "ACTIVE",
                    Student.section_id == None
                )
            ).order_by(Student.name) # Alphabetical or Roll No
        ).all()

        if not students:
            return {"message": "No unassigned students found", "assigned_count": 0}

        # 4. Round Robin Assignment
        assigned_count = 0
        section_count = len(sections)
        
        for i, student in enumerate(students):
            target_section = sections[i % section_count]
            
            # Create Assignment Record
            assignment = StudentSectionAssignment(
                student_id=student.id,
                section_id=target_section.id,
                assignment_type="AUTO",
                assigned_by=user_id
            )
            session.add(assignment)

            # Update Student Record
            student.section_id = target_section.id
            student.batch_semester_id = batch_semester.id
            session.add(student)
            
            assigned_count += 1

        session.commit()

        return {
            "message": "Auto-assignment completed successfully", 
            "assigned_count": assigned_count,
            "unassigned_count": 0
        }

    @staticmethod
    def get_unassigned_students_count(session: Session, batch_id: int, semester_no: int) -> int:
        """Count unassigned students for a batch"""
        from app.domains.student.models import Student
        
        count = session.exec(
            select(Student).where(
                and_(
                    Student.batch_id == batch_id,
                    Student.status == "ACTIVE",
                    Student.section_id == None
                )
            )
        ).all()
        
        return len(count)

academic_operations_service = AcademicOperationsService()
