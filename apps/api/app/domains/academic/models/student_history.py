"""
Student History Models - Academic Progression Tracking

CRITICAL CORRECTIONS APPLIED:
1. StudentCreditTracker REMOVED (merged into StudentSemesterHistory)
2. Single source of truth for semester progression
3. Promotion transaction order: History → Logs → Student → Commit
"""
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import DECIMAL, Text, UniqueConstraint

if TYPE_CHECKING:
    from app.models.student import Student
    from .batch import AcademicBatch
    from .regulation import Regulation


class StudentSemesterHistory(SQLModel, table=True):
    """
    SINGLE SOURCE OF TRUTH for student academic progression
    
    Combines:
    - Semester history (academic timeline)
    - Credit tracking (earned/failed credits)
    
    CRITICAL: This is the ONLY table for credit tracking
    StudentCreditTracker has been REMOVED
    """
    __tablename__ = "student_semester_history"
    __table_args__ = (
        UniqueConstraint('student_id', 'academic_year_id', 'semester_no', name='uq_student_semester'),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Student links
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    academic_year_id: int = Field(foreign_key="academic_year.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Semester identification
    program_year: int = Field(ge=1, le=5)  # 1, 2, 3
    semester_no: int = Field(ge=1, le=10)  # 1-6 typically
    
    # CREDIT TRACKING (merged from StudentCreditTracker)
    total_credits: int = Field(default=0, ge=0)
    earned_credits: int = Field(default=0, ge=0)
    failed_credits: int = Field(default=0, ge=0)
    
    # Status
    status: str = Field(max_length=20)  # PROMOTED, DETAINED, REPEAT, READMISSION
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="semester_history")
    batch: "AcademicBatch" = Relationship()
    regulation: "Regulation" = Relationship()
    
    @property
    def credit_percentage(self) -> Decimal:
        """
        Calculate credit percentage with precision
        Uses Decimal to avoid floating-point errors
        """
        if self.total_credits == 0:
            return Decimal('0.00')
        
        pct = (Decimal(str(self.earned_credits)) / Decimal(str(self.total_credits))) * 100
        return pct.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @property
    def is_passed(self) -> bool:
        """Check if student passed this semester"""
        return self.status == "PROMOTED"


class StudentPromotionLog(SQLModel, table=True):
    """
    Log of all promotion/detention decisions
    
    CRITICAL: This is written BEFORE student record is updated
    Ensures audit trail exists even if transaction fails
    """
    __tablename__ = "student_promotion_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    regulation_id: int = Field(foreign_key="regulations.id", index=True)
    
    # Promotion details
    from_year: int = Field(ge=1, le=5)
    to_year: int = Field(ge=1, le=5)
    from_semester: int = Field(ge=1, le=10)
    to_semester: int = Field(ge=1, le=10)
    
    # Decision
    status: str = Field(max_length=20)  # PROMOTED, DETAINED, REPEAT
    reason: str = Field(sa_column=Column(Text))
    
    # Credits summary
    year_total_credits: int = Field(default=0, ge=0)
    year_earned_credits: int = Field(default=0, ge=0)
    year_failed_credits: int = Field(default=0, ge=0)
    year_percentage: Optional[Decimal] = Field(
        default=None,
        sa_column=Column(DECIMAL(5, 2))
    )
    
    # Decision maker
    decided_by: int = Field(foreign_key="user.id")
    decided_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship(back_populates="promotion_logs")
    batch: "AcademicBatch" = Relationship()
    regulation: "Regulation" = Relationship()


class StudentRegulationMigration(SQLModel, table=True):
    """
    Track regulation changes for students
    
    Rare but important: When a student switches regulations
    (e.g., university changes regulation mid-course)
    """
    __tablename__ = "student_regulation_migrations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Migration details
    from_regulation_id: int = Field(foreign_key="regulations.id")
    to_regulation_id: int = Field(foreign_key="regulations.id")
    
    migration_date: datetime = Field(default_factory=datetime.utcnow)
    reason: str = Field(sa_column=Column(Text))
    
    # Approval
    approved_by: int = Field(foreign_key="user.id")
    approved_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()


# ============================================================================
# Promotion Eligibility Check (Business Logic)
# ============================================================================

class PromotionEligibility:
    """
    Check if student is eligible for promotion
    
    Based on regulation rules and credit requirements
    """
    
    @staticmethod
    def check_year_promotion(
        student_id: int,
        current_year: int,
        regulation,
        session
    ) -> dict:
        """
        Check if student can be promoted to next year
        
        Returns:
        {
            "eligible": bool,
            "message": str,
            "year_total_credits": int,
            "year_earned_credits": int,
            "year_failed_credits": int,
            "year_percentage": Decimal
        }
        """
        from sqlmodel import select, func
        
        # Get all semesters for current year
        start_semester = (current_year - 1) * 2 + 1
        end_semester = current_year * 2
        
        # Get semester history for current year
        history_records = session.exec(
            select(StudentSemesterHistory)
            .where(StudentSemesterHistory.student_id == student_id)
            .where(StudentSemesterHistory.program_year == current_year)
            .where(StudentSemesterHistory.semester_no.between(start_semester, end_semester))
        ).all()
        
        if not history_records:
            return {
                "eligible": False,
                "message": "No semester history found for current year",
                "year_total_credits": 0,
                "year_earned_credits": 0,
                "year_failed_credits": 0,
                "year_percentage": Decimal('0.00')
            }
        
        # Calculate year totals
        year_total_credits = sum(h.total_credits for h in history_records)
        year_earned_credits = sum(h.earned_credits for h in history_records)
        year_failed_credits = sum(h.failed_credits for h in history_records)
        
        # Calculate percentage
        if year_total_credits == 0:
            year_percentage = Decimal('0.00')
        else:
            year_percentage = (
                Decimal(str(year_earned_credits)) / Decimal(str(year_total_credits))
            ) * 100
            year_percentage = year_percentage.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Get promotion rule
        if current_year == 1:
            min_percentage = regulation.year1_to_year2_min_percentage
        elif current_year == 2:
            min_percentage = regulation.year2_to_year3_min_year2_percentage
        else:
            min_percentage = regulation.year3_to_graduation_min_percentage
        
        # Check eligibility
        eligible = year_percentage >= min_percentage
        
        if eligible:
            message = f"Eligible for promotion. Earned {year_percentage}% (required: {min_percentage}%)"
        else:
            message = f"Not eligible. Earned {year_percentage}% (required: {min_percentage}%)"
        
        return {
            "eligible": eligible,
            "message": message,
            "year_total_credits": year_total_credits,
            "year_earned_credits": year_earned_credits,
            "year_failed_credits": year_failed_credits,
            "year_percentage": year_percentage
        }
