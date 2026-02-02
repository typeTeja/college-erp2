from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser
from ..models import EntranceTestConfig, EntranceExamResult, TentativeAdmission, ScholarshipCalculation
from ..schemas import (
    EntranceTestConfigRead, EntranceTestConfigCreate,
    EntranceExamResultRead, EntranceExamResultCreate,
    TentativeAdmissionRead, TentativeAdmissionCreate
)
from ..services import EntranceExamService, MeritService

router = APIRouter()

# Entrance Test Configuration
@router.post("/test-config", response_model=EntranceTestConfigRead)
async def create_test_config(
    data: EntranceTestConfigCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_superuser)
):
    return EntranceExamService.create_test_config(session, data.dict())

@router.get("/test-config", response_model=list[EntranceTestConfigRead])
async def list_test_configs(
    session: Session = Depends(get_session)
):
    return EntranceExamService.list_test_configs(session)

# Scholarship & Merit
@router.post("/calculate-merit/{application_id}", response_model=dict)
async def calculate_merit(
    application_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_superuser)
):
    calc = MeritService.calculate_scholarship(session, application_id, current_user.id)
    return {"message": "Merit calculated", "calculation_id": calc.id}
