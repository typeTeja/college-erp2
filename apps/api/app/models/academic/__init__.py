"""
Academic models package
Contains regulation, batch, and student history models
"""
from .regulation import (
    Regulation,
    RegulationSubject,
    RegulationSemester,
    RegulationPromotionRule
)
from .batch import (
    AcademicBatch,
    BatchSubject,
    BatchSemester,
    ProgramYear
)
from .student_history import (
    StudentSemesterHistory,
    StudentPromotionLog,
    StudentRegulationMigration,
    PromotionEligibility
)

__all__ = [
    "Regulation",
    "RegulationSubject", 
    "RegulationSemester",
    "RegulationPromotionRule",
    "AcademicBatch",
    "BatchSubject",
    "BatchSemester",
    "ProgramYear",
    "StudentSemesterHistory",
    "StudentPromotionLog",
    "StudentRegulationMigration",
    "PromotionEligibility"
]
