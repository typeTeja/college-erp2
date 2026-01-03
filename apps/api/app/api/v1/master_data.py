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
    Designation, Classroom, PlacementCompany,
    EmailTemplate, SMSTemplate
)
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
# Academic Batch Endpoints
# ============================================================================

@router.get("/academic-batches", response_model=List[AcademicBatchRead], tags=["Academic Setup"])
def list_academic_batches(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
    program_id: Optional[int] = None,
    is_active: Optional[bool] = None
):
    """List all academic batches"""
    stmt = select(AcademicBatch)
    if program_id:
        stmt = stmt.where(AcademicBatch.program_id == program_id)
    if is_active is not None:
        stmt = stmt.where(AcademicBatch.is_active == is_active)
    return session.exec(stmt.order_by(AcademicBatch.admission_year.desc())).all()

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
    stmt = select(Classroom)
    if is_active is not None:
        stmt = stmt.where(Classroom.is_active == is_active)
    if room_type:
        stmt = stmt.where(Classroom.room_type == room_type)
    return session.exec(stmt.order_by(Classroom.building, Classroom.floor, Classroom.name)).all()

@router.post("/classrooms", response_model=ClassroomRead, tags=["Infrastructure"])
def create_classroom(
    data: ClassroomCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create a new classroom"""
    check_admin(current_user)
    
    classroom = Classroom(**data.model_dump())
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
    
    classroom = session.get(Classroom, id)
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
    
    classroom = session.get(Classroom, id)
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
