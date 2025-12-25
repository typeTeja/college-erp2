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

class BookIssue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    student_id: int = Field(foreign_key="student.id")
    issue_date: date = Field(default_factory=date.today)
    due_date: date
    return_date: Optional[date] = None
    is_returned: bool = Field(default=False)
    
    # Relationships
    book: Book = Relationship(back_populates="issues")
    # student: "Student" = Relationship() # Link once student model is verified

class LibraryFine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_issue_id: int = Field(foreign_key="bookissue.id")
    amount: float
    is_paid: bool = Field(default=False)
    payment_date: Optional[datetime] = None
    remarks: Optional[str] = None
