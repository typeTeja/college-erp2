import os

# Set mock environment variables before any app imports to satisfy pydantic settings
os.environ["DATABASE_URL"] = "postgresql://user:pass@localhost:5432/db"
os.environ["SECRET_KEY"] = "test_secret_key_must_be_long_enough_for_security"
os.environ["BACKEND_BASE_URL"] = "http://localhost:8000"
os.environ["PORTAL_BASE_URL"] = "http://localhost:3000"

import pytest
from unittest.mock import MagicMock
from datetime import date
from sqlmodel import Session, SQLModel

# Ensure all models are registered to avoid relationship resolution errors
from app.models import User, Role, Student
from app.domains.academic.models import AcademicBatch, Section, AcademicYear, Program

from app.domains.academic.services import AcademicService, AcademicValidationService
from app.domains.academic.exceptions import HierarchyValidationError, AcademicYearOverlapError

def test_validate_hierarchy_success():
    session = MagicMock(spec=Session)
    service = AcademicValidationService()
    
    # Mock Batch
    batch = AcademicBatch(id=1, program_id=1, name="Batch 2024")
    session.get.side_effect = lambda model, id: batch if model == AcademicBatch and id == 1 else None
    
    assert service.validate_hierarchy(session, batch_id=1, program_id=1) is True

def test_validate_hierarchy_mismatch():
    session = MagicMock(spec=Session)
    service = AcademicValidationService()
    
    # Mock Batch with different program_id
    batch = AcademicBatch(id=1, program_id=2, name="Batch 2024")
    session.get.side_effect = lambda model, id: batch if model == AcademicBatch and id == 1 else None
    
    with pytest.raises(HierarchyValidationError):
        service.validate_hierarchy(session, batch_id=1, program_id=1)

def test_validate_section_hierarchy_success():
    session = MagicMock(spec=Session)
    service = AcademicValidationService()
    
    # Mock Section
    section = Section(id=1, batch_id=1, name="Section A", code="A", batch_semester_id=1)
    session.get.side_effect = lambda model, id: section if model == Section and id == 1 else None
    
    assert service.validate_hierarchy(session, section_id=1, batch_id=1) is True

def test_validate_academic_year_overlap():
    session = MagicMock(spec=Session)
    service = AcademicValidationService()
    
    # Mock existing year
    existing_year = AcademicYear(id=1, name="2024-25", start_date=date(2024, 6, 1), end_date=date(2025, 5, 31))
    
    # Mock session.exec(statement).first()
    mock_exec = MagicMock()
    mock_exec.first.return_value = existing_year
    session.exec.return_value = mock_exec
    
    with pytest.raises(AcademicYearOverlapError):
        service.validate_academic_year_dates(
            session, 
            start_date=date(2024, 7, 1), 
            end_date=date(2025, 6, 30)
        )

def test_validate_academic_year_valid():
    session = MagicMock(spec=Session)
    service = AcademicValidationService()
    
    # No existing year found (session.exec().first() returns None)
    mock_exec = MagicMock()
    mock_exec.first.return_value = None
    session.exec.return_value = mock_exec
    
    # Should not raise any exception
    service.validate_academic_year_dates(
        session, 
        start_date=date(2025, 6, 1), 
        end_date=date(2026, 5, 31)
    )
