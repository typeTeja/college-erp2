import os
import pytest
from unittest.mock import MagicMock
from sqlmodel import Session
from app.shared.enums import DayOfWeek

# Set mock environment variables
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/db"
os.environ["SECRET_KEY"] = "test_secret_key_must_be_long_enough_for_security"
os.environ["BACKEND_BASE_URL"] = "http://localhost:8000"
os.environ["PORTAL_BASE_URL"] = "http://localhost:3000"

from app.models import Student
from app.domains.academic.operations_service import academic_operations_service
from app.domains.academic.models import ClassSchedule, TimeSlot
from app.domains.academic.schemas import ClassScheduleCreate, StudentSectionAssignmentCreate
from fastapi import HTTPException

def test_timetable_faculty_conflict():
    session = MagicMock(spec=Session)
    
    # Mock existing entry with same faculty
    existing_entry = ClassSchedule(
        id=1, academic_year_id=1, batch_semester_id=1, 
        day_of_week=DayOfWeek.MONDAY, period_id=1, faculty_id=10
    )
    
    mock_exec = MagicMock()
    mock_exec.first.return_value = existing_entry
    session.exec.return_value = mock_exec
    
    data = ClassScheduleCreate(
        academic_year_id=1, batch_semester_id=2, 
        day_of_week=DayOfWeek.MONDAY, period_id=1, faculty_id=10
    )
    
    with pytest.raises(HTTPException) as exc:
        academic_operations_service.create_timetable_entry(session, data)
    assert exc.value.status_code == 400
    assert "Faculty already assigned" in exc.value.detail

def test_timetable_room_conflict():
    session = MagicMock(spec=Session)
    
    # Mock existing entry with same room
    existing_entry = ClassSchedule(
        id=1, academic_year_id=1, batch_semester_id=1, 
        day_of_week=DayOfWeek.MONDAY, period_id=1, room_id=20
    )
    
    # Mock return values for different checks (Faculty, then Room)
    # First call for faculty conflict might return None
    # Second call for room conflict returns the conflict
    mock_exec = MagicMock()
    mock_exec.first.side_effect = [None, existing_entry]
    session.exec.return_value = mock_exec
    
    data = ClassScheduleCreate(
        academic_year_id=1, batch_semester_id=2, 
        day_of_week=DayOfWeek.MONDAY, period_id=1, room_id=20, faculty_id=11
    )
    
    with pytest.raises(HTTPException) as exc:
        academic_operations_service.create_timetable_entry(session, data)
    assert exc.value.status_code == 400
    assert "Classroom already occupied" in exc.value.detail

def test_student_section_assignment():
    session = MagicMock(spec=Session)
    
    # No existing active assignment
    mock_exec = MagicMock()
    mock_exec.first.return_value = None
    session.exec.return_value = mock_exec
    
    data = StudentSectionAssignmentCreate(student_id=1, section_id=5)
    
    assignment = academic_operations_service.assign_student_to_section(session, data, user_id=100)
    
    assert assignment.student_id == 1
    assert assignment.section_id == 5
    assert assignment.assigned_by == 100
    session.add.assert_called_once()
    session.commit.assert_called_once()
