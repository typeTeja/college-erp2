from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.library import Book, BookIssue, LibraryFine, BookStatus
from app.schemas.library import BookCreate, BookRead, BookUpdate, BookIssueCreate, BookIssueRead
from typing import List, Optional
from datetime import date, datetime

router = APIRouter()

@router.get("/books", response_model=List[BookRead])
def list_books(
    session: Session = Depends(get_session),
    search: Optional[str] = None,
    category: Optional[str] = None
):
    statement = select(Book)
    if search:
        statement = statement.where(Book.title.contains(search) | Book.author.contains(search) | Book.isbn.contains(search))
    if category:
        statement = statement.where(Book.category == category)
    return session.exec(statement).all()

@router.post("/books", response_model=BookRead)
def create_book(data: BookCreate, session: Session = Depends(get_session)):
    book = Book(**data.dict(), available_copies=data.total_copies)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@router.post("/issue", response_model=BookIssueRead)
def issue_book(data: BookIssueCreate, session: Session = Depends(get_session)):
    book = session.get(Book, data.book_id)
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available for issue")
    
    issue = BookIssue(**data.dict())
    book.available_copies -= 1
    if book.available_copies == 0:
        book.status = BookStatus.ISSUED
        
    session.add(issue)
    session.add(book)
    session.commit()
    session.refresh(issue)
    return issue

@router.post("/return/{issue_id}", response_model=BookIssueRead)
def return_book(issue_id: int, session: Session = Depends(get_session)):
    issue = session.get(BookIssue, issue_id)
    if not issue or issue.is_returned:
        raise HTTPException(status_code=400, detail="Invalid issue record")
    
    issue.return_date = date.today()
    issue.is_returned = True
    
    book = session.get(Book, issue.book_id)
    book.available_copies += 1
    book.status = BookStatus.AVAILABLE
    
    # Simple fine calculation: ₹5 per day overdue
    if issue.return_date > issue.due_date:
        overdue_days = (issue.return_date - issue.due_date).days
        fine_amount = overdue_days * 5.0
        fine = LibraryFine(book_issue_id=issue.id, amount=fine_amount)
        session.add(fine)
    
    session.add(issue)
    session.add(book)
    session.commit()
    session.refresh(issue)
    return issue
