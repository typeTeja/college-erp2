from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import date

from app.api.deps import get_session, get_current_active_superuser, get_current_user
from app.models import User
from ..models import Book, LibraryMember, DigitalResource, BookIssue
from .services import library_circulation_service
from app.shared.enums import IssueStatus, MemberType, BookStatus


router = APIRouter(prefix="/library", tags=["Library Circulation"])

# Schemas
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    total_copies: int = 1

class MembershipCreate(BaseModel):
    student_id: Optional[int] = None
    user_id: Optional[int] = None
    member_type: MemberType = MemberType.STUDENT
    max_books: int = 3

class BookIssueRequest(BaseModel):
    book_id: int
    member_id: int
    due_days: int = 14

# ============================================================================
# Book Management Endpoints
# ============================================================================

@router.post("/books", response_model=Book)
def create_book(
    *,
    session: Session = Depends(get_session),
    book_data: BookCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Add a new book to the library catalog"""
    book = Book(**book_data.model_dump(), available_copies=book_data.total_copies)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.get("/books", response_model=List[Book])
def list_books(
    *,
    session: Session = Depends(get_session),
    category: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    available_only: bool = Query(False),
    limit: int = Query(100)
):
    """List books in the catalog with filters"""
    stmt = select(Book)
    if category:
        stmt = stmt.where(Book.category == category)
    if author:
        stmt = stmt.where(Book.author.contains(author))
    if available_only:
        stmt = stmt.where(Book.available_copies > 0)
    
    return session.exec(stmt.limit(limit)).all()

# ============================================================================
# Membership Endpoints
# ============================================================================

@router.post("/members", response_model=LibraryMember)
def create_membership(
    *,
    session: Session = Depends(get_session),
    member_data: MembershipCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new library membership"""
    return library_circulation_service.create_membership(
        session,
        member_data.student_id,
        member_data.user_id,
        member_data.member_type,
        member_data.max_books
    )

@router.get("/members/{member_id}/statistics")
def get_member_statistics(
    *,
    session: Session = Depends(get_session),
    member_id: int
):
    """Get circulation statistics for a member"""
    return library_circulation_service.get_member_statistics(session, member_id)

# ============================================================================
# Circulation Endpoints
# ============================================================================

@router.post("/issue", response_model=BookIssue)
def issue_book(
    *,
    session: Session = Depends(get_session),
    issue_data: BookIssueRequest,
    current_user: User = Depends(get_current_user)
):
    """Issue a book to a member"""
    return library_circulation_service.issue_book(
        session,
        issue_data.book_id,
        issue_data.member_id,
        issue_data.due_days
    )

@router.post("/return/{issue_id}", response_model=BookIssue)
def return_book(
    *,
    session: Session = Depends(get_session),
    issue_id: int
):
    """Return an issued book"""
    return library_circulation_service.return_book(session, issue_id)

@router.get("/issues", response_model=List[BookIssue])
def list_issues(
    *,
    session: Session = Depends(get_session),
    member_id: Optional[int] = Query(None),
    status: Optional[IssueStatus] = Query(None),
    overdue_only: bool = Query(False),
    limit: int = Query(100)
):
    """List book issues with filters"""
    stmt = select(BookIssue)
    if member_id:
        stmt = stmt.where(BookIssue.library_member_id == member_id)
    if status:
        stmt = stmt.where(BookIssue.status == status)
    if overdue_only:
        stmt = stmt.where(BookIssue.is_returned == False, BookIssue.due_date < date.today())
    
    return session.exec(stmt.order_by(BookIssue.issue_date.desc()).limit(limit)).all()
