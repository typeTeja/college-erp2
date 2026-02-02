"""
Batch Cloning Service
Clones existing batch structures for new academic years
"""
from typing import Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException, status, Request

from app.models.program import Program
from app.domains.academic.models import AcademicBatch, ProgramYear, BatchSemester, Regulation, RegulationSemester, Section, PracticalBatch
from app.schemas.batch_cloning import BatchCloneRequest, BatchCloneResponse, CloneOptions
from app.utils.audit import log_create


class BatchCloningService:
    """Service for batch cloning operations"""
    
    @staticmethod
    def clone_batch(
        session: Session,
        source_batch_id: int,
        request: BatchCloneRequest,
        user_id: int,
        http_request: Request | None = None
    ) -> BatchCloneResponse:
        """
        Clone an existing batch structure for a new academic year
        
        Steps:
        1. Validate source batch exists
        2. Validate new regulation
        3. Create new batch
        4. Clone program years
        5. Clone semesters
        6. Clone sections (with capacity adjustments)
        7. Clone labs (with capacity adjustments)
        8. Optionally clone faculty assignments
        9. Log audit trail
        
        Args:
            session: Database session
            source_batch_id: ID of batch to clone
            request: Clone request with options
            user_id: User performing the clone
            http_request: HTTP request for audit logging
            
        Returns:
            BatchCloneResponse with statistics
        """
        # Step 1: Validate source batch
        source_batch = session.get(AcademicBatch, source_batch_id)
        if not source_batch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Source batch {source_batch_id} not found"
            )
        
        # Get source program
        program = session.get(Program, source_batch.program_id)
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Program {source_batch.program_id} not found"
            )
        
        # Step 2: Validate new regulation
        new_regulation = session.get(Regulation, request.new_regulation_id)
        if not new_regulation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Regulation {request.new_regulation_id} not found"
            )
        
        # Ensure regulation belongs to the same program
        if new_regulation.program_id != program.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Regulation must belong to program {program.code}"
            )
        
        # Step 3: Check for duplicate batch
        end_year = request.new_joining_year + program.duration_years
        new_batch_code = f"{request.new_joining_year}-{end_year}"
        
        existing = session.exec(
            select(AcademicBatch).where(AcademicBatch.batch_code == new_batch_code)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Batch '{new_batch_code}' already exists"
            )
        
        # Step 4: Create new batch
        new_batch_name = request.clone_options.custom_batch_name or f"Batch {new_batch_code}"
        
        new_batch = AcademicBatch(
            batch_code=new_batch_code,
            batch_name=new_batch_name,
            program_id=program.id,
            regulation_id=request.new_regulation_id,
            joining_year=request.new_joining_year,
            start_year=request.new_joining_year,
            end_year=end_year,
            current_year=1,
            total_students=0,
            status="active",
            is_active=True,
            created_by=user_id
        )
        session.add(new_batch)
        session.flush()
        
        # Audit log
        log_create(
            session=session,
            table_name="academic_batch",
            record_id=new_batch.id,
            new_values={
                "batch_code": new_batch.batch_code,
                "source_batch_id": source_batch_id,
                "cloned": True
            },
            user_id=user_id,
            request=http_request
        )
        
        # Step 5: Clone program years
        source_years = session.exec(
            select(ProgramYear)
            .where(ProgramYear.batch_id == source_batch_id)
            .order_by(ProgramYear.year_no)
        ).all()
        
        year_mapping = {}  # Map old year IDs to new year IDs
        for source_year in source_years:
            new_year = ProgramYear(
                batch_id=new_batch.id,
                year_no=source_year.year_no,
                year_name=source_year.year_name
            )
            session.add(new_year)
            session.flush()
            year_mapping[source_year.id] = new_year.id
        
        # Step 6: Clone semesters
        source_semesters = session.exec(
            select(BatchSemester)
            .where(BatchSemester.batch_id == source_batch_id)
            .order_by(BatchSemester.semester_no)
        ).all()
        
        semester_mapping = {}  # Map old semester IDs to new semester IDs
        for source_sem in source_semesters:
            new_sem = BatchSemester(
                batch_id=new_batch.id,
                program_year_id=year_mapping.get(source_sem.program_year_id),
                year_no=source_sem.year_no,
                semester_no=source_sem.semester_no,
                semester_name=source_sem.semester_name,
                total_credits=source_sem.total_credits,
                min_credits_to_pass=source_sem.min_credits_to_pass
            )
            session.add(new_sem)
            session.flush()
            semester_mapping[source_sem.id] = new_sem.id
        
        # Step 7: Clone sections
        source_sections = session.exec(
            select(Section)
            .where(Section.batch_id == source_batch_id)
        ).all()
        
        section_mapping = {}  # Map old section IDs to new section IDs
        sections_created = 0
        
        for source_section in source_sections:
            # Apply capacity multiplier
            new_capacity = int(
                source_section.max_strength * request.clone_options.section_capacity_multiplier
            )
            
            new_section = Section(
                name=source_section.name,
                code=source_section.code,
                batch_semester_id=semester_mapping.get(source_section.batch_semester_id),
                batch_id=new_batch.id,
                faculty_id=source_section.faculty_id if request.clone_options.clone_faculty_assignments else None,
                max_strength=new_capacity,
                current_strength=0,  # Start with 0 students
                is_active=True
            )
            session.add(new_section)
            session.flush()
            section_mapping[source_section.id] = new_section.id
            sections_created += 1
        
        # Step 8: Clone labs
        source_labs = session.exec(
            select(PracticalBatch)
            .where(PracticalBatch.section_id.in_(list(section_mapping.keys())))
        ).all()
        
        labs_created = 0
        for source_lab in source_labs:
            # Apply capacity multiplier
            new_lab_capacity = int(
                source_lab.max_strength * request.clone_options.lab_capacity_multiplier
            )
            
            new_lab = PracticalBatch(
                name=source_lab.name,
                code=source_lab.code,
                section_id=section_mapping.get(source_lab.section_id),
                max_strength=new_lab_capacity,
                current_strength=0,  # Start with 0 students
                is_active=True
            )
            session.add(new_lab)
            labs_created += 1
        
        # Commit all changes
        session.commit()
        session.refresh(new_batch)
        
        return BatchCloneResponse(
            batch_id=new_batch.id,
            batch_code=new_batch.batch_code,
            batch_name=new_batch.batch_name,
            source_batch_id=source_batch_id,
            years_created=len(source_years),
            semesters_created=len(source_semesters),
            sections_created=sections_created,
            labs_created=labs_created,
            message=f"Successfully cloned batch {source_batch.batch_code} to {new_batch.batch_code}"
        )
