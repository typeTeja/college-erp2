from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.program import Program
from app.schemas.program import ProgramRead
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProgramRead])
def get_programs(session: Session = Depends(get_session)):
    """Public list of programs for application forms"""
    return session.exec(select(Program)).all()
