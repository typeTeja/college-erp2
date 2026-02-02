"""
Library Domain Models

Resource and circulation models for library management.
"""

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from app.shared.enums import BookStatus, MemberType, IssueStatus


if TYPE_CHECKING:
    from app.domains.student.models.student import Student


# ======================================================================
# Resource Models
# ======================================================================

class Book(SQLModel, table=True):
    """Intellectual Resource - Library Collection Item"""
    __tablename__ = "library_book"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    isbn: str = Field(unique=True, index=True)
    publisher: Optional[str] = None
    category: Optional[str] = None # e.g., "Computer Science", "Fiction"
    location: Optional[str] = None # Rack number / Shelf
    total_copies: int = Field(default=1)
    available_copies: int = Field(default=1)
    status: BookStatus = Field(default=BookStatus.AVAILABLE)
    
    # Relationships
    issues: List["BookIssue"] = Relationship(back_populates="book")


class LibraryMember(SQLModel, table=True):
    """Library Patron - Access and Loan Limits"""
    __tablename__ = "library_member"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
    member_type: MemberType = Field(default=MemberType.STUDENT)
    card_number: str = Field(unique=True, index=True)
    max_books: int = Field(default=3)
    books_issued_count: int = Field(default=0)
    status: str = Field(default="ACTIVE")
    joined_date: date = Field(default_factory=date.today)
    
    issues: List["BookIssue"] = Relationship(back_populates="member")


class DigitalResource(SQLModel, table=True):
    """Digital Asset - Electronic Access Resource"""
    __tablename__ = "digital_resource"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    resource_type: str # E-Book, Journal, Video
    url: str
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    view_count: int = Field(default=0)
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


# ======================================================================
# Circulation Models
# ======================================================================

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
