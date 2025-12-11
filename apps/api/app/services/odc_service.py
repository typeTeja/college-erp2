from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, desc
from app.models.odc import (
    ODCHotel, ODCRequest, StudentODCApplication, 
    ODCStatus, ApplicationStatus
)
from app.schemas.odc import (
    ODCHotelCreate, ODCRequestCreate, ApplicationCreate, SelectionUpdate
)
from app.models.student import Student

class ODCService:
    def __init__(self, session: Session):
        self.session = session

    # Hotel Management
    def create_hotel(self, hotel_data: ODCHotelCreate) -> ODCHotel:
        hotel = ODCHotel(**hotel_data.model_dump())
        self.session.add(hotel)
        self.session.commit()
        self.session.refresh(hotel)
        return hotel

    def get_hotels(self, skip: int = 0, limit: int = 100) -> List[ODCHotel]:
        return self.session.exec(
            select(ODCHotel).where(ODCHotel.is_active == True).offset(skip).limit(limit)
        ).all()

    # Request Management
    def create_request(self, request_data: ODCRequestCreate, user_id: int) -> ODCRequest:
        request = ODCRequest(
            **request_data.model_dump(),
            created_by_id=user_id,
            status=ODCStatus.OPEN
        )
        self.session.add(request)
        self.session.commit()
        self.session.refresh(request)
        return request

    def get_requests(self, status: Optional[ODCStatus] = None) -> List[ODCRequest]:
        query = select(ODCRequest)
        if status:
            query = query.where(ODCRequest.status == status)
        query = query.order_by(desc(ODCRequest.event_date))
        return self.session.exec(query).all()

    def get_request_by_id(self, request_id: int) -> Optional[ODCRequest]:
        return self.session.get(ODCRequest, request_id)

    # Application Management
    def apply_for_odc(self, student_id: int, request_id: int) -> StudentODCApplication:
        # Check if already applied
        existing = self.session.exec(
            select(StudentODCApplication).where(
                StudentODCApplication.student_id == student_id,
                StudentODCApplication.request_id == request_id
            )
        ).first()
        
        if existing:
            raise ValueError("Student has already applied for this ODC")
            
        # Check vacancies
        request = self.get_request_by_id(request_id)
        if not request or request.status != ODCStatus.OPEN:
            raise ValueError("ODC Request is closed or invalid")

        application = StudentODCApplication(
            request_id=request_id,
            student_id=student_id,
            status=ApplicationStatus.APPLIED
        )
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application

    def update_selections(self, update_data: SelectionUpdate) -> List[StudentODCApplication]:
        updated_apps = []
        for app_id in update_data.application_ids:
            app = self.session.get(StudentODCApplication, app_id)
            if app:
                app.status = update_data.status
                if update_data.remarks:
                    app.admin_remarks = update_data.remarks
                self.session.add(app)
                updated_apps.append(app)
        
        self.session.commit()
        return updated_apps
    
    def get_student_applications(self, student_id: int) -> List[StudentODCApplication]:
        return self.session.exec(
            select(StudentODCApplication)
            .where(StudentODCApplication.student_id == student_id)
            .order_by(desc(StudentODCApplication.applied_at))
        ).all()
