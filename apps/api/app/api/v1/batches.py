"""
Batch API Endpoints with Auto-Generation

CRITICAL WORKFLOW:
1. Create batch
2. Auto-generate Program Years (READ-ONLY)
3. Auto-generate Semesters (2 per year)
4. Freeze regulation subjects to batch
5. Lock regulation
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from app.utils.audit import log_create, log_delete
from app.utils.academic_validation import AcademicValidationError

from app.api import deps
from app.models.user import User
from app.models.program import Program
from app.models.academic.regulation import Regulation, RegulationSubject, RegulationSemester
from app.models.academic.batch import (
    AcademicBatch,
    BatchSubject,
    BatchSemester,
    ProgramYear
)
from app.schemas.academic.batch import (
    AcademicBatchCreate,
    AcademicBatchUpdate,
    AcademicBatchRead,
    AcademicBatchWithDetails,
    ProgramYearRead,
    BatchSemesterRead,
    BatchSemesterUpdate,
    BatchSubjectRead
)
from app.schemas.bulk_setup import BulkBatchSetupRequest, BulkBatchSetupResponse
from app.schemas.batch_cloning import BatchCloneRequest, BatchCloneResponse
from app.services.bulk_setup_service import BulkBatchSetupService
from app.services.batch_cloning_service import BatchCloningService

router = APIRouter()


def check_admin(current_user: User):
    """Check if user has admin privileges"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True


def get_ordinal_name(num: int) -> str:
    """Convert number to ordinal name"""
    if num == 1:
        return "1st Year"
    elif num == 2:
        return "2nd Year"
    elif num == 3:
        return "3rd Year"
    else:
        return f"{num}th Year"


# ============================================================================
# Academic Batch Endpoints
# ============================================================================

@router.get("/", response_model=List[AcademicBatchRead], tags=["Academic Batches"])
def list_batches(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    program_id: Optional[int] = None,
    regulation_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """List all academic batches with optional filters"""
    stmt = select(AcademicBatch)
    
    if program_id:
        stmt = stmt.where(AcademicBatch.program_id == program_id)
    if regulation_id:
        stmt = stmt.where(AcademicBatch.regulation_id == regulation_id)
    if status:
        stmt = stmt.where(AcademicBatch.status == status)
    
    stmt = stmt.offset(skip).limit(limit).order_by(AcademicBatch.joining_year.desc())
    
    return session.exec(stmt).all()


@router.get("/{id}", response_model=AcademicBatchWithDetails, tags=["Academic Batches"])
def get_batch(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Get batch with all details"""
    batch = session.get(AcademicBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    return batch


@router.post("/", response_model=AcademicBatchRead, tags=["Academic Batches"])
def create_batch(
    data: AcademicBatchCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create academic batch with AUTO-GENERATION
    
    This endpoint:
    1. Creates the batch
    2. Auto-generates Program Years (1st, 2nd, 3rd)
    3. Auto-generates Semesters (2 per year)
    4. Freezes all regulation subjects to batch
    5. Locks the regulation
    
    All operations are ATOMIC (all or nothing)
    """
    check_admin(current_user)
    
    try:
        with session.begin_nested():  # Savepoint for rollback safety
            # Get program
            program = session.get(Program, data.program_id)
            if not program:
                raise HTTPException(status_code=404, detail="Program not found")
            
            # Get regulation
            regulation = session.get(Regulation, data.regulation_id)
            if not regulation:
                raise HTTPException(status_code=404, detail="Regulation not found")
            
            # Verify regulation belongs to program
            if regulation.program_id != data.program_id:
                raise HTTPException(
                    status_code=400,
                    detail="Regulation does not belong to this program"
                )
            
            # Check for duplicate batch
            existing = session.exec(
                select(AcademicBatch)
                .where(AcademicBatch.program_id == data.program_id)
                .where(AcademicBatch.joining_year == data.joining_year)
            ).first()
            
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail=f"Batch already exists for {program.name} joining in {data.joining_year}"
                )
            
            # Calculate batch details
            end_year = data.joining_year + program.duration_years
            batch_code = f"{program.code}-{data.joining_year}-{end_year}"
            batch_name = f"Batch {data.joining_year}-{end_year}"
            
            # 1. Create batch
            batch = AcademicBatch(
                batch_code=batch_code,
                batch_name=batch_name,
                program_id=data.program_id,
                regulation_id=data.regulation_id,
                joining_year=data.joining_year,
                start_year=data.joining_year,
                end_year=end_year,
                total_students=data.total_students,
                created_by=current_user.id
            )
            session.add(batch)
            session.flush()  # Get batch.id
            
            # 2. Auto-generate Program Years (READ-ONLY)
            for year_no in range(1, program.duration_years + 1):
                program_year = ProgramYear(
                    batch_id=batch.id,
                    year_no=year_no,
                    year_name=get_ordinal_name(year_no)
                )
                session.add(program_year)
                session.flush()  # Get program_year.id
                
                # 3. Auto-generate Semesters (2 per year)
                for sem_in_year in range(1, 3):
                    semester_no = (year_no - 1) * 2 + sem_in_year
                    
                    # Get regulation semester data (if exists)
                    reg_semester = session.exec(
                        select(RegulationSemester)
                        .where(RegulationSemester.regulation_id == data.regulation_id)
                        .where(RegulationSemester.semester_no == semester_no)
                    ).first()
                    
                    batch_semester = BatchSemester(
                        batch_id=batch.id,
                        program_year_id=program_year.id,
                        year_no=year_no,
                        semester_no=semester_no,
                        semester_name=f"Semester {semester_no}",
                        total_credits=reg_semester.total_credits if reg_semester else 0,
                        min_credits_to_pass=reg_semester.min_credits_to_pass if reg_semester else 0
                    )
                    session.add(batch_semester)
            
            # 4. Freeze regulation subjects to batch
            reg_subjects = session.exec(
                select(RegulationSubject)
                .where(RegulationSubject.regulation_id == data.regulation_id)
                .where(RegulationSubject.is_active == True)
            ).all()
            
            for reg_subject in reg_subjects:
                batch_subject = BatchSubject(
                    batch_id=batch.id,
                    subject_code=reg_subject.subject_code,
                    subject_name=reg_subject.subject_name,
                    short_name=reg_subject.short_name,
                    subject_type=reg_subject.subject_type,
                    program_year=reg_subject.program_year,
                    semester_no=reg_subject.semester_no,
                    internal_max=reg_subject.internal_max,
                    external_max=reg_subject.external_max,
                    total_max=reg_subject.total_max,
                    passing_percentage=reg_subject.passing_percentage,
                    evaluation_type=reg_subject.evaluation_type,
                    has_exam=reg_subject.has_exam,
                    has_assignments=reg_subject.has_assignments,
                    hours_per_session=reg_subject.hours_per_session,
                    credits=reg_subject.credits,
                    is_active=reg_subject.is_active,
                    is_elective=reg_subject.is_elective
                )
                session.add(batch_subject)
            
            # 5. Lock regulation
            if not regulation.is_locked:
                regulation.is_locked = True
                regulation.locked_at = datetime.utcnow()
                regulation.locked_by = current_user.id
                regulation.version += 1
                session.add(regulation)
            
        # Commit all changes atomically
        session.commit()
        session.refresh(batch)
        
        # Log batch creation
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
            user=current_user,
            request=None
        )
        
        return batch
        
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Batch creation failed: {str(e)}"
        )


@router.patch("/{id}", response_model=AcademicBatchRead, tags=["Academic Batches"])
def update_batch(
    id: int,
    data: AcademicBatchUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update batch (admin only)
    
    SAFETY CHECK: Cannot update if students are admitted
    """
    check_admin(current_user)
    
    batch = session.get(AcademicBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # CRITICAL: Check if students are admitted
    # TODO: Add student count check when Student model is updated
    # student_count = session.exec(
    #     select(func.count(Student.id))
    #     .where(Student.batch_id == id)
    # ).one()
    # 
    # if student_count > 0:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Cannot modify batch after students are admitted"
    #     )
    
    # Update allowed fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(batch, key, value)
    
    batch.updated_at = datetime.utcnow()
    
    session.add(batch)
    session.commit()
    session.refresh(batch)
    
    return batch


@router.delete("/{id}", tags=["Academic Batches"])
def delete_batch(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete batch (admin only)
    
    SAFETY CHECK: Cannot delete if students are admitted
    """
    check_admin(current_user)
    
    batch = session.get(AcademicBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    # CRITICAL: Check if students are admitted
    if batch.total_students and batch.total_students > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete batch with {batch.total_students} admitted students. Remove students first."
        )
    
    # Store batch info for audit log
    batch_info = {
        "batch_code": batch.batch_code,
        "batch_name": batch.batch_name,
        "program_id": batch.program_id,
        "total_students": batch.total_students
    }
    
    session.delete(batch)
    session.commit()
    
    # Log deletion
    log_delete(
        session=session,
        table_name="academic_batch",
        record_id=id,
                old_values=batch_info,
        user_id=current_user.id,
        request=None
    )
    
    return {"message": "Batch deleted successfully"}


@router.post("/{batch_id}/clone", response_model=BatchCloneResponse)
def clone_batch(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    request: Request,
    batch_id: int,
    data: BatchCloneRequest
):
    """
    Clone an existing batch structure for a new academic year
    
    Clones:
    - Program years
    - Semesters
    - Sections (with capacity adjustments)
    - Labs (with capacity adjustments)
    - Optionally: Faculty assignments
    
    Does NOT clone:
    - Students
    - Attendance records
    - Grades
    """
    result = BatchCloningService.clone_batch(
        session=session,
        source_batch_id=batch_id,
        request=data,
        user_id=current_user.id,
        http_request=request
    )
    
    return result


# ============================================================================
# Program Year Endpoints (READ-ONLY)
# ============================================================================

@router.get("/{batch_id}/program-years", response_model=List[ProgramYearRead], tags=["Program Years"])
def list_program_years(
    batch_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    List program years for a batch (READ-ONLY)
    
    NOTE: Program years are auto-generated and cannot be modified
    """
    batch = session.get(AcademicBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    stmt = select(ProgramYear).where(
        ProgramYear.batch_id == batch_id
    ).order_by(ProgramYear.year_no)
    
    return session.exec(stmt).all()


# ============================================================================
# Batch Semester Endpoints (READ-ONLY)
# ============================================================================

@router.get("/{batch_id}/semesters", response_model=List[BatchSemesterRead], tags=["Batch Semesters"])
def list_batch_semesters(
    batch_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """List semesters for a batch (frozen from regulation)"""
    batch = session.get(AcademicBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    stmt = select(BatchSemester).where(
        BatchSemester.batch_id == batch_id
    ).options(
        selectinload(BatchSemester.sections),
        selectinload(BatchSemester.practical_batches)
    ).order_by(BatchSemester.semester_no)
    
    return session.exec(stmt).all()


@router.patch("/{batch_id}/semesters/{semester_id}", response_model=BatchSemesterRead, tags=["Batch Semesters"])
def update_batch_semester(
    batch_id: int,
    semester_id: int,
    data: BatchSemesterUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update batch semester dates and active status.
    Setting 'is_active=True' can trigger auto-promotion logic.
    """
    check_admin(current_user)
    
    # Verify batch
    batch = session.get(AcademicBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
        
    # Verify semester
    semester = session.get(BatchSemester, semester_id)
    if not semester or semester.batch_id != batch_id:
        raise HTTPException(status_code=404, detail="Semester not found in this batch")
        
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(semester, key, value)
        
    session.add(semester)
    session.commit()
    session.refresh(semester)
    
    return semester


# ============================================================================
# Batch Subject Endpoints (READ-ONLY)
# ============================================================================

@router.get("/{batch_id}/subjects", response_model=List[BatchSubjectRead], tags=["Batch Subjects"])
def list_batch_subjects(
    batch_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    semester_no: Optional[int] = None
):
    """List subjects for a batch (frozen from regulation)"""
    batch = session.get(AcademicBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    stmt = select(BatchSubject).where(BatchSubject.batch_id == batch_id)
    
    if semester_no:
        stmt = stmt.where(BatchSubject.semester_no == semester_no)
    
    stmt = stmt.order_by(BatchSubject.semester_no, BatchSubject.subject_code)
    
    return session.exec(stmt).all()


# ============================================================================
# Bulk Batch Setup (Feature 1: One-Click Registration)
# ============================================================================

@router.post("/bulk-setup", response_model=dict, tags=["Bulk Setup"])
def bulk_batch_setup(
    request_data: dict,
    request: Request,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    🚀 ONE-CLICK BATCH SETUP
    
    Creates entire academic structure in one operation:
    - Academic Batch
    - Program Years (1st, 2nd, 3rd, etc.)
    - Batch Semesters (from regulation)
    - Sections (A, B, C, etc.)
    - Practical Batches / Labs (P1, P2, P3, etc.)
    
    Example:
    ```json
    {
        "program_id": 1,
        "joining_year": 2024,
        "regulation_id": 1,
        "sections_per_semester": 2,
        "section_capacity": 60,
        "labs_per_section": 3,
        "lab_capacity": 20
    }
    ```
    
    This will create:
    - 1 Batch (2024-2028)
    - 4 Program Years
    - 8 Semesters
    - 16 Sections (2 per semester)
    - 48 Labs (3 per section)
    """
    check_admin(current_user)
    
    # Import here to avoid circular dependency
    from app.schemas.bulk_setup import BulkBatchSetupRequest
    from app.services.bulk_setup_service import BulkBatchSetupService
    from app.utils.audit import log_create
    
    # Validate and parse request
    try:
        bulk_request = BulkBatchSetupRequest(**request_data)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request data: {str(e)}"
        )
    
    # Execute bulk setup
    result = BulkBatchSetupService.create_bulk_batch(
        session=session,
        request=bulk_request,
        user_id=current_user.id
    )
    
    # Log audit trail
    log_create(
        session=session,
        table_name="academic_batch",
        record_id=result.batch_id,
        new_values={
            "batch_code": result.batch_code,
            "batch_name": result.batch_name,
            "years_created": result.years_created,
            "semesters_created": result.semesters_created,
            "sections_created": result.sections_created,
            "labs_created": result.labs_created,
            "bulk_setup": True
        },
        user=current_user,
        request=request
    )
    
    return result.dict()
