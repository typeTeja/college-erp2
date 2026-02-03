from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import ApplicationPaymentStatus

if TYPE_CHECKING:
    from .application import Application

class ApplicationPayment(SQLModel, table=True):
    """Tracks application fee payments via Easebuzz or other gateways"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    transaction_id: str = Field(unique=True, index=True)
    amount: float
    status: ApplicationPaymentStatus = Field(default=ApplicationPaymentStatus.PENDING)
    payment_method: Optional[str] = None # Easebuzz, Card, UPI
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="payments")
