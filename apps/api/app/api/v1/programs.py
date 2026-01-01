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
    programs = session.exec(select(Program)).all()
    
    # Manually construct response with department_name
    return [
        ProgramRead(
            id=program.id,
            code=program.code,
            name=program.name,
            duration_years=program.duration_years,
            description=program.description,
            department_name=program.department.name if program.department else "Unknown"
        )
        for program in programs
    ]
