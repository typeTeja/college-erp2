import os
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from sqlmodel import Session

# Set mock environment variables
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/db"
os.environ["SECRET_KEY"] = "test_secret_key_must_be_long_enough_for_security"
os.environ["BACKEND_BASE_URL"] = "http://localhost:8000"
os.environ["PORTAL_BASE_URL"] = "http://localhost:3000"

from app.models import Student # Ensure registration
from app.domains.academic.setup_service import academic_setup_service
from app.domains.academic.models import (
    Subject, SubjectConfig, Regulation, RegulationSubject
)
from app.domains.academic.schemas import (
    SubjectCreate, SubjectConfigCreate, RegulationCreate, RegulationSubjectCreate
)
from app.domains.academic.exceptions import RegulationLockedError

def test_create_subject():
    session = MagicMock(spec=Session)
    data = SubjectCreate(name="Physics", code="PHY101")
    
    subject = academic_setup_service.create_subject(session, data)
    
    assert subject.name == "Physics"
    assert subject.code == "PHY101"
    session.add.assert_called_once()
    session.commit.assert_called_once()

def test_add_subject_to_locked_regulation():
    session = MagicMock(spec=Session)
    
    # Mock a locked regulation
    regulation = Regulation(
        id=1, name="R22", program_id=1, total_credits=160, duration_years=4,
        is_locked=True
    )
    session.get.return_value = regulation
    
    data = RegulationSubjectCreate(subject_id=1, semester=1, credits=3.0)
    
    with pytest.raises(RegulationLockedError):
        academic_setup_service.add_subject_to_regulation(session, 1, data)

def test_lock_regulation():
    session = MagicMock(spec=Session)
    regulation = Regulation(
        id=1, name="R22", program_id=1, total_credits=160, duration_years=4,
        is_locked=False
    )
    session.get.return_value = regulation
    
    updated_reg = academic_setup_service.lock_regulation(session, 1, user_id=1)
    
    assert updated_reg.is_locked is True
    assert updated_reg.locked_by == 1
    assert isinstance(updated_reg.locked_at, datetime)
    session.commit.assert_called_once()
