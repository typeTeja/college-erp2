from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from enum import Enum
from app.shared.enums import IssueStatus


if TYPE_CHECKING:
    from .resource import Book, LibraryMember


class BookIssue(SQLModel, table=True):
    """Loan Record - Tracking intellectual resource usage"""
    __tablename__ = "book_issue"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="library_book.id")
    library_member_id: int = Field(foreign_key="library_member.id")
    issue_date: date = Field(default_factory=date.today)
    due_date: date
    return_date: Optional[date] = None
    status: IssueStatus = Field(default=IssueStatus.ISSUED)
    is_returned: bool = Field(default=False)
    
    # Relationships
    book: "Book" = Relationship(back_populates="issues")
    member: "LibraryMember" = Relationship(back_populates="issues")

class LibraryFine(SQLModel, table=True):
    """Monetary Penalty - Overdue or damaged resource fee"""
    __tablename__ = "library_fine"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    book_issue_id: int = Field(foreign_key="book_issue.id")
    amount: float
    is_paid: bool = Field(default=False)
    payment_date: Optional[datetime] = None
    remarks: Optional[str] = None
