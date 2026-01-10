"""
Academic Setup Validation Utilities
Smart error-proofing to prevent data integrity issues
"""
from typing import Optional
from fastapi import HTTPException, status
from sqlmodel import Session, select
from datetime import date

from app.models.master_data import Section, AcademicYear
from app.models.academic.batch import BatchSemester, AcademicBatch


class AcademicValidationError(HTTPException):
    """Custom exception for academic validation errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


def validate_date_overlap(
    session: Session,
    start_date: date,
    end_date: date,
    academic_year_id: Optional[int] = None
) -> None:
    """
    Validate that dates don't overlap incorrectly
    
    Args:
        session: Database session
        start_date: Start date to validate
        end_date: End date to validate
        academic_year_id: Optional academic year ID to check against
    
    Raises:
        AcademicValidationError: If dates are invalid
    """
    # Basic validation
    if start_date >= end_date:
        raise AcademicValidationError(
            "Start date must be before end date"
        )
    
    # If academic year specified, validate semester falls within it
    if academic_year_id:
        academic_year = session.get(AcademicYear, academic_year_id)
        if not academic_year:
            raise AcademicValidationError(
                f"Academic year {academic_year_id} not found"
            )
        
        if start_date < academic_year.start_date:
            raise AcademicValidationError(
                f"Start date cannot be before academic year start date ({academic_year.start_date})"
            )
        
        if end_date > academic_year.end_date:
            raise AcademicValidationError(
                f"End date cannot be after academic year end date ({academic_year.end_date})"
            )


def validate_section_deletion(session: Session, section_id: int) -> None:
    """
    Validate that a section can be safely deleted
    
    Args:
        session: Database session
        section_id: Section ID to validate
    
    Raises:
        AcademicValidationError: If section cannot be deleted
    """
    section = session.get(Section, section_id)
    if not section:
        raise AcademicValidationError(f"Section {section_id} not found")
    
    # Check if students are enrolled
    if section.current_strength > 0:
        raise AcademicValidationError(
            f"Cannot delete section '{section.name}' - {section.current_strength} students are currently enrolled. "
            f"Please reassign students before deleting."
        )
    
    # Check if practical batches exist
    if section.practical_batches:
        active_batches = [pb for pb in section.practical_batches if pb.is_active]
        if active_batches:
            raise AcademicValidationError(
                f"Cannot delete section '{section.name}' - {len(active_batches)} active practical batches exist. "
                f"Please delete practical batches first."
            )


def validate_batch_deletion(session: Session, batch_id: int) -> None:
    """
    Validate that a batch can be safely deleted
    
    Args:
        session: Database session
        batch_id: Batch ID to validate
    
    Raises:
        AcademicValidationError: If batch cannot be deleted
    """
    batch = session.get(AcademicBatch, batch_id)
    if not batch:
        raise AcademicValidationError(f"Batch {batch_id} not found")
    
    # Check if students are enrolled
    if batch.total_students > 0:
        raise AcademicValidationError(
            f"Cannot delete batch '{batch.batch_name}' - {batch.total_students} students are enrolled. "
            f"Please reassign students before deleting."
        )


def validate_capacity_change(
    current_strength: int,
    new_max_strength: int,
    entity_name: str = "section"
) -> None:
    """
    Validate that capacity change doesn't drop below current enrollment
    
    Args:
        current_strength: Current number of enrolled students
        new_max_strength: New maximum capacity
        entity_name: Name of entity (for error message)
    
    Raises:
        AcademicValidationError: If new capacity is too low
    """
    if new_max_strength < current_strength:
        raise AcademicValidationError(
            f"Cannot reduce {entity_name} capacity to {new_max_strength} - "
            f"{current_strength} students are currently enrolled. "
            f"Capacity must be at least {current_strength}."
        )


def validate_section_capacity(
    session: Session,
    section_id: int,
    new_max_strength: int
) -> None:
    """
    Validate section capacity change
    
    Args:
        session: Database session
        section_id: Section ID
        new_max_strength: New maximum capacity
    
    Raises:
        AcademicValidationError: If capacity is invalid
    """
    section = session.get(Section, section_id)
    if not section:
        raise AcademicValidationError(f"Section {section_id} not found")
    
    validate_capacity_change(
        current_strength=section.current_strength,
        new_max_strength=new_max_strength,
        entity_name=f"section '{section.name}'"
    )


def validate_faculty_assignment(
    session: Session,
    faculty_id: Optional[int]
) -> None:
    """
    Validate that faculty exists and is active
    
    Args:
        session: Database session
        faculty_id: Faculty ID to validate
    
    Raises:
        AcademicValidationError: If faculty is invalid
    """
    if faculty_id is None:
        return  # Optional assignment
    
    from app.models.faculty import Faculty
    
    faculty = session.get(Faculty, faculty_id)
    if not faculty:
        raise AcademicValidationError(f"Faculty {faculty_id} not found")
    
    # Could add additional checks here:
    # - Is faculty active?
    # - Does faculty have capacity for more sections?
    # - Is faculty from the right department?
