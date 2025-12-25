from typing import Optional, List
from pydantic import BaseModel
from datetime import date, datetime
from app.models.library import BookStatus

# --- Book Schemas ---
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    total_copies: int = 1

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int
    available_copies: int
    status: BookStatus

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    total_copies: Optional[int] = None
    status: Optional[BookStatus] = None

# --- Issue Schemas ---
class BookIssueBase(BaseModel):
    book_id: int
    student_id: int
    due_date: date

class BookIssueCreate(BookIssueBase):
    pass

class BookIssueRead(BookIssueBase):
    id: int
    issue_date: date
    return_date: Optional[date] = None
    is_returned: bool

# --- Fine Schemas ---
class LibraryFineRead(BaseModel):
    id: int
    book_issue_id: int
    amount: float
    is_paid: bool
    payment_date: Optional[datetime] = None
    remarks: Optional[str] = None
