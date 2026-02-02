from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlmodel import Session
from app.db.session import get_session
from ..services.easebuzz import easebuzz_service

router = APIRouter()

@router.post("/initiate")
async def initiate_easebuzz_payment(
    request: dict,
    session: Session = Depends(get_session)
):
    """Initiate Easebuzz Payment"""
    return await easebuzz_service.initiate_payment(session, request)

@router.post("/response")
async def handle_easebuzz_response(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """Handle Easebuzz response"""
    form_data = await request.form()
    # Simplified logic, in actual project it should call AdmissionService or FeeService
    return {"status": "success", "txnid": form_data.get("txnid")}

@router.post("/webhook")
async def handle_easebuzz_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """Handle Easebuzz Webhook"""
    form_data = await request.form()
    return {"status": "success", "message": "Webhook processed"}
