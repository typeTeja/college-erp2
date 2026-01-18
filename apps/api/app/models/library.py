from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from enum import Enum

if TYPE_CHECKING:
    from .student import Student

class BookStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"
    LOST = "LOST"
    DAMAGED = "DAMAGED"

class IssueStatus(str, Enum):
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    LOST = "LOST"

class BookCondition(str, Enum):
    GOOD = "GOOD"
    DAMAGED = "DAMAGED"
    LOST = "LOST"
    REPAIRED = "REPAIRED"

class MemberType(str, Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"
    STAFF = "STAFF"

class Book(SQLModel, table=True):
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
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id", nullable=True)
    student_id: Optional[int] = Field(foreign_key="student.id", nullable=True)
    member_type: MemberType = Field(default=MemberType.STUDENT)
    card_number: str = Field(unique=True, index=True)
    max_books: int = Field(default=3)
    books_issued_count: int = Field(default=0)
    status: str = Field(default="ACTIVE")
    joined_date: date = Field(default_factory=date.today)
    
    issues: List["BookIssue"] = Relationship(back_populates="member")

class BookIssue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    library_member_id: int = Field(foreign_key="librarymember.id")
    issue_date: date = Field(default_factory=date.today)
    due_date: date
    return_date: Optional[date] = None
    status: IssueStatus = Field(default=IssueStatus.ISSUED)
    is_returned: bool = Field(default=False)
    
    # Relationships
    book: Book = Relationship(back_populates="issues")
    member: LibraryMember = Relationship(back_populates="issues")

class LibraryFine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_issue_id: int = Field(foreign_key="bookissue.id")
    amount: float
    is_paid: bool = Field(default=False)
    payment_date: Optional[datetime] = None
    remarks: Optional[str] = None

class DigitalResource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    category: str
    resource_type: str # E-Book, Journal, Video
    url: str
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    view_count: int = Field(default=0)
    uploaded_at: datetime = Field(default_factory=datetime.now)
