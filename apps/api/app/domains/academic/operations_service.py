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
    StudentSectionAssignmentCreate
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
        # Check if already assigned
        existing = session.exec(
            select(StudentSectionAssignment).where(
                and_(
                    StudentSectionAssignment.student_id == data.student_id,
                    StudentSectionAssignment.is_active == True
                )
            )
        ).first()

        if existing:
            existing.is_active = False
            session.add(existing)

        db_assignment = StudentSectionAssignment(**data.model_dump())
        if user_id:
            db_assignment.assigned_by = user_id
        
        session.add(db_assignment)
        session.commit()
        session.refresh(db_assignment)
        return db_assignment

academic_operations_service = AcademicOperationsService()
