"""
Library Management API Endpoints

Provides library management functionality
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import date

from app.api.deps import get_session, get_current_active_superuser, get_current_user
from app.models.user import User
from app.models.library import Book, LibraryMember, BookIssue, DigitalResource, MemberType
from app.services.library_service import LibraryService

router = APIRouter(prefix="/library", tags=["Library Management"])


# Schemas
class BookCreate(BaseModel):
    isbn: Optional[str] = None
    accession_number: str
    title: str
    author: str
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    category: str
    total_copies: int = 1
    price: float = 0.0


class MembershipCreate(BaseModel):
    student_id: Optional[int] = None
    user_id: Optional[int] = None
    member_type: str
    max_books: int = 3


class BookIssueRequest(BaseModel):
    book_id: int
    member_id: int
    due_days: int = 14


# ============================================================================
# Book Management Endpoints
# ============================================================================

@router.post("/books")
def create_book(
    *,
    session: Session = Depends(get_session),
    book_data: BookCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Add new book to catalog"""
    book = Book(**book_data.model_dump(), available_copies=book_data.total_copies)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/books")
def list_books(
    *,
    session: Session = Depends(get_session),
    category: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    available_only: bool = Query(False),
    limit: int = Query(50, le=100)
):
    """List books with filters"""
    stmt = select(Book)
    
    if category:
        stmt = stmt.where(Book.category == category)
    if author:
        stmt = stmt.where(Book.author.contains(author))
    if search:
        stmt = stmt.where(
            (Book.title.contains(search)) | (Book.author.contains(search))
        )
    if available_only:
        stmt = stmt.where(Book.available_copies > 0)
    
    stmt = stmt.limit(limit)
    return session.exec(stmt).all()


@router.get("/books/{book_id}")
def get_book(
    *,
    session: Session = Depends(get_session),
    book_id: int
):
    """Get book details"""
    book = session.get(Book, book_id)
    if not book:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Book not found")
    return book


# ============================================================================
# Membership Endpoints
# ============================================================================

@router.post("/members")
def create_membership(
    *,
    session: Session = Depends(get_session),
    membership_data: MembershipCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create library membership"""
    return LibraryService.create_membership(
        session,
        membership_data.student_id,
        membership_data.user_id,
        MemberType(membership_data.member_type),
        membership_data.max_books
    )


@router.get("/members/{member_id}")
def get_member(
    *,
    session: Session = Depends(get_session),
    member_id: int
):
    """Get member details"""
    member = session.get(LibraryMember, member_id)
    if not member:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.get("/members/{member_id}/statistics")
def get_member_statistics(
    *,
    session: Session = Depends(get_session),
    member_id: int
):
    """Get member statistics"""
    return LibraryService.get_member_statistics(session, member_id)


# ============================================================================
# Book Circulation Endpoints
# ============================================================================

@router.post("/issue")
def issue_book(
    *,
    session: Session = Depends(get_session),
    issue_data: BookIssueRequest,
    current_user: User = Depends(get_current_user)
):
    """Issue a book"""
    return LibraryService.issue_book(
        session,
        issue_data.book_id,
        issue_data.member_id,
        current_user.id,
        issue_data.due_days
    )


@router.post("/return/{issue_id}")
def return_book(
    *,
    session: Session = Depends(get_session),
    issue_id: int,
    current_user: User = Depends(get_current_user)
):
    """Return a book"""
    return LibraryService.return_book(session, issue_id, current_user.id)


@router.post("/renew/{issue_id}")
def renew_book(
    *,
    session: Session = Depends(get_session),
    issue_id: int
):
    """Renew book issue"""
    return LibraryService.renew_book(session, issue_id)


@router.get("/issues")
def list_issues(
    *,
    session: Session = Depends(get_session),
    member_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    overdue_only: bool = Query(False),
    limit: int = Query(50)
):
    """List book issues"""
    stmt = select(BookIssue)
    
    if member_id:
        stmt = stmt.where(BookIssue.library_member_id == member_id)
    if status:
        stmt = stmt.where(BookIssue.status == status)
    if overdue_only:
        from datetime import date
        stmt = stmt.where(
            BookIssue.status == "ISSUED",
            BookIssue.due_date < date.today()
        )
    
    stmt = stmt.order_by(BookIssue.issue_date.desc()).limit(limit)
    return session.exec(stmt).all()


# ============================================================================
# Digital Resources Endpoints
# ============================================================================

@router.get("/digital-resources")
def list_digital_resources(
    *,
    session: Session = Depends(get_session),
    resource_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(50)
):
    """List digital resources"""
    stmt = select(DigitalResource).where(DigitalResource.is_active == True)
    
    if resource_type:
        stmt = stmt.where(DigitalResource.resource_type == resource_type)
    if category:
        stmt = stmt.where(DigitalResource.category == category)
    
    stmt = stmt.limit(limit)
    return session.exec(stmt).all()


@router.get("/digital-resources/{resource_id}")
def get_digital_resource(
    *,
    session: Session = Depends(get_session),
    resource_id: int
):
    """Get digital resource and track view"""
    resource = session.get(DigitalResource, resource_id)
    if not resource:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Increment view count
    resource.view_count += 1
    session.commit()
    
    return resource


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/summary")
def get_library_statistics(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get library statistics"""
    total_books = len(session.exec(select(Book)).all())
    total_members = len(session.exec(select(LibraryMember)).all())
    active_issues = len(session.exec(
        select(BookIssue).where(BookIssue.status == "ISSUED")
    ).all())
    
    from datetime import date
    overdue_issues = len(session.exec(
        select(BookIssue).where(
            BookIssue.status == "ISSUED",
            BookIssue.due_date < date.today()
        )
    ).all())
    
    return {
        "total_books": total_books,
        "total_members": total_members,
        "active_issues": active_issues,
        "overdue_issues": overdue_issues
    }
