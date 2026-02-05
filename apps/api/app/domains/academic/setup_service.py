from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException

from .models.subject import Subject, SubjectConfig
from .models.regulation import (
    Regulation, 
    RegulationSubject, 
    RegulationSemester, 
    RegulationPromotionRule
)
from .schemas import (
    SubjectCreate, 
    SubjectConfigCreate,
    RegulationCreate,
    RegulationSubjectCreate,
    RegulationSemesterCreate,
    RegulationPromotionRuleCreate
)
from .exceptions import RegulationLockedError, RegulationNotFoundError

class AcademicSetupService:
    """Service for managing Academic Setup (Subjects & Regulations)"""

    @staticmethod
    def create_subject(session: Session, data: SubjectCreate) -> Subject:
        """Create a new global subject"""
        db_subject = Subject(**data.model_dump())
        session.add(db_subject)
        session.commit()
        session.refresh(db_subject)
        return db_subject

    @staticmethod
    def configure_subject(session: Session, data: SubjectConfigCreate) -> SubjectConfig:
        """Add evaluation configuration to a subject"""
        db_config = SubjectConfig(**data.model_dump())
        session.add(db_config)
        session.commit()
        session.refresh(db_config)
        return db_config

    @staticmethod
    def create_regulation(session: Session, data: RegulationCreate, user_id: Optional[int] = None) -> Regulation:
        """Create a new academic regulation"""
        db_regulation = Regulation(**data.model_dump())
        if user_id:
            db_regulation.created_by = user_id
        session.add(db_regulation)
        session.commit()
        session.refresh(db_regulation)
        return db_regulation

    @staticmethod
    def add_subject_to_regulation(session: Session, regulation_id: int, data: RegulationSubjectCreate) -> RegulationSubject:
        """Map a global subject to a specific regulation with credit rules"""
        regulation = session.get(Regulation, regulation_id)
        if not regulation:
            raise RegulationNotFoundError(f"Regulation {regulation_id} not found")
        if regulation.is_locked:
            raise RegulationLockedError(f"Regulation {regulation_id} is locked")

        db_reg_subject = RegulationSubject(
            regulation_id=regulation_id,
            **data.model_dump()
        )
        session.add(db_reg_subject)
        session.commit()
        session.refresh(db_reg_subject)
        return db_reg_subject

    @staticmethod
    def add_semester_rules(session: Session, regulation_id: int, data: RegulationSemesterCreate) -> RegulationSemester:
        """Add credit constraints for a regulation semester"""
        db_semester = RegulationSemester(
            regulation_id=regulation_id,
            **data.model_dump()
        )
        session.add(db_semester)
        session.commit()
        session.refresh(db_semester)
        return db_semester

    @staticmethod
    def add_promotion_rule(session: Session, regulation_id: int, data: RegulationPromotionRuleCreate) -> RegulationPromotionRule:
        """Add promotion logic between years for a regulation"""
        db_rule = RegulationPromotionRule(
            regulation_id=regulation_id,
            **data.model_dump()
        )
        session.add(db_rule)
        session.commit()
        session.refresh(db_rule)
        return db_rule

    @staticmethod
    def list_subjects(session: Session) -> List[Subject]:
        """List all global subjects"""
        return session.exec(select(Subject)).all()

    @staticmethod
    def get_subject(session: Session, subject_id: int) -> Subject:
        """Get subject details"""
        subject = session.get(Subject, subject_id)
        if not subject:
            raise HTTPException(status_code=404, detail="Subject not found")
        return subject

    @staticmethod
    def list_regulations(session: Session, program_id: Optional[int] = None) -> List[Regulation]:
        """List all regulations, optionally filtered by program"""
        statement = select(Regulation)
        if program_id:
            statement = statement.where(Regulation.program_id == program_id)
        return session.exec(statement).all()

    @staticmethod
    def get_regulation(session: Session, regulation_id: int) -> Regulation:
        """Get regulation with all its rules and subjects"""
        regulation = session.get(Regulation, regulation_id)
        if not regulation:
            raise RegulationNotFoundError(f"Regulation {regulation_id} not found")
        return regulation

    @staticmethod
    def lock_regulation(session: Session, regulation_id: int, user_id: int) -> Regulation:
        """Lock regulation to prevent further modification"""
        regulation = session.get(Regulation, regulation_id)
        if not regulation:
            raise RegulationNotFoundError(f"Regulation {regulation_id} not found")
        
        regulation.is_locked = True
        regulation.locked_at = datetime.utcnow()
        regulation.locked_by = user_id
        
        session.add(regulation)
        session.commit()
        session.refresh(regulation)
        return regulation

academic_setup_service = AcademicSetupService()
