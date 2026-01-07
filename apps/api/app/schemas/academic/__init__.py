"""
Academic schemas package
"""
from .regulation import (
    RegulationCreate,
    RegulationUpdate,
    RegulationRead,
    RegulationSubjectCreate,
    RegulationSubjectUpdate,
    RegulationSubjectRead,
    RegulationSemesterCreate,
    RegulationSemesterRead,
    RegulationPromotionRuleCreate,
    RegulationPromotionRuleRead
)
from .batch import (
    AcademicBatchCreate,
    AcademicBatchUpdate,
    AcademicBatchRead,
    AcademicBatchWithDetails,
    ProgramYearRead,
    BatchSemesterRead,
    BatchSubjectRead
)

__all__ = [
    "RegulationCreate",
    "RegulationUpdate",
    "RegulationRead",
    "RegulationSubjectCreate",
    "RegulationSubjectUpdate",
    "RegulationSubjectRead",
    "RegulationSemesterCreate",
    "RegulationSemesterRead",
    "RegulationPromotionRuleCreate",
    "RegulationPromotionRuleRead",
    "AcademicBatchCreate",
    "AcademicBatchUpdate",
    "AcademicBatchRead",
    "AcademicBatchWithDetails",
    "ProgramYearRead",
    "BatchSemesterRead",
    "BatchSubjectRead"
]
