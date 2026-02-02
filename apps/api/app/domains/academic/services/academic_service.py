
from typing import Optional
from sqlmodel import Session, select
from fastapi import HTTPException
from app.domains.academic.models import AcademicBatch, ProgramYear, BatchSemester, Section, PracticalBatch

class AcademicValidationService:
    @staticmethod
    def validate_hierarchy(
        session: Session,
        batch_id: int,
        program_year_id: int,
        batch_semester_id: int,
        section_id: Optional[int] = None,
        practical_batch_id: Optional[int] = None
    ) -> None:
        """
        Strictly validates the academic hierarchy.
        Raises HTTPException if any rule is violated.
        
        Rules:
        1. Program Year must belong to Batch.
        2. Batch Semester must belong to Program Year (and thus Batch).
        3. Section must belong to Batch Semester.
        4. Practical Batch must belong to Section.
        """
        
        # 1. Validate Program Year -> Batch
        program_year = session.get(ProgramYear, program_year_id)
        if not program_year:
            raise HTTPException(status_code=400, detail=f"Program Year {program_year_id} not found")
            
        if program_year.batch_id != batch_id:
            raise HTTPException(
                status_code=400, 
                detail=f"Hierarchy Violation: Program Year {program_year.year_name} (ID: {program_year_id}) belongs to Batch {program_year.batch_id}, not {batch_id}"
            )

        # 2. Validate Semester -> Program Year
        batch_semester = session.get(BatchSemester, batch_semester_id)
        if not batch_semester:
            raise HTTPException(status_code=400, detail=f"Semester {batch_semester_id} not found")
        
        # Note: BatchSemester links to ProgramYear. 
        # Optionally checking batch_semester.batch_id == batch_id as well for redundancy
        if batch_semester.program_year_id != program_year_id:
             raise HTTPException(
                status_code=400, 
                detail=f"Hierarchy Violation: Semester {batch_semester.semester_name} (ID: {batch_semester_id}) belongs to Program Year {batch_semester.program_year_id}, not {program_year_id}"
            )
            
        # 3. Validate Section -> Semester (If assigned)
        if section_id:
            section = session.get(Section, section_id)
            if not section:
                 raise HTTPException(status_code=400, detail=f"Section {section_id} not found")
            
            if section.batch_semester_id != batch_semester_id:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Hierarchy Violation: Section {section.name} (ID: {section_id}) belongs to Semester {section.batch_semester_id}, not {batch_semester_id}"
                )
        
        # 4. Validate Practical Batch -> Section (If assigned)
        if practical_batch_id:
            if not section_id:
                raise HTTPException(status_code=400, detail="Cannot assign Practical Batch without a Section")
                
            pb = session.get(PracticalBatch, practical_batch_id)
            if not pb:
                 raise HTTPException(status_code=400, detail=f"Practical Batch {practical_batch_id} not found")
                 
            if pb.section_id != section_id:
                 raise HTTPException(
                    status_code=400, 
                    detail=f"Hierarchy Violation: Practical Batch {pb.batch_name} (ID: {practical_batch_id}) belongs to Section {pb.section_id}, not {section_id}"
                )

academic_validation_service = AcademicValidationService()
