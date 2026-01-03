"""
Master Data API Router - Settings Module
Comprehensive CRUD endpoints for all master data tables
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api import deps
from app.models.user import User
from app.models.master_data import (
    AcademicYear, AcademicBatch, Section, PracticalBatch, SubjectConfig,
    FeeHead, InstallmentPlan, ScholarshipSlab,
    Board, PreviousQualification, StudyGroup, ReservationCategory, LeadSource,
    Designation, MasterClassroom, PlacementCompany,
    EmailTemplate, SMSTemplate
)
from app.models.program import Program
from app.models.department import Department
from app.schemas.master_data import (
    AcademicYearCreate, AcademicYearUpdate, AcademicYearRead,
    AcademicBatchCreate, AcademicBatchUpdate, AcademicBatchRead,
    SectionCreate, SectionUpdate, SectionRead,
    PracticalBatchCreate, PracticalBatchUpdate, PracticalBatchRead,
    SubjectConfigCreate, SubjectConfigUpdate, SubjectConfigRead,
    FeeHeadCreate, FeeHeadUpdate, FeeHeadRead,
    InstallmentPlanCreate, InstallmentPlanUpdate, InstallmentPlanRead,
    ScholarshipSlabCreate, ScholarshipSlabUpdate, ScholarshipSlabRead,
    BoardCreate, BoardUpdate, BoardRead,
    PreviousQualificationCreate, PreviousQualificationUpdate, PreviousQualificationRead,
    StudyGroupCreate, StudyGroupUpdate, StudyGroupRead,
    ReservationCategoryCreate, ReservationCategoryUpdate, ReservationCategoryRead,
    LeadSourceCreate, LeadSourceUpdate, LeadSourceRead,
    DesignationCreate, DesignationUpdate, DesignationRead,
    ClassroomCreate, ClassroomUpdate, ClassroomRead,
    PlacementCompanyCreate, PlacementCompanyUpdate, PlacementCompanyRead,
    EmailTemplateCreate, EmailTemplateUpdate, EmailTemplateRead,
    SMSTemplateCreate, SMSTemplateUpdate, SMSTemplateRead,
)

router = APIRouter()

def check_admin(current_user: User):
    """Check if user has admin privileges"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True

# ============================================================================
# Academic Year Endpoints
# ============================================================================

@router.get("/academic-years", response_model=List[AcademicYearRead], tags=["Academic Setup"])
def list_academic_years(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_current: Optional[bool] = None
):
    """List all academic years"""
    stmt = select(AcademicYear)
    if is_current is not None:
        stmt = stmt.where(AcademicYear.is_current == is_current)
    return session.exec(stmt.order_by(AcademicYear.start_date.desc())).all()

@router.post("/academic-years", response_model=AcademicYearRead, tags=["Academic Setup"])
def create_academic_year(
    data: AcademicYearCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new academic year"""
    check_admin(current_user)
    
    # If this is set as current, unset others
    if data.is_current:
        existing = session.exec(select(AcademicYear).where(AcademicYear.is_current == True)).all()
        for ay in existing:
            ay.is_current = False
            session.add(ay)
    
    academic_year = AcademicYear(**data.model_dump())
    session.add(academic_year)
    session.commit()
    session.refresh(academic_year)
    return academic_year

@router.patch("/academic-years/{id}", response_model=AcademicYearRead, tags=["Academic Setup"])
def update_academic_year(
    id: int,
    data: AcademicYearUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an academic year"""
    check_admin(current_user)
    
    academic_year = session.get(AcademicYear, id)
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic year not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # If setting as current, unset others
    if update_data.get("is_current"):
        existing = session.exec(select(AcademicYear).where(AcademicYear.is_current == True, AcademicYear.id != id)).all()
        for ay in existing:
            ay.is_current = False
            session.add(ay)
    
    for key, value in update_data.items():
        setattr(academic_year, key, value)
    
    session.add(academic_year)
    session.commit()
    session.refresh(academic_year)
    return academic_year

@router.delete("/academic-years/{id}", tags=["Academic Setup"])
def delete_academic_year(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete an academic year"""
    check_admin(current_user)
    
    academic_year = session.get(AcademicYear, id)
    if not academic_year:
        raise HTTPException(status_code=404, detail="Academic year not found")
    
    session.delete(academic_year)
    session.commit()
    return {"status": "success", "message": "Academic year deleted"}

# ============================================================================
# Programs Endpoint (for dropdown selection)
# ============================================================================

@router.get("/programs-list", tags=["Academic Setup"])
def list_programs_for_selection(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """List all programs for dropdown selection"""
    programs = session.exec(select(Program).where(Program.is_active == True).order_by(Program.name)).all()
    return [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "duration_years": p.duration_years,
            "program_type": p.program_type
        }
        for p in programs
    ]

# ============================================================================
# Academic Batch Endpoints
# ============================================================================

@router.get("/academic-batches", tags=["Academic Setup"])
def list_academic_batches(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    program_id: Optional[int] = None,
    is_active: Optional[bool] = None
):
    """List all academic batches with program details"""
    stmt = select(AcademicBatch)
    if program_id:
        stmt = stmt.where(AcademicBatch.program_id == program_id)
    if is_active is not None:
        stmt = stmt.where(AcademicBatch.is_active == is_active)
    
    batches = session.exec(stmt.order_by(AcademicBatch.admission_year.desc())).all()
    
    # Enrich with program details
    result = []
    for batch in batches:
        program = session.get(Program, batch.program_id)
        batch_dict = {
            "id": batch.id,
            "name": batch.name,
            "code": batch.code,
            "program_id": batch.program_id,
            "program_name": program.name if program else "Unknown",
            "program_code": program.code if program else "Unknown",
            "academic_year_id": batch.academic_year_id,
            "admission_year": batch.admission_year,
            "graduation_year": batch.graduation_year,
            "max_strength": batch.max_strength,
            "current_strength": batch.current_strength,
            "is_active": batch.is_active,
            "created_at": batch.created_at,
            "updated_at": batch.updated_at
        }
        result.append(batch_dict)
    
    return result

@router.post("/academic-batches", response_model=AcademicBatchRead, tags=["Academic Setup"])
def create_academic_batch(
    data: AcademicBatchCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new academic batch"""
    check_admin(current_user)
    
    batch = AcademicBatch(**data.model_dump())
    session.add(batch)
    session.commit()
    session.refresh(batch)
    return batch

@router.patch("/academic-batches/{id}", response_model=AcademicBatchRead, tags=["Academic Setup"])
def update_academic_batch(
    id: int,
    data: AcademicBatchUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an academic batch"""
    check_admin(current_user)
    
    batch = session.get(AcademicBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Academic batch not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(batch, key, value)
    
    session.add(batch)
    session.commit()
    session.refresh(batch)
    return batch

@router.delete("/academic-batches/{id}", tags=["Academic Setup"])
def delete_academic_batch(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete an academic batch"""
    check_admin(current_user)
    
    batch = session.get(AcademicBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Academic batch not found")
    
    session.delete(batch)
    session.commit()
    return {"status": "success", "message": "Academic batch deleted"}

# ============================================================================
# Fee Head Endpoints
# ============================================================================

@router.get("/fee-heads", response_model=List[FeeHeadRead], tags=["Fee Configuration"])
def list_fee_heads(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all fee heads"""
    stmt = select(FeeHead)
    if is_active is not None:
        stmt = stmt.where(FeeHead.is_active == is_active)
    return session.exec(stmt.order_by(FeeHead.display_order)).all()

@router.post("/fee-heads", response_model=FeeHeadRead, tags=["Fee Configuration"])
def create_fee_head(
    data: FeeHeadCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new fee head"""
    check_admin(current_user)
    
    fee_head = FeeHead(**data.model_dump())
    session.add(fee_head)
    session.commit()
    session.refresh(fee_head)
    return fee_head

@router.patch("/fee-heads/{id}", response_model=FeeHeadRead, tags=["Fee Configuration"])
def update_fee_head(
    id: int,
    data: FeeHeadUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a fee head"""
    check_admin(current_user)
    
    fee_head = session.get(FeeHead, id)
    if not fee_head:
        raise HTTPException(status_code=404, detail="Fee head not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(fee_head, key, value)
    
    session.add(fee_head)
    session.commit()
    session.refresh(fee_head)
    return fee_head

@router.delete("/fee-heads/{id}", tags=["Fee Configuration"])
def delete_fee_head(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a fee head"""
    check_admin(current_user)
    
    fee_head = session.get(FeeHead, id)
    if not fee_head:
        raise HTTPException(status_code=404, detail="Fee head not found")
    
    session.delete(fee_head)
    session.commit()
    return {"status": "success", "message": "Fee head deleted"}

# ============================================================================
# Installment Plan Endpoints
# ============================================================================

@router.get("/installment-plans", response_model=List[InstallmentPlanRead], tags=["Fee Configuration"])
def list_installment_plans(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all installment plans"""
    stmt = select(InstallmentPlan)
    if is_active is not None:
        stmt = stmt.where(InstallmentPlan.is_active == is_active)
    return session.exec(stmt).all()

@router.post("/installment-plans", response_model=InstallmentPlanRead, tags=["Fee Configuration"])
def create_installment_plan(
    data: InstallmentPlanCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new installment plan"""
    check_admin(current_user)
    
    plan = InstallmentPlan(**data.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.patch("/installment-plans/{id}", response_model=InstallmentPlanRead, tags=["Fee Configuration"])
def update_installment_plan(
    id: int,
    data: InstallmentPlanUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an installment plan"""
    check_admin(current_user)
    
    plan = session.get(InstallmentPlan, id)
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(plan, key, value)
    
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan

@router.delete("/installment-plans/{id}", tags=["Fee Configuration"])
def delete_installment_plan(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete an installment plan"""
    check_admin(current_user)
    
    plan = session.get(InstallmentPlan, id)
    if not plan:
        raise HTTPException(status_code=404, detail="Installment plan not found")
    
    session.delete(plan)
    session.commit()
    return {"status": "success", "message": "Installment plan deleted"}

# ============================================================================
# Scholarship Slab Endpoints
# ============================================================================

@router.get("/scholarship-slabs", response_model=List[ScholarshipSlabRead], tags=["Fee Configuration"])
def list_scholarship_slabs(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all scholarship slabs"""
    stmt = select(ScholarshipSlab)
    if is_active is not None:
        stmt = stmt.where(ScholarshipSlab.is_active == is_active)
    return session.exec(stmt).all()

@router.post("/scholarship-slabs", response_model=ScholarshipSlabRead, tags=["Fee Configuration"])
def create_scholarship_slab(
    data: ScholarshipSlabCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new scholarship slab"""
    check_admin(current_user)
    
    slab = ScholarshipSlab(**data.model_dump())
    session.add(slab)
    session.commit()
    session.refresh(slab)
    return slab

@router.patch("/scholarship-slabs/{id}", response_model=ScholarshipSlabRead, tags=["Fee Configuration"])
def update_scholarship_slab(
    id: int,
    data: ScholarshipSlabUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a scholarship slab"""
    check_admin(current_user)
    
    slab = session.get(ScholarshipSlab, id)
    if not slab:
        raise HTTPException(status_code=404, detail="Scholarship slab not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(slab, key, value)
    
    session.add(slab)
    session.commit()
    session.refresh(slab)
    return slab

@router.delete("/scholarship-slabs/{id}", tags=["Fee Configuration"])
def delete_scholarship_slab(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a scholarship slab"""
    check_admin(current_user)
    
    slab = session.get(ScholarshipSlab, id)
    if not slab:
        raise HTTPException(status_code=404, detail="Scholarship slab not found")
    
    session.delete(slab)
    session.commit()
    return {"status": "success", "message": "Scholarship slab deleted"}

# ============================================================================
# Board Endpoints
# ============================================================================

@router.get("/boards", response_model=List[BoardRead], tags=["Admission Setup"])
def list_boards(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all boards/universities"""
    stmt = select(Board)
    if is_active is not None:
        stmt = stmt.where(Board.is_active == is_active)
    return session.exec(stmt.order_by(Board.display_order)).all()

@router.post("/boards", response_model=BoardRead, tags=["Admission Setup"])
def create_board(
    data: BoardCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new board"""
    check_admin(current_user)
    
    board = Board(**data.model_dump())
    session.add(board)
    session.commit()
    session.refresh(board)
    return board

@router.patch("/boards/{id}", response_model=BoardRead, tags=["Admission Setup"])
def update_board(
    id: int,
    data: BoardUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a board"""
    check_admin(current_user)
    
    board = session.get(Board, id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(board, key, value)
    
    session.add(board)
    session.commit()
    session.refresh(board)
    return board

@router.delete("/boards/{id}", tags=["Admission Setup"])
def delete_board(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a board"""
    check_admin(current_user)
    
    board = session.get(Board, id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    
    session.delete(board)
    session.commit()
    return {"status": "success", "message": "Board deleted"}

# ============================================================================
# Previous Qualification Endpoints
# ============================================================================

@router.get("/qualifications", response_model=List[PreviousQualificationRead], tags=["Admission Setup"])
def list_qualifications(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all previous qualifications"""
    stmt = select(PreviousQualification)
    if is_active is not None:
        stmt = stmt.where(PreviousQualification.is_active == is_active)
    return session.exec(stmt.order_by(PreviousQualification.level, PreviousQualification.display_order)).all()

@router.post("/qualifications", response_model=PreviousQualificationRead, tags=["Admission Setup"])
def create_qualification(
    data: PreviousQualificationCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new qualification"""
    check_admin(current_user)
    
    qual = PreviousQualification(**data.model_dump())
    session.add(qual)
    session.commit()
    session.refresh(qual)
    return qual

@router.patch("/qualifications/{id}", response_model=PreviousQualificationRead, tags=["Admission Setup"])
def update_qualification(
    id: int,
    data: PreviousQualificationUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a qualification"""
    check_admin(current_user)
    
    qual = session.get(PreviousQualification, id)
    if not qual:
        raise HTTPException(status_code=404, detail="Qualification not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(qual, key, value)
    
    session.add(qual)
    session.commit()
    session.refresh(qual)
    return qual

@router.delete("/qualifications/{id}", tags=["Admission Setup"])
def delete_qualification(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a qualification"""
    check_admin(current_user)
    
    qual = session.get(PreviousQualification, id)
    if not qual:
        raise HTTPException(status_code=404, detail="Qualification not found")
    
    session.delete(qual)
    session.commit()
    return {"status": "success", "message": "Qualification deleted"}

# ============================================================================
# Study Group Endpoints
# ============================================================================

@router.get("/study-groups", response_model=List[StudyGroupRead], tags=["Admission Setup"])
def list_study_groups(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all study groups"""
    stmt = select(StudyGroup)
    if is_active is not None:
        stmt = stmt.where(StudyGroup.is_active == is_active)
    return session.exec(stmt.order_by(StudyGroup.display_order)).all()

@router.post("/study-groups", response_model=StudyGroupRead, tags=["Admission Setup"])
def create_study_group(
    data: StudyGroupCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new study group"""
    check_admin(current_user)
    
    group = StudyGroup(**data.model_dump())
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

@router.patch("/study-groups/{id}", response_model=StudyGroupRead, tags=["Admission Setup"])
def update_study_group(
    id: int,
    data: StudyGroupUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a study group"""
    check_admin(current_user)
    
    group = session.get(StudyGroup, id)
    if not group:
        raise HTTPException(status_code=404, detail="Study group not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(group, key, value)
    
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

@router.delete("/study-groups/{id}", tags=["Admission Setup"])
def delete_study_group(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a study group"""
    check_admin(current_user)
    
    group = session.get(StudyGroup, id)
    if not group:
        raise HTTPException(status_code=404, detail="Study group not found")
    
    session.delete(group)
    session.commit()
    return {"status": "success", "message": "Study group deleted"}

# ============================================================================
# Reservation Category Endpoints
# ============================================================================

@router.get("/reservation-categories", response_model=List[ReservationCategoryRead], tags=["Admission Setup"])
def list_reservation_categories(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all reservation categories"""
    stmt = select(ReservationCategory)
    if is_active is not None:
        stmt = stmt.where(ReservationCategory.is_active == is_active)
    return session.exec(stmt.order_by(ReservationCategory.display_order)).all()

@router.post("/reservation-categories", response_model=ReservationCategoryRead, tags=["Admission Setup"])
def create_reservation_category(
    data: ReservationCategoryCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new reservation category"""
    check_admin(current_user)
    
    category = ReservationCategory(**data.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.patch("/reservation-categories/{id}", response_model=ReservationCategoryRead, tags=["Admission Setup"])
def update_reservation_category(
    id: int,
    data: ReservationCategoryUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a reservation category"""
    check_admin(current_user)
    
    category = session.get(ReservationCategory, id)
    if not category:
        raise HTTPException(status_code=404, detail="Reservation category not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)
    
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

@router.delete("/reservation-categories/{id}", tags=["Admission Setup"])
def delete_reservation_category(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a reservation category"""
    check_admin(current_user)
    
    category = session.get(ReservationCategory, id)
    if not category:
        raise HTTPException(status_code=404, detail="Reservation category not found")
    
    session.delete(category)
    session.commit()
    return {"status": "success", "message": "Reservation category deleted"}

# ============================================================================
# Lead Source Endpoints
# ============================================================================

@router.get("/lead-sources", response_model=List[LeadSourceRead], tags=["Admission Setup"])
def list_lead_sources(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all lead sources"""
    stmt = select(LeadSource)
    if is_active is not None:
        stmt = stmt.where(LeadSource.is_active == is_active)
    return session.exec(stmt.order_by(LeadSource.display_order)).all()

@router.post("/lead-sources", response_model=LeadSourceRead, tags=["Admission Setup"])
def create_lead_source(
    data: LeadSourceCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new lead source"""
    check_admin(current_user)
    
    source = LeadSource(**data.model_dump())
    session.add(source)
    session.commit()
    session.refresh(source)
    return source

@router.patch("/lead-sources/{id}", response_model=LeadSourceRead, tags=["Admission Setup"])
def update_lead_source(
    id: int,
    data: LeadSourceUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a lead source"""
    check_admin(current_user)
    
    source = session.get(LeadSource, id)
    if not source:
        raise HTTPException(status_code=404, detail="Lead source not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(source, key, value)
    
    session.add(source)
    session.commit()
    session.refresh(source)
    return source

@router.delete("/lead-sources/{id}", tags=["Admission Setup"])
def delete_lead_source(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a lead source"""
    check_admin(current_user)
    
    source = session.get(LeadSource, id)
    if not source:
        raise HTTPException(status_code=404, detail="Lead source not found")
    
    session.delete(source)
    session.commit()
    return {"status": "success", "message": "Lead source deleted"}

# ============================================================================
# Designation Endpoints
# ============================================================================

@router.get("/designations", response_model=List[DesignationRead], tags=["Infrastructure"])
def list_designations(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all designations"""
    stmt = select(Designation)
    if is_active is not None:
        stmt = stmt.where(Designation.is_active == is_active)
    return session.exec(stmt.order_by(Designation.level, Designation.display_order)).all()

@router.post("/designations", response_model=DesignationRead, tags=["Infrastructure"])
def create_designation(
    data: DesignationCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new designation"""
    check_admin(current_user)
    
    designation = Designation(**data.model_dump())
    session.add(designation)
    session.commit()
    session.refresh(designation)
    return designation

@router.patch("/designations/{id}", response_model=DesignationRead, tags=["Infrastructure"])
def update_designation(
    id: int,
    data: DesignationUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a designation"""
    check_admin(current_user)
    
    designation = session.get(Designation, id)
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(designation, key, value)
    
    session.add(designation)
    session.commit()
    session.refresh(designation)
    return designation

@router.delete("/designations/{id}", tags=["Infrastructure"])
def delete_designation(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a designation"""
    check_admin(current_user)
    
    designation = session.get(Designation, id)
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    
    session.delete(designation)
    session.commit()
    return {"status": "success", "message": "Designation deleted"}

# ============================================================================
# Classroom Endpoints
# ============================================================================

@router.get("/classrooms", response_model=List[ClassroomRead], tags=["Infrastructure"])
def list_classrooms(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None,
    room_type: Optional[str] = None
):
    """List all classrooms"""
    stmt = select(MasterClassroom)
    if is_active is not None:
        stmt = stmt.where(MasterClassroom.is_active == is_active)
    if room_type:
        stmt = stmt.where(MasterClassroom.room_type == room_type)
    return session.exec(stmt.order_by(MasterClassroom.building, MasterClassroom.floor, MasterClassroom.name)).all()

@router.post("/classrooms", response_model=ClassroomRead, tags=["Infrastructure"])
def create_classroom(
    data: ClassroomCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new classroom"""
    check_admin(current_user)
    
    classroom = MasterClassroom(**data.model_dump())
    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return classroom

@router.patch("/classrooms/{id}", response_model=ClassroomRead, tags=["Infrastructure"])
def update_classroom(
    id: int,
    data: ClassroomUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a classroom"""
    check_admin(current_user)
    
    classroom = session.get(MasterClassroom, id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(classroom, key, value)
    
    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return classroom

@router.delete("/classrooms/{id}", tags=["Infrastructure"])
def delete_classroom(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a classroom"""
    check_admin(current_user)
    
    classroom = session.get(MasterClassroom, id)
    if not classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    
    session.delete(classroom)
    session.commit()
    return {"status": "success", "message": "Classroom deleted"}

# ============================================================================
# Placement Company Endpoints
# ============================================================================

@router.get("/placement-companies", response_model=List[PlacementCompanyRead], tags=["Infrastructure"])
def list_placement_companies(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None,
    is_partner: Optional[bool] = None
):
    """List all placement companies"""
    stmt = select(PlacementCompany)
    if is_active is not None:
        stmt = stmt.where(PlacementCompany.is_active == is_active)
    if is_partner is not None:
        stmt = stmt.where(PlacementCompany.is_partner == is_partner)
    return session.exec(stmt.order_by(PlacementCompany.name)).all()

@router.post("/placement-companies", response_model=PlacementCompanyRead, tags=["Infrastructure"])
def create_placement_company(
    data: PlacementCompanyCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new placement company"""
    check_admin(current_user)
    
    company = PlacementCompany(**data.model_dump())
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@router.patch("/placement-companies/{id}", response_model=PlacementCompanyRead, tags=["Infrastructure"])
def update_placement_company(
    id: int,
    data: PlacementCompanyUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a placement company"""
    check_admin(current_user)
    
    company = session.get(PlacementCompany, id)
    if not company:
        raise HTTPException(status_code=404, detail="Placement company not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(company, key, value)
    
    session.add(company)
    session.commit()
    session.refresh(company)
    return company

@router.delete("/placement-companies/{id}", tags=["Infrastructure"])
def delete_placement_company(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a placement company"""
    check_admin(current_user)
    
    company = session.get(PlacementCompany, id)
    if not company:
        raise HTTPException(status_code=404, detail="Placement company not found")
    
    session.delete(company)
    session.commit()
    return {"status": "success", "message": "Placement company deleted"}

# ============================================================================
# Email Template Endpoints
# ============================================================================

@router.get("/email-templates", response_model=List[EmailTemplateRead], tags=["Communication"])
def list_email_templates(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all email templates"""
    stmt = select(EmailTemplate)
    if is_active is not None:
        stmt = stmt.where(EmailTemplate.is_active == is_active)
    return session.exec(stmt).all()

@router.post("/email-templates", response_model=EmailTemplateRead, tags=["Communication"])
def create_email_template(
    data: EmailTemplateCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new email template"""
    check_admin(current_user)
    
    template = EmailTemplate(**data.model_dump())
    session.add(template)
    session.commit()
    session.refresh(template)
    return template

@router.patch("/email-templates/{id}", response_model=EmailTemplateRead, tags=["Communication"])
def update_email_template(
    id: int,
    data: EmailTemplateUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an email template"""
    check_admin(current_user)
    
    template = session.get(EmailTemplate, id)
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(template, key, value)
    
    session.add(template)
    session.commit()
    session.refresh(template)
    return template

@router.delete("/email-templates/{id}", tags=["Communication"])
def delete_email_template(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete an email template"""
    check_admin(current_user)
    
    template = session.get(EmailTemplate, id)
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    
    session.delete(template)
    session.commit()
    return {"status": "success", "message": "Email template deleted"}

# ============================================================================
# SMS Template Endpoints
# ============================================================================

@router.get("/sms-templates", response_model=List[SMSTemplateRead], tags=["Communication"])
def list_sms_templates(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all SMS templates"""
    stmt = select(SMSTemplate)
    if is_active is not None:
        stmt = stmt.where(SMSTemplate.is_active == is_active)
    return session.exec(stmt).all()

@router.post("/sms-templates", response_model=SMSTemplateRead, tags=["Communication"])
def create_sms_template(
    data: SMSTemplateCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new SMS template"""
    check_admin(current_user)
    
    template = SMSTemplate(**data.model_dump())
    session.add(template)
    session.commit()
    session.refresh(template)
    return template

@router.patch("/sms-templates/{id}", response_model=SMSTemplateRead, tags=["Communication"])
def update_sms_template(
    id: int,
    data: SMSTemplateUpdate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update an SMS template"""
    check_admin(current_user)
    
    template = session.get(SMSTemplate, id)
    if not template:
        raise HTTPException(status_code=404, detail="SMS template not found")
    
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(template, key, value)
    
    session.add(template)
    session.commit()
    session.refresh(template)
    return template

@router.delete("/sms-templates/{id}", tags=["Communication"])
def delete_sms_template(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete an SMS template"""
    check_admin(current_user)
    
    template = session.get(SMSTemplate, id)
    if not template:
        raise HTTPException(status_code=404, detail="SMS template not found")
    
    session.delete(template)
    session.commit()
    return {"status": "success", "message": "SMS template deleted"}

# ============================================================================
# Programs/Courses Management
# ============================================================================

@router.get("/programs", tags=["Programs"])
def list_programs(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    is_active: Optional[bool] = None
):
    """List all programs/courses with department details"""
    stmt = select(Program)
    if is_active is not None:
        stmt = stmt.where(Program.is_active == is_active)
    
    programs = session.exec(stmt.order_by(Program.name)).all()
    
    result = []
    for p in programs:
        dept = session.get(Department, p.department_id)
        result.append({
            "id": p.id,
            "code": p.code,
            "short_name": p.short_name or p.code,
            "name": p.name,
            "program_type": p.program_type,
            "status": p.status,
            "duration_years": p.duration_years,
            "description": p.description,
            "semester_system": getattr(p, 'semester_system', True),
            "rnet_required": getattr(p, 'rnet_required', True),
            "allow_installments": getattr(p, 'allow_installments', True),
            "department_id": p.department_id,
            "department_name": dept.name if dept else "Unknown",
            "is_active": p.is_active,
            "created_at": p.created_at,
            "updated_at": p.updated_at
        })
    
    return result

@router.get("/departments-list", tags=["Programs"])
def list_departments_for_selection(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """List all departments for dropdown selection"""
    departments = session.exec(select(Department).order_by(Department.name)).all()
    return [{"id": d.id, "name": d.name, "code": d.code} for d in departments]

@router.post("/programs", tags=["Programs"])
def create_program(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new program/course"""
    check_admin(current_user)
    
    # Check if code already exists
    existing = session.exec(select(Program).where(Program.code == data.get('code'))).first()
    if existing:
        raise HTTPException(status_code=400, detail="Program code already exists")
    
    program = Program(
        code=data.get('code'),
        short_name=data.get('short_name', data.get('code')),
        name=data.get('name'),
        program_type=data.get('program_type', 'UG'),
        duration_years=data.get('duration_years', 4),
        description=data.get('description'),
        semester_system=data.get('semester_system', True),
        rnet_required=data.get('rnet_required', True),
        allow_installments=data.get('allow_installments', True),
        department_id=data.get('department_id'),
        is_active=data.get('is_active', True),
        status=data.get('status', 'ACTIVE')
    )
    
    session.add(program)
    session.commit()
    session.refresh(program)
    
    return {
        "id": program.id,
        "code": program.code,
        "short_name": program.short_name,
        "name": program.name,
        "duration_years": program.duration_years,
        "message": "Program created successfully"
    }

@router.patch("/programs/{id}", tags=["Programs"])
def update_program(
    id: int,
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a program/course"""
    check_admin(current_user)
    
    program = session.get(Program, id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Update fields
    for key in ['code', 'short_name', 'name', 'program_type', 'duration_years', 
                'description', 'semester_system', 'rnet_required', 'allow_installments',
                'department_id', 'is_active', 'status']:
        if key in data:
            setattr(program, key, data[key])
    
    session.add(program)
    session.commit()
    session.refresh(program)
    
    return {"message": "Program updated successfully", "id": program.id}

@router.delete("/programs/{id}", tags=["Programs"])
def delete_program(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a program/course"""
    check_admin(current_user)
    
    program = session.get(Program, id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    # Check if there are students in this program
    from app.models.student import Student
    students_count = session.exec(
        select(Student).where(Student.program_id == id)
    ).first()
    
    if students_count:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete program with enrolled students. Deactivate instead."
        )
    
    session.delete(program)
    session.commit()
    return {"status": "success", "message": "Program deleted"}

# ============================================================================
# Academic Structure Management
# Course → Year → Semester → Section → Batch
# ============================================================================

from app.models.program_year import ProgramYear
from app.models.semester import Semester
from app.models.master_data import Section, PracticalBatch

@router.get("/academic-structure", tags=["Academic Structure"])
def get_academic_structure(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    program_id: Optional[int] = None
):
    """Get complete academic structure: Program → Year → Semester → Section → Batch"""
    
    # Get programs
    stmt = select(Program).where(Program.is_active == True)
    if program_id:
        stmt = stmt.where(Program.id == program_id)
    programs = session.exec(stmt.order_by(Program.name)).all()
    
    result = []
    for program in programs:
        program_data = {
            "id": program.id,
            "code": program.code,
            "name": program.name,
            "short_name": getattr(program, 'short_name', program.code),
            "duration_years": program.duration_years,
            "semester_system": getattr(program, 'semester_system', True),
            "years": []
        }
        
        # Get program years
        years = session.exec(
            select(ProgramYear)
            .where(ProgramYear.program_id == program.id)
            .order_by(ProgramYear.year_number)
        ).all()
        
        for year in years:
            year_data = {
                "id": year.id,
                "year_number": year.year_number,
                "name": year.name,
                "is_active": year.is_active,
                "semesters": []
            }
            
            # Get semesters
            semesters = session.exec(
                select(Semester)
                .where(Semester.program_year_id == year.id)
                .order_by(Semester.semester_number)
            ).all()
            
            for sem in semesters:
                sem_data = {
                    "id": sem.id,
                    "semester_number": sem.semester_number,
                    "name": sem.name,
                    "is_internship": sem.is_internship,
                    "is_project_semester": sem.is_project_semester,
                    "sections": []
                }
                
                # Get sections
                sections = session.exec(
                    select(Section)
                    .where(Section.semester_id == sem.id)
                    .order_by(Section.code)
                ).all()
                
                for section in sections:
                    section_data = {
                        "id": section.id,
                        "name": section.name,
                        "code": section.code,
                        "max_strength": section.max_strength,
                        "current_strength": section.current_strength,
                        "is_active": section.is_active,
                        "batches": []
                    }
                    
                    # Get practical batches
                    batches = session.exec(
                        select(PracticalBatch)
                        .where(PracticalBatch.section_id == section.id)
                        .order_by(PracticalBatch.code)
                    ).all()
                    
                    for batch in batches:
                        section_data["batches"].append({
                            "id": batch.id,
                            "name": batch.name,
                            "code": batch.code,
                            "max_strength": batch.max_strength,
                            "current_strength": batch.current_strength,
                            "is_active": batch.is_active
                        })
                    
                    sem_data["sections"].append(section_data)
                
                year_data["semesters"].append(sem_data)
            
            program_data["years"].append(year_data)
        
        result.append(program_data)
    
    return result

@router.post("/academic-structure/generate", tags=["Academic Structure"])
def generate_academic_structure(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Auto-generate academic structure for a program"""
    check_admin(current_user)
    
    program_id = data.get('program_id')
    sections_per_semester = data.get('sections_per_semester', 2)
    students_per_section = data.get('students_per_section', 60)
    batches_per_section = data.get('batches_per_section', 2)
    students_per_batch = data.get('students_per_batch', 30)
    
    program = session.get(Program, program_id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    created = {"years": 0, "semesters": 0, "sections": 0, "batches": 0}
    
    # Create years
    for year_num in range(1, program.duration_years + 1):
        year_names = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]
        year_name = f"{year_names[year_num-1]} Year" if year_num <= 6 else f"Year {year_num}"
        
        # Check if year exists
        existing_year = session.exec(
            select(ProgramYear)
            .where(ProgramYear.program_id == program_id)
            .where(ProgramYear.year_number == year_num)
        ).first()
        
        if not existing_year:
            year = ProgramYear(
                program_id=program_id,
                year_number=year_num,
                name=year_name,
                is_active=True
            )
            session.add(year)
            session.flush()
            created["years"] += 1
        else:
            year = existing_year
        
        # Create semesters (2 per year if semester system)
        semesters_count = 2 if getattr(program, 'semester_system', True) else 1
        for sem_num in range(1, semesters_count + 1):
            global_sem_num = (year_num - 1) * semesters_count + sem_num
            sem_name = f"Semester {global_sem_num}" if semesters_count == 2 else f"Year {year_num}"
            
            existing_sem = session.exec(
                select(Semester)
                .where(Semester.program_year_id == year.id)
                .where(Semester.semester_number == sem_num)
            ).first()
            
            if not existing_sem:
                sem = Semester(
                    program_year_id=year.id,
                    semester_number=sem_num,
                    name=sem_name,
                    is_internship=False,
                    is_project_semester=False
                )
                session.add(sem)
                session.flush()
                created["semesters"] += 1
            else:
                sem = existing_sem
            
            # Create sections
            section_codes = ["A", "B", "C", "D", "E", "F", "G", "H"]
            for sec_idx in range(sections_per_semester):
                sec_code = section_codes[sec_idx] if sec_idx < len(section_codes) else str(sec_idx + 1)
                sec_name = f"Section {sec_code}"
                
                existing_section = session.exec(
                    select(Section)
                    .where(Section.semester_id == sem.id)
                    .where(Section.code == sec_code)
                ).first()
                
                if not existing_section:
                    section = Section(
                        name=sec_name,
                        code=sec_code,
                        semester_id=sem.id,
                        max_strength=students_per_section,
                        current_strength=0,
                        is_active=True
                    )
                    session.add(section)
                    session.flush()
                    created["sections"] += 1
                else:
                    section = existing_section
                
                # Create practical batches
                batch_codes = ["A", "B", "C", "D"]
                for batch_idx in range(batches_per_section):
                    batch_code = batch_codes[batch_idx] if batch_idx < len(batch_codes) else str(batch_idx + 1)
                    batch_name = f"Batch {batch_code}"
                    
                    existing_batch = session.exec(
                        select(PracticalBatch)
                        .where(PracticalBatch.section_id == section.id)
                        .where(PracticalBatch.code == batch_code)
                    ).first()
                    
                    if not existing_batch:
                        batch = PracticalBatch(
                            name=batch_name,
                            code=batch_code,
                            section_id=section.id,
                            max_strength=students_per_batch,
                            current_strength=0,
                            is_active=True
                        )
                        session.add(batch)
                        created["batches"] += 1
    
    session.commit()
    
    return {
        "message": f"Structure generated for {program.code}",
        "created": created
    }

# Program Year CRUD
@router.post("/program-years", tags=["Academic Structure"])
def create_program_year(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a program year"""
    check_admin(current_user)
    
    year = ProgramYear(
        program_id=data.get('program_id'),
        year_number=data.get('year_number'),
        name=data.get('name'),
        is_active=data.get('is_active', True)
    )
    session.add(year)
    session.commit()
    session.refresh(year)
    return {"id": year.id, "message": "Program year created"}

@router.patch("/program-years/{id}", tags=["Academic Structure"])
def update_program_year(
    id: int,
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a program year"""
    check_admin(current_user)
    
    year = session.get(ProgramYear, id)
    if not year:
        raise HTTPException(status_code=404, detail="Program year not found")
    
    for key in ['name', 'is_active']:
        if key in data:
            setattr(year, key, data[key])
    
    session.add(year)
    session.commit()
    return {"message": "Program year updated"}

@router.delete("/program-years/{id}", tags=["Academic Structure"])
def delete_program_year(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a program year and all child elements"""
    check_admin(current_user)
    
    year = session.get(ProgramYear, id)
    if not year:
        raise HTTPException(status_code=404, detail="Program year not found")
    
    session.delete(year)
    session.commit()
    return {"message": "Program year deleted"}

# Semester CRUD
@router.post("/semesters", tags=["Academic Structure"])
def create_semester(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a semester"""
    check_admin(current_user)
    
    sem = Semester(
        program_year_id=data.get('program_year_id'),
        semester_number=data.get('semester_number'),
        name=data.get('name'),
        is_internship=data.get('is_internship', False),
        is_project_semester=data.get('is_project_semester', False)
    )
    session.add(sem)
    session.commit()
    session.refresh(sem)
    return {"id": sem.id, "message": "Semester created"}

@router.patch("/semesters/{id}", tags=["Academic Structure"])
def update_semester(
    id: int,
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a semester"""
    check_admin(current_user)
    
    sem = session.get(Semester, id)
    if not sem:
        raise HTTPException(status_code=404, detail="Semester not found")
    
    for key in ['name', 'is_internship', 'is_project_semester']:
        if key in data:
            setattr(sem, key, data[key])
    
    session.add(sem)
    session.commit()
    return {"message": "Semester updated"}

@router.delete("/semesters/{id}", tags=["Academic Structure"])
def delete_semester(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a semester"""
    check_admin(current_user)
    
    sem = session.get(Semester, id)
    if not sem:
        raise HTTPException(status_code=404, detail="Semester not found")
    
    session.delete(sem)
    session.commit()
    return {"message": "Semester deleted"}

# Section CRUD
@router.post("/sections", tags=["Academic Structure"])
def create_section(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a section"""
    check_admin(current_user)
    
    section = Section(
        name=data.get('name'),
        code=data.get('code'),
        semester_id=data.get('semester_id'),
        max_strength=data.get('max_strength', 60),
        is_active=data.get('is_active', True)
    )
    session.add(section)
    session.commit()
    session.refresh(section)
    return {"id": section.id, "message": "Section created"}

@router.patch("/sections/{id}", tags=["Academic Structure"])
def update_section(
    id: int,
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a section"""
    check_admin(current_user)
    
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    for key in ['name', 'max_strength', 'is_active']:
        if key in data:
            setattr(section, key, data[key])
    
    session.add(section)
    session.commit()
    return {"message": "Section updated"}

@router.delete("/sections/{id}", tags=["Academic Structure"])
def delete_section(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a section"""
    check_admin(current_user)
    
    section = session.get(Section, id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    
    # Delete child batches first
    batches = session.exec(select(PracticalBatch).where(PracticalBatch.section_id == id)).all()
    for batch in batches:
        session.delete(batch)
    
    session.delete(section)
    session.commit()
    return {"message": "Section deleted"}

# Practical Batch CRUD
@router.post("/practical-batches", tags=["Academic Structure"])
def create_practical_batch(
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a practical batch"""
    check_admin(current_user)
    
    batch = PracticalBatch(
        name=data.get('name'),
        code=data.get('code'),
        section_id=data.get('section_id'),
        max_strength=data.get('max_strength', 30),
        is_active=data.get('is_active', True)
    )
    session.add(batch)
    session.commit()
    session.refresh(batch)
    return {"id": batch.id, "message": "Practical batch created"}

@router.patch("/practical-batches/{id}", tags=["Academic Structure"])
def update_practical_batch(
    id: int,
    data: dict,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Update a practical batch"""
    check_admin(current_user)
    
    batch = session.get(PracticalBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Practical batch not found")
    
    for key in ['name', 'max_strength', 'is_active']:
        if key in data:
            setattr(batch, key, data[key])
    
    session.add(batch)
    session.commit()
    return {"message": "Practical batch updated"}

@router.delete("/practical-batches/{id}", tags=["Academic Structure"])
def delete_practical_batch(
    id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Delete a practical batch"""
    check_admin(current_user)
    
    batch = session.get(PracticalBatch, id)
    if not batch:
        raise HTTPException(status_code=404, detail="Practical batch not found")
    
    session.delete(batch)
    session.commit()
    return {"message": "Practical batch deleted"}
