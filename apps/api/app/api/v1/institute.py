from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_active_superuser, get_session
from app.models.institute import InstituteInfo
from app.schemas.institute import InstituteInfoCreate, InstituteInfoRead
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=InstituteInfoRead)
def get_institute_info(*, session: Session = Depends(get_session), _: User = Depends(get_current_active_superuser)):
    institute = session.exec(select(InstituteInfo)).first()
    if not institute:
        # Return default empty institute for initial setup
        return InstituteInfoRead(
            id=0,
            name="",
            short_code="",
            address="",
            contact_email="",
            contact_phone="",
            logo_url=""
        )
    return institute

@router.put("/", response_model=InstituteInfoRead)
def update_institute_info(*, session: Session = Depends(get_session), data: InstituteInfoCreate, _: User = Depends(get_current_active_superuser)):
    institute = session.exec(select(InstituteInfo)).first()
    if not institute:
        institute = InstituteInfo(**data.dict())
        session.add(institute)
    else:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(institute, key, value)
    session.commit()
    session.refresh(institute)
    return institute
