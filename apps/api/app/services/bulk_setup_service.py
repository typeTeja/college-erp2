"""
Bulk Batch Setup Service
Handles one-click creation of entire academic structure
"""
from typing import Dict, Any, List
from sqlmodel import Session, select
from fastapi import HTTPException, status, Request

from app.models.program import Program
from app.models.academic.batch import AcademicBatch, ProgramYear, BatchSemester
from app.models.academic.regulation import Regulation, RegulationSemester
from app.models.master_data import Section, PracticalBatch
from app.schemas.bulk_setup import BulkBatchSetupRequest, BulkBatchSetupResponse
from app.utils.audit import log_create


class BulkBatchSetupService:
    """Service for bulk batch setup operations"""
    
    @staticmethod
    def create_bulk_batch(
        session: Session,
        request: BulkBatchSetupRequest,
        user_id: int,
        http_request: Request | None = None
    ) -> BulkBatchSetupResponse:
        """
        Create complete academic structure in one operation
        
        Steps:
        1. Validate program and regulation
        2. Create AcademicBatch
        3. Auto-generate ProgramYears
        4. Auto-generate BatchSemesters (from regulation)
        5. Auto-generate Sections
        6. Auto-generate PracticalBatches (labs)
        
        Args:
            session: Database session
            request: Bulk setup request
            user_id: User creating the batch
            
        Returns:
            BulkBatchSetupResponse with statistics
        """
        # Step 1: Validate program
        program = session.get(Program, request.program_id)
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Program {request.program_id} not found"
            )
        
        # Step 2: Validate regulation
        regulation = session.get(Regulation, request.regulation_id)
        if not regulation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Regulation {request.regulation_id} not found"
            )
        
        # Ensure regulation belongs to the program
        if regulation.program_id != program.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Regulation {regulation.regulation_code} does not belong to program {program.code}"
            )
        
        # Step 3: Check for duplicate batch
        existing_batch = session.exec(
            select(AcademicBatch).where(
                AcademicBatch.program_id == program.id,
                AcademicBatch.joining_year == request.joining_year
            )
        ).first()
        
        if existing_batch:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Batch already exists for {program.code} joining year {request.joining_year}"
            )
        
        # Step 4: Create AcademicBatch
        end_year = request.joining_year + program.duration_years
        batch_code = f"{request.joining_year}-{end_year}"
        batch_name = request.batch_name_override or f"Batch {batch_code}"
        
        batch = AcademicBatch(
            batch_code=batch_code,
            batch_name=batch_name,
            program_id=program.id,
            regulation_id=regulation.id,
            joining_year=request.joining_year,
            start_year=request.joining_year,
            end_year=end_year,
            current_year=1,
            total_students=0,
            status="active",
            is_active=True,
            created_by=user_id
        )
        session.add(batch)
        session.flush()  # Get batch.id
        
        # Audit log batch creation
        log_create(
            session=session,
            table_name="academic_batch",
            record_id=batch.id,
            new_values={
                "batch_code": batch.batch_code,
                "batch_name": batch.batch_name,
                "program_id": batch.program_id,
                "regulation_id": batch.regulation_id,
                "joining_year": batch.joining_year
            },
            user_id=user_id,
            request=http_request
        )
        
        # Step 5: Auto-generate ProgramYears
        program_years = []
        for year_no in range(1, program.duration_years + 1):
            year_name = BulkBatchSetupService._get_year_name(year_no)
            program_year = ProgramYear(
                batch_id=batch.id,
                year_no=year_no,
                year_name=year_name
            )
            session.add(program_year)
            program_years.append(program_year)
        
        session.flush()  # Get program_year IDs
        
        # Audit log program year creation
        for program_year in program_years:
            log_create(
                session=session,
                table_name="program_year",
                record_id=program_year.id,
                new_values={
                    "batch_id": program_year.batch_id,
                    "year_no": program_year.year_no,
                    "year_name": program_year.year_name
                },
                user_id=user_id,
                request=http_request
            )
        
        # Step 6: Auto-generate BatchSemesters from regulation
        regulation_semesters = session.exec(
            select(RegulationSemester)
            .where(RegulationSemester.regulation_id == regulation.id)
            .order_by(RegulationSemester.semester_no)
        ).all()
        
        if not regulation_semesters:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Regulation {regulation.regulation_code} has no semesters defined"
            )
        
        batch_semesters = []
        for reg_sem in regulation_semesters:
            # Find corresponding program year
            program_year = next(
                (py for py in program_years if py.year_no == reg_sem.year_no),
                None
            )
            if not program_year:
                continue
            
            batch_semester = BatchSemester(
                batch_id=batch.id,
                program_year_id=program_year.id,
                year_no=reg_sem.year_no,
                semester_no=reg_sem.semester_no,
                semester_name=reg_sem.semester_name,
                total_credits=reg_sem.total_credits,
                min_credits_to_pass=reg_sem.min_credits_to_pass
            )
            session.add(batch_semester)
            batch_semesters.append(batch_semester)
        
        session.flush()  # Get batch_semester IDs
        
        # Audit log batch semester creation
        for batch_semester in batch_semesters:
            log_create(
                session=session,
                table_name="batch_semester",
                record_id=batch_semester.id,
                new_values={
                    "batch_id": batch_semester.batch_id,
                    "semester_no": batch_semester.semester_no,
                    "semester_name": batch_semester.semester_name,
                    "total_credits": batch_semester.total_credits
                },
                user_id=user_id,
                request=http_request
            )
        
        # Step 7: Auto-generate Sections
        sections_created = 0
        section_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        sections = []
        for batch_semester in batch_semesters:
            for i in range(request.sections_per_semester):
                if i >= len(section_letters):
                    break
                
                section_code = section_letters[i]
                section_name = f"Section {section_code}"
                
                section = Section(
                    name=section_name,
                    code=section_code,
                    batch_semester_id=batch_semester.id,
                    batch_id=batch.id,
                    max_strength=request.section_capacity,
                    current_strength=0,
                    is_active=True
                )
                session.add(section)
                sections.append(section)
                sections_created += 1
        
        session.flush()  # Get section IDs
        
        # Audit log section creation
        for section in sections:
            log_create(
                session=session,
                table_name="section",
                record_id=section.id,
                new_values={
                    "name": section.name,
                    "code": section.code,
                    "batch_semester_id": section.batch_semester_id,
                    "max_strength": section.max_strength
                },
                user_id=user_id,
                request=http_request
            )
        
        # Step 8: Auto-generate PracticalBatches (labs)
        labs_created = 0
        if request.labs_per_section > 0:
            for section in sections:
                for lab_no in range(1, request.labs_per_section + 1):
                    lab_code = f"P{lab_no}"
                    lab_name = f"Lab {lab_code}"
                    
                    practical_batch = PracticalBatch(
                        name=lab_name,
                        code=lab_code,
                        section_id=section.id,
                        max_strength=request.lab_capacity,
                        current_strength=0,
                        is_active=True
                    )
                    session.add(practical_batch)
                    labs_created += 1
        
        session.flush()  # Get practical_batch IDs
        
        # Audit log practical batch creation
        if request.labs_per_section > 0:
            for section in sections:
                labs = session.exec(
                    select(PracticalBatch).where(PracticalBatch.section_id == section.id)
                ).all()
                for lab in labs:
                    log_create(
                        session=session,
                        table_name="practical_batch",
                        record_id=lab.id,
                        new_values={
                            "name": lab.name,
                            "code": lab.code,
                            "section_id": lab.section_id,
                            "max_strength": lab.max_strength
                        },
                        user_id=user_id,
                        request=http_request
                    )
        
        # Commit all changes
        session.commit()
        session.refresh(batch)
        
        # Calculate statistics
        total_section_capacity = sections_created * request.section_capacity
        total_lab_capacity = labs_created * request.lab_capacity if labs_created > 0 else 0
        
        return BulkBatchSetupResponse(
            batch_id=batch.id,
            batch_code=batch.batch_code,
            batch_name=batch.batch_name,
            years_created=len(program_years),
            semesters_created=len(batch_semesters),
            sections_created=sections_created,
            labs_created=labs_created,
            total_section_capacity=total_section_capacity,
            total_lab_capacity=total_lab_capacity,
            message=f"Successfully created batch {batch.batch_code} with complete academic structure"
        )
    
    @staticmethod
    def _get_year_name(year_no: int) -> str:
        """Get year name (1st Year, 2nd Year, etc.)"""
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        suffix = suffixes.get(year_no, 'th')
        return f"{year_no}{suffix} Year"
