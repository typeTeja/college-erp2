from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_session
from app.models.institute import InstituteInfo
from app.schemas.institute import InstituteInfoCreate, InstituteInfoRead
from app.models.user import User

router = APIRouter()

def admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return current_user

@router.get("/", response_model=InstituteInfoRead)
def get_institute_info(*, session: Session = Depends(get_session), _: User = Depends(admin_user)):
    institute = session.exec(select(InstituteInfo)).first()
    if not institute:
        raise HTTPException(status_code=404, detail="Institute info not found")
    return institute

@router.put("/", response_model=InstituteInfoRead)
def update_institute_info(*, session: Session = Depends(get_session), data: InstituteInfoCreate, _: User = Depends(admin_user)):
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
