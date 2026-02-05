import hashlib
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select, and_

from .models.regulation import Regulation, RegulationSubject, RegulationSemester, RegulationPromotionRule
from .models.batch import AcademicBatch, BatchSemester, BatchSubject, BatchPromotionRule, BatchRuleOverride
from .schemas import BatchRuleOverrideCreate
from app.shared.enums import BatchStatus, SemesterStatus

class AcademicEngineService:
    """
    University-Grade Academic Engine.
    Handles critical logic for rule freezing, audit safety, and promotion evaluation.
    """

    @staticmethod
    def _generate_regulation_checksum(
        regulation: Regulation, 
        subjects: List[RegulationSubject], 
        semesters: List[RegulationSemester],
        rules: List[RegulationPromotionRule]
    ) -> str:
        """Generate a deterministic hash of regulation rules for audit safety."""
        data = {
            "name": regulation.name,
            "version": regulation.regulation_version,
            "subjects": [
                {
                    "id": s.subject_id,
                    "credits": s.credits,
                    "max_marks": s.max_marks,
                    "internal_max": s.internal_max,
                    "external_max": s.external_max,
                    "hall_ticket": s.counts_for_hall_ticket,
                    "promotion": s.counts_for_promotion
                } for s in subjects
            ],
            "semesters": [{"sem": sem.semester, "credits": sem.total_credits} for sem in semesters],
            "promotion_rules": [{"from": r.from_year, "to": r.to_year, "type": r.rule_type} for r in rules]
        }
        serialized = json.dumps(data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()

    @staticmethod
    def freeze_regulation_to_batch(session: Session, batch_id: int, user_id: int) -> AcademicBatch:
        """
        [ATOMIC] Copy and Freeze Regulation rules into the Batch layer.
        Once called, the batch is independent of future Regulation changes.
        """
        batch = session.get(AcademicBatch, batch_id)
        if not batch:
            raise ValueError(f"Batch {batch_id} not found")
        
        regulation = session.get(Regulation, batch.regulation_id)
        if not regulation:
            raise ValueError(f"Regulation {batch.regulation_id} not found")

        # 1. Capture snapshots of all regulation rules
        subjects = regulation.subjects
        semesters = regulation.semesters
        prom_rules = regulation.promotion_rules

        # 2. Generate Audit Checksum
        checksum = AcademicEngineService._generate_regulation_checksum(
            regulation, subjects, semesters, prom_rules
        )

        # 3. Freeze Semesters
        for reg_sem in semesters:
            batch_sem = BatchSemester(
                batch_id=batch.id,
                semester_number=reg_sem.semester,
                academic_year_id=batch.admission_year_id, # Default, will be updated per sem
                start_date=datetime.utcnow(), # Placeholder
                end_date=datetime.utcnow(),   # Placeholder
                total_credits=reg_sem.total_credits,
                min_credits=reg_sem.min_credits,
                status=SemesterStatus.UPCOMING
            )
            session.add(batch_sem)
            session.flush() # Get ID for subjects

            # 4. Freeze Subjects for this semester
            sem_subjects = [s for s in subjects if s.semester == reg_sem.semester]
            for reg_sub in sem_subjects:
                batch_sub = BatchSubject(
                    batch_semester_id=batch_sem.id,
                    subject_id=reg_sub.subject_id,
                    regulation_subject_id=reg_sub.id,
                    credits=reg_sub.credits,
                    subject_type=reg_sub.subject_type,
                    evaluation_type=reg_sub.evaluation_type,
                    max_marks=reg_sub.max_marks,
                    internal_max=reg_sub.internal_max,
                    external_max=reg_sub.external_max,
                    counts_for_hall_ticket=reg_sub.counts_for_hall_ticket,
                    counts_for_promotion=reg_sub.counts_for_promotion
                )
                session.add(batch_sub)

        # 5. Freeze Promotion Rules
        for reg_prom in prom_rules:
            batch_prom = BatchPromotionRule(
                batch_id=batch.id,
                from_year=reg_prom.from_year,
                to_year=reg_prom.to_year,
                rule_type=reg_prom.rule_type,
                min_credits_required=reg_prom.min_credits_required,
                min_credit_percentage_required=reg_prom.min_credit_percentage_required,
                max_backlogs_allowed=reg_prom.max_backlogs_allowed
            )
            session.add(batch_prom)

        # 6. Update Batch Metadata
        batch.regulation_code = regulation.name
        batch.frozen_at = datetime.utcnow()
        batch.frozen_by_id = user_id
        batch.freeze_checksum = checksum
        
        session.add(batch)
        session.commit()
        session.refresh(batch)
        return batch

    @staticmethod
    def evaluate_promotion(
        session: Session, 
        student_id: int, 
        target_year: int, 
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluate student promotion eligibility strictly based on frozen batch rules.
        """
        # 1. Fetch Student and Batch
        # (Assuming Student model has batch enrichment)
        # This is a conceptual implementation of logic
        
        # logic: 
        # - find student.batch_id
        # - find BatchPromotionRule for from_year (target_year - 1) to target_year
        # - count earned credits from previous semesters
        # - compare with rule requirements
        
        return {
            "eligible": True, # Placeholder
            "dry_run": dry_run,
            "earned_credits": 0,
            "required_credits": 0,
            "violations": []
        }

    @staticmethod
    def apply_rule_override(session: Session, data: BatchRuleOverrideCreate) -> BatchRuleOverride:
        """Admin override for frozen academic rules (With mandatory audit trail)."""
        override = BatchRuleOverride(**data.model_dump())
        session.add(override)
        session.commit()
        session.refresh(override)
        return override

academic_engine = AcademicEngineService()
