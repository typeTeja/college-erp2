"""
Academic Domain Services

Business logic for academic domain.
Note: This is a simplified version. Full services can be added as needed.
"""

from typing import List, Optional
from sqlmodel import Session, select

from app.domains.academic.models import (
    AcademicYear, AcademicBatch, Regulation, Section,
    Exam, AttendanceRecord
)
from app.domains.academic.schemas import (
    AcademicYearCreate, BatchCreate, RegulationCreate,
    SectionCreate, ExamCreate, AttendanceRecordCreate
)
from app.domains.academic.exceptions import (
    AcademicYearNotFoundError, BatchNotFoundError,
    RegulationNotFoundError, SectionNotFoundError,
    ExamNotFoundError, AttendanceNotFoundError
)


class AcademicService:
    """Service for academic domain operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    # ----------------------------------------------------------------------
    # Academic Year Management
    # ----------------------------------------------------------------------
    
    def get_academic_year(self, year_id: int) -> AcademicYear:
        """Get academic year by ID"""
        year = self.session.get(AcademicYear, year_id)
        if not year:
            raise AcademicYearNotFoundError(f"Academic year with ID {year_id} not found")
        return year
    
    def list_academic_years(self) -> List[AcademicYear]:
        """List all academic years"""
        statement = select(AcademicYear).order_by(AcademicYear.start_date.desc())
        return list(self.session.exec(statement).all())
    
    def create_academic_year(self, year_data: AcademicYearCreate) -> AcademicYear:
        """Create a new academic year"""
        year = AcademicYear(**year_data.model_dump())
        self.session.add(year)
        self.session.commit()
        self.session.refresh(year)
        return year
    
    # ----------------------------------------------------------------------
    # Batch Management
    # ----------------------------------------------------------------------
    
    def get_batch(self, batch_id: int) -> AcademicBatch:
        """Get batch by ID"""
        batch = self.session.get(AcademicBatch, batch_id)
        if not batch:
            raise BatchNotFoundError(f"Batch with ID {batch_id} not found")
        return batch
    
    def list_batches(self, program_id: Optional[int] = None) -> List[AcademicBatch]:
        """List all batches"""
        statement = select(AcademicBatch)
        if program_id:
            statement = statement.where(AcademicBatch.program_id == program_id)
        return list(self.session.exec(statement).all())
    
    # ----------------------------------------------------------------------
    # Regulation Management
    # ----------------------------------------------------------------------
    
    def get_regulation(self, regulation_id: int) -> Regulation:
        """Get regulation by ID"""
        regulation = self.session.get(Regulation, regulation_id)
        if not regulation:
            raise RegulationNotFoundError(f"Regulation with ID {regulation_id} not found")
        return regulation
    
    def list_regulations(self, program_id: Optional[int] = None) -> List[Regulation]:
        """List all regulations"""
        statement = select(Regulation)
        if program_id:
            statement = statement.where(Regulation.program_id == program_id)
        return list(self.session.exec(statement).all())
    
    # ----------------------------------------------------------------------
    # Section Management
    # ----------------------------------------------------------------------
    
    def get_section(self, section_id: int) -> Section:
        """Get section by ID"""
        section = self.session.get(Section, section_id)
        if not section:
            raise SectionNotFoundError(f"Section with ID {section_id} not found")
        return section
    
    def list_sections(self, batch_id: Optional[int] = None) -> List[Section]:
        """List all sections"""
        statement = select(Section)
        if batch_id:
            statement = statement.where(Section.batch_id == batch_id)
        return list(self.session.exec(statement).all())


# ======================================================================
# Academic Validation Service
# ======================================================================

class AcademicValidationService:
    """Service for validating academic hierarchy and relationships"""
    
    @staticmethod
    def validate_hierarchy(
        session: Session,
        batch_id: Optional[int] = None,
        program_year_id: Optional[int] = None,
        batch_semester_id: Optional[int] = None,
        section_id: Optional[int] = None
    ) -> bool:
        """
        Validates the academic hierarchy relationships.
        Ensures that batch -> program_year -> batch_semester -> section relationships are valid.
        """
        # Basic validation logic
        if batch_id:
            batch = session.get(AcademicBatch, batch_id)
            if not batch:
                raise ValueError(f"Batch with ID {batch_id} not found")
        
        # Add more validation logic as needed
        return True


# Create singleton instance for backward compatibility
academic_validation_service = AcademicValidationService()
