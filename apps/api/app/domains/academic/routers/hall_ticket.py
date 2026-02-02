"""
Hall Ticket API Endpoints

Provides comprehensive hall ticket management functionality
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.domains.academic.models import (
    HallTicketConfig, HallTicket, DisciplineBlock
)
from app.schemas.academic.hall_ticket import (
    HallTicketConfigCreate, HallTicketConfigUpdate, HallTicketConfigResponse,
    HallTicketResponse, HallTicketGenerateRequest, BulkHallTicketGenerateRequest,
    BulkGenerationResponse, EligibilityCheckResponse,
    CancelHallTicketRequest, ReissueHallTicketRequest,
    DisciplineBlockCreate, DisciplineBlockResponse, UnblockStudentRequest
)
from app.domains.academic.services.hall_ticket_service import HallTicketService

router = APIRouter(prefix="/hall-tickets", tags=["Hall Tickets"])


# ============================================================================
# Configuration Endpoints
# ============================================================================

@router.post("/config", response_model=HallTicketConfigResponse)
def create_hall_ticket_config(
    *,
    session: Session = Depends(get_session),
    config_data: HallTicketConfigCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new hall ticket configuration"""
    config = HallTicketConfig(
        **config_data.model_dump(),
        created_by=current_user.id
    )
    session.add(config)
    session.commit()
    session.refresh(config)
    return config


@router.get("/config", response_model=List[HallTicketConfigResponse])
def list_hall_ticket_configs(
    *,
    session: Session = Depends(get_session),
    academic_year: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List hall ticket configurations"""
    stmt = select(HallTicketConfig)
    
    if academic_year:
        stmt = stmt.where(HallTicketConfig.academic_year == academic_year)
    if is_active is not None:
        stmt = stmt.where(HallTicketConfig.is_active == is_active)
    
    stmt = stmt.offset(skip).limit(limit).order_by(HallTicketConfig.created_at.desc())
    return session.exec(stmt).all()


@router.get("/config/{config_id}", response_model=HallTicketConfigResponse)
def get_hall_ticket_config(
    *,
    session: Session = Depends(get_session),
    config_id: int
):
    """Get a specific hall ticket configuration"""
    config = session.get(HallTicketConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config


@router.put("/config/{config_id}", response_model=HallTicketConfigResponse)
def update_hall_ticket_config(
    *,
    session: Session = Depends(get_session),
    config_id: int,
    config_data: HallTicketConfigUpdate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Update hall ticket configuration"""
    config = session.get(HallTicketConfig, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    
    for key, value in config_data.model_dump(exclude_unset=True).items():
        setattr(config, key, value)
    
    session.commit()
    session.refresh(config)
    return config


# ============================================================================
# Eligibility & Generation Endpoints
# ============================================================================

@router.get("/eligibility/{student_id}/{config_id}", response_model=EligibilityCheckResponse)
def check_eligibility(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    config_id: int
):
    """Check if student is eligible for hall ticket"""
    return HallTicketService.check_eligibility(session, student_id, config_id)


@router.post("/generate", response_model=HallTicketResponse)
def generate_hall_ticket(
    *,
    session: Session = Depends(get_session),
    request: HallTicketGenerateRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Generate hall ticket for a student"""
    return HallTicketService.generate_hall_ticket(
        session,
        request.student_id,
        request.config_id,
        current_user.id,
        request.force
    )


@router.post("/bulk-generate", response_model=BulkGenerationResponse)
def bulk_generate_hall_tickets(
    *,
    session: Session = Depends(get_session),
    request: BulkHallTicketGenerateRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Bulk generate hall tickets"""
    result = HallTicketService.bulk_generate(
        session,
        request.config_id,
        request.student_ids,
        current_user.id,
        request.force
    )
    
    return BulkGenerationResponse(
        success=result["success"],
        failed=result["failed"],
        total_success=len(result["success"]),
        total_failed=len(result["failed"])
    )


# ============================================================================
# Hall Ticket Management Endpoints
# ============================================================================

@router.get("", response_model=List[HallTicketResponse])
def list_hall_tickets(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    config_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List hall tickets with filters"""
    stmt = select(HallTicket)
    
    if student_id:
        stmt = stmt.where(HallTicket.student_id == student_id)
    if config_id:
        stmt = stmt.where(HallTicket.hall_ticket_config_id == config_id)
    if status:
        stmt = stmt.where(HallTicket.status == status)
    
    stmt = stmt.offset(skip).limit(limit).order_by(HallTicket.generated_at.desc())
    return session.exec(stmt).all()


@router.get("/{hall_ticket_number}", response_model=HallTicketResponse)
def get_hall_ticket(
    *,
    session: Session = Depends(get_session),
    hall_ticket_number: str
):
    """Get hall ticket by number"""
    stmt = select(HallTicket).where(HallTicket.hall_ticket_number == hall_ticket_number)
    hall_ticket = session.exec(stmt).first()
    
    if not hall_ticket:
        raise HTTPException(status_code=404, detail="Hall ticket not found")
    return hall_ticket


@router.post("/{hall_ticket_id}/download", response_model=HallTicketResponse)
def track_download(
    *,
    session: Session = Depends(get_session),
    hall_ticket_id: int
):
    """Track hall ticket download"""
    return HallTicketService.track_download(session, hall_ticket_id)


@router.post("/{hall_ticket_id}/cancel", response_model=HallTicketResponse)
def cancel_hall_ticket(
    *,
    session: Session = Depends(get_session),
    hall_ticket_id: int,
    request: CancelHallTicketRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Cancel a hall ticket"""
    return HallTicketService.cancel_hall_ticket(
        session,
        hall_ticket_id,
        current_user.id,
        request.reason
    )


@router.post("/{hall_ticket_id}/reissue", response_model=HallTicketResponse)
def reissue_hall_ticket(
    *,
    session: Session = Depends(get_session),
    hall_ticket_id: int,
    request: ReissueHallTicketRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Reissue a hall ticket"""
    return HallTicketService.reissue_hall_ticket(
        session,
        hall_ticket_id,
        current_user.id,
        request.reason
    )


# ============================================================================
# Discipline Block Endpoints
# ============================================================================

@router.post("/blocks", response_model=DisciplineBlockResponse)
def block_student(
    *,
    session: Session = Depends(get_session),
    block_data: DisciplineBlockCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Block a student from hall ticket generation"""
    return HallTicketService.block_student(
        session,
        block_data.student_id,
        block_data.block_reason,
        block_data.block_description,
        current_user.id
    )


@router.get("/blocks", response_model=List[DisciplineBlockResponse])
def list_discipline_blocks(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List discipline blocks"""
    stmt = select(DisciplineBlock)
    
    if student_id:
        stmt = stmt.where(DisciplineBlock.student_id == student_id)
    if is_active is not None:
        stmt = stmt.where(DisciplineBlock.is_active == is_active)
    
    stmt = stmt.offset(skip).limit(limit).order_by(DisciplineBlock.created_at.desc())
    return session.exec(stmt).all()


@router.post("/blocks/{block_id}/unblock", response_model=DisciplineBlockResponse)
def unblock_student(
    *,
    session: Session = Depends(get_session),
    block_id: int,
    request: UnblockStudentRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Unblock a student"""
    return HallTicketService.unblock_student(
        session,
        block_id,
        current_user.id,
        request.remarks
    )


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/stats/config/{config_id}")
def get_hall_ticket_statistics(
    *,
    session: Session = Depends(get_session),
    config_id: int
):
    """Get statistics for a hall ticket configuration"""
    stmt = select(HallTicket).where(HallTicket.hall_ticket_config_id == config_id)
    tickets = session.exec(stmt).all()
    
    total = len(tickets)
    downloaded = sum(1 for t in tickets if t.download_count > 0)
    cancelled = sum(1 for t in tickets if t.status == "CANCELLED")
    reissued = sum(1 for t in tickets if t.status == "REISSUED")
    
    return {
        "config_id": config_id,
        "total_generated": total,
        "downloaded": downloaded,
        "not_downloaded": total - downloaded,
        "cancelled": cancelled,
        "reissued": reissued,
        "download_percentage": round((downloaded / total * 100) if total > 0 else 0, 2)
    }
