from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, desc, func
from ..models.odc import (
    ODCHotel, ODCRequest, StudentODCApplication, ODCBilling, ODCPayout,
    ODCStatus, ApplicationStatus as ODCApplicationStatus, BillingStatus,
    PaymentMethod as ODCPaymentMethod
)
from ..models.student import Student

class ODCService:
    @staticmethod
    def get_hotels(session: Session, skip: int = 0, limit: int = 100) -> List[ODCHotel]:
        return session.exec(
            select(ODCHotel).where(ODCHotel.is_active == True).offset(skip).limit(limit)
        ).all()

    @staticmethod
    def create_request(session: Session, request_data: dict, user_id: int) -> ODCRequest:
        request = ODCRequest(
            **request_data,
            created_by_id=user_id,
            status=ODCStatus.OPEN
        )
        session.add(request)
        session.commit()
        session.refresh(request)
        return request

    @staticmethod
    def get_requests(session: Session, status: Optional[ODCStatus] = None) -> List[ODCRequest]:
        query = select(ODCRequest)
        if status:
            query = query.where(ODCRequest.status == status)
        query = query.order_by(desc(ODCRequest.event_date))
        return session.exec(query).all()

    @staticmethod
    def apply_for_odc(session: Session, student_id: int, request_id: int) -> StudentODCApplication:
        existing = session.exec(
            select(StudentODCApplication).where(
                StudentODCApplication.student_id == student_id,
                StudentODCApplication.request_id == request_id
            )
        ).first()
        if existing:
            raise ValueError("Student has already applied for this ODC")
            
        request = session.get(ODCRequest, request_id)
        if not request or request.status != ODCStatus.OPEN:
            raise ValueError("ODC Request is closed or invalid")

        application = StudentODCApplication(
            request_id=request_id,
            student_id=student_id,
            status=ODCApplicationStatus.APPLIED
        )
        session.add(application)
        session.commit()
        session.refresh(application)
        return application

odc_service = ODCService()
