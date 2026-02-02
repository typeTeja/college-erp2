from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException

from .models import Book, LibraryMember, BookIssue, LibraryFine
from app.shared.enums import BookStatus, IssueStatus, MemberType


class LibraryCirculationService:
    """Service for library circulation operations (Circulation Owner)"""
    
    FINE_PER_DAY = 5.0
    MAX_FINE_AMOUNT = 500.0
    
    @staticmethod
    def generate_card_number(member_type: MemberType, member_id: int) -> str:
        """Generate unique library card number"""
        prefix = {
            MemberType.STUDENT: "STU",
            MemberType.FACULTY: "FAC",
            MemberType.STAFF: "STF"
        }[member_type]
        
        year = datetime.utcnow().year
        return f"LIB-{prefix}-{year}-{str(member_id).zfill(6)}"
    
    @staticmethod
    def create_membership(
        session: Session,
        student_id: Optional[int] = None,
        user_id: Optional[int] = None,
        member_type: MemberType = MemberType.STUDENT,
        max_books: int = 3
    ) -> LibraryMember:
        """Create library membership"""
        if not student_id and not user_id:
            raise HTTPException(status_code=400, detail="Either student_id or user_id required")
        
        stmt = select(LibraryMember)
        if student_id:
            stmt = stmt.where(LibraryMember.student_id == student_id)
        else:
            stmt = stmt.where(LibraryMember.user_id == user_id)
        
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(status_code=400, detail="Membership already exists")
        
        member_id = student_id or user_id
        card_number = LibraryCirculationService.generate_card_number(member_type, member_id)
        
        member = LibraryMember(
            student_id=student_id,
            user_id=user_id,
            member_type=member_type,
            card_number=card_number,
            max_books=max_books,
            status="ACTIVE"
        )
        
        session.add(member)
        session.commit()
        session.refresh(member)
        return member
    
    @staticmethod
    def issue_book(
        session: Session,
        book_id: int,
        member_id: int,
        due_days: int = 14
    ) -> BookIssue:
        """Issue a book to member"""
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail="Book not available")
        
        member = session.get(LibraryMember, member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        if member.status != "ACTIVE":
            raise HTTPException(status_code=400, detail="Membership inactive")
        
        if member.books_issued_count >= member.max_books:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {member.max_books} books allowed"
            )
        
        due_date = date.today() + timedelta(days=due_days)
        
        issue = BookIssue(
            book_id=book_id,
            library_member_id=member_id,
            due_date=due_date,
            status=IssueStatus.ISSUED
        )
        
        book.available_copies -= 1
        if book.available_copies == 0:
            book.status = BookStatus.ISSUED
            
        member.books_issued_count += 1
        
        session.add(issue)
        session.add(book)
        session.add(member)
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def return_book(
        session: Session,
        issue_id: int
    ) -> BookIssue:
        """Return a book and calculate fine if any"""
        issue = session.get(BookIssue, issue_id)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue record not found")
        
        if issue.status == IssueStatus.RETURNED:
            raise HTTPException(status_code=400, detail="Book already returned")
        
        fine_amount = LibraryCirculationService.calculate_fine(issue.due_date, date.today())
        
        issue.return_date = date.today()
        issue.status = IssueStatus.RETURNED
        issue.is_returned = True
        
        book = session.get(Book, issue.book_id)
        book.available_copies += 1
        book.status = BookStatus.AVAILABLE
        
        member = session.get(LibraryMember, issue.library_member_id)
        member.books_issued_count -= 1
        
        if fine_amount > 0:
            fine = LibraryFine(
                book_issue_id=issue_id,
                amount=fine_amount
            )
            session.add(fine)
        
        session.add(issue)
        session.add(book)
        session.add(member)
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def calculate_fine(due_date: date, return_date: date) -> float:
        """Calculate overdue fine"""
        if return_date <= due_date:
            return 0.0
        
        overdue_days = (return_date - due_date).days
        fine = overdue_days * LibraryCirculationService.FINE_PER_DAY
        return min(fine, LibraryCirculationService.MAX_FINE_AMOUNT)

    @staticmethod
    def get_member_statistics(
        session: Session,
        member_id: int
    ) -> Dict:
        """Get circulation statistics for a member"""
        member = session.get(LibraryMember, member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        stmt = select(BookIssue).where(BookIssue.library_member_id == member_id)
        issues = session.exec(stmt).all()
        
        total_issued = len(issues)
        total_returned = sum(1 for i in issues if i.is_returned)
        overdue = sum(1 for i in issues if not i.is_returned and i.due_date < date.today())
        
        return {
            "member_id": member_id,
            "card_number": member.card_number,
            "total_issued": total_issued,
            "total_returned": total_returned,
            "currently_issued": member.books_issued_count,
            "overdue_count": overdue,
            "status": member.status
        }

library_circulation_service = LibraryCirculationService()
