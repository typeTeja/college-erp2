from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_current_active_superuser, get_session
from ..models.system import InstituteInfo
from ..schemas.institute import InstituteInfoCreate, InstituteInfoRead

router = APIRouter()

@router.get("/", response_model=InstituteInfoRead, tags=["System - Institute"])
def get_institute_info(*, session: Session = Depends(get_session), current_user = Depends(deps.get_current_active_superuser)):
    institute = session.exec(select(InstituteInfo)).first()
    if not institute:
        return InstituteInfoRead(id=0, name="", short_code="")
    return institute

@router.put("/", response_model=InstituteInfoRead, tags=["System - Institute"])
def update_institute_info(*, session: Session = Depends(get_session), data: InstituteInfoCreate, current_user = Depends(deps.get_current_active_superuser)):
    institute = session.exec(select(InstituteInfo)).first()
    if not institute:
        institute = InstituteInfo(**data.model_dump())
        session.add(institute)
    else:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(institute, key, value)
    session.commit()
    session.refresh(institute)
    return institute
