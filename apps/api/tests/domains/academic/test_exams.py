import os
import pytest
import json
from unittest.mock import MagicMock
from datetime import date
from sqlmodel import Session

# Set mock environment variables
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/db"
os.environ["SECRET_KEY"] = "test_secret_key_must_be_long_enough_for_security"
os.environ["BACKEND_BASE_URL"] = "http://localhost:8000"
os.environ["PORTAL_BASE_URL"] = "http://localhost:3000"

from app.models import Student
from app.domains.academic.university_exam_service import university_exam_service
from app.domains.academic.models import UniversityExam, UniversityExamRegistration
from app.domains.academic.schemas import UniversityExamRegistrationCreate, UniversityExamCreate

def test_register_student_university_exam():
    session = MagicMock(spec=Session)
    
    # Mock no existing registrations to get first reg number
    # session.exec(statement).all()
    mock_exec = MagicMock()
    mock_exec.all.return_value = []
    session.exec.return_value = mock_exec
    
    data = UniversityExamRegistrationCreate(
        student_id=1,
        university_exam_id=1,
        batch_semester_id=1,
        subjects_registered=[{"subject_id": 1, "code": "CS101"}],
        exam_fee=1000.0,
        total_fee=1000.0
    )
    
    registration = university_exam_service.register_student(session, data)
    
    assert "REG-" in registration.registration_number
    # Verify JSON stringification
    assert "CS101" in registration.subjects_registered
    session.add.assert_called_once()
    session.commit.assert_called_once()

def test_generate_hall_tickets():
    session = MagicMock(spec=Session)
    
    # Mock eligible registration
    reg = UniversityExamRegistration(
        id=1, student_id=10, university_exam_id=1, 
        is_eligible=True, fee_paid=True, hall_ticket_generated=False
    )
    
    mock_exec = MagicMock()
    mock_exec.all.return_value = [reg]
    session.exec.return_value = mock_exec
    
    hall_tickets = university_exam_service.generate_hall_tickets(session, 1)
    
    assert len(hall_tickets) == 1
    assert hall_tickets[0].hall_ticket_generated is True
    assert "HT-1-10" in hall_tickets[0].hall_ticket_number
    session.commit.assert_called_once()
