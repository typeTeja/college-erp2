"""
Library Management Service Layer

Handles business logic for library operations including:
- Book circulation (issue/return)
- Fine calculation
- Membership management
- Digital resource tracking
"""
from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.library import Book, LibraryMember, BookIssue, DigitalResource
from app.models.library import IssueStatus, MemberType, BookCondition


class LibraryService:
    """Service for library operations"""
    
    # Configuration
    FINE_PER_DAY = 5.0  # Fine amount per day
    MAX_FINE_AMOUNT = 500.0  # Maximum fine cap
    
    @staticmethod
    def generate_membership_number(member_type: MemberType, member_id: int) -> str:
        """Generate unique membership number"""
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
        max_books: int = 3,
        validity_days: int = 365
    ) -> LibraryMember:
        """Create library membership"""
        if not student_id and not user_id:
            raise HTTPException(status_code=400, detail="Either student_id or user_id required")
        
        # Check if membership already exists
        stmt = select(LibraryMember)
        if student_id:
            stmt = stmt.where(LibraryMember.student_id == student_id)
        else:
            stmt = stmt.where(LibraryMember.user_id == user_id)
        
        existing = session.exec(stmt).first()
        if existing:
            raise HTTPException(status_code=400, detail="Membership already exists")
        
        # Generate membership number
        member_id = student_id or user_id
        membership_number = LibraryService.generate_membership_number(member_type, member_id)
        
        # Calculate expiry
        expiry_date = date.today() + timedelta(days=validity_days)
        
        member = LibraryMember(
            student_id=student_id,
            user_id=user_id,
            member_type=member_type,
            membership_number=membership_number,
            expiry_date=expiry_date,
            max_books_allowed=max_books
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
        issued_by: int,
        due_days: int = 14
    ) -> BookIssue:
        """Issue a book to member"""
        # Get book
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Check availability
        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail="Book not available")
        
        if book.is_reference_only:
            raise HTTPException(status_code=400, detail="Reference books cannot be issued")
        
        # Get member
        member = session.get(LibraryMember, member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Check member status
        if not member.is_active:
            raise HTTPException(status_code=400, detail="Membership inactive")
        
        if member.is_blocked:
            raise HTTPException(status_code=400, detail=f"Member blocked: {member.block_reason}")
        
        # Check book limit
        if member.current_books_issued >= member.max_books_allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {member.max_books_allowed} books allowed"
            )
        
        # Check pending fines
        if member.pending_fines > 0:
            raise HTTPException(
                status_code=400,
                detail=f"Please clear pending fines: ₹{member.pending_fines}"
            )
        
        # Calculate due date
        due_date = date.today() + timedelta(days=due_days)
        
        # Create issue record
        issue = BookIssue(
            book_id=book_id,
            library_member_id=member_id,
            due_date=due_date,
            issued_by=issued_by,
            issue_condition=book.condition
        )
        
        # Update book availability
        book.available_copies -= 1
        
        # Update member count
        member.current_books_issued += 1
        
        session.add(issue)
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def return_book(
        session: Session,
        issue_id: int,
        returned_to: int,
        return_condition: Optional[BookCondition] = None
    ) -> BookIssue:
        """Return a book"""
        issue = session.get(BookIssue, issue_id)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue record not found")
        
        if issue.status == IssueStatus.RETURNED:
            raise HTTPException(status_code=400, detail="Book already returned")
        
        # Calculate fine
        fine = LibraryService.calculate_fine(issue.due_date, date.today())
        
        # Update issue record
        issue.return_date = date.today()
        issue.returned_to = returned_to
        issue.return_condition = return_condition
        issue.fine_amount = fine
        issue.status = IssueStatus.RETURNED
        
        # Update book availability
        book = session.get(Book, issue.book_id)
        book.available_copies += 1
        
        # Update member
        member = session.get(LibraryMember, issue.library_member_id)
        member.current_books_issued -= 1
        
        if fine > 0:
            member.total_fines += fine
            member.pending_fines += fine
        
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def calculate_fine(due_date: date, return_date: date) -> float:
        """Calculate overdue fine"""
        if return_date <= due_date:
            return 0.0
        
        overdue_days = (return_date - due_date).days
        fine = overdue_days * LibraryService.FINE_PER_DAY
        
        # Cap at maximum
        return min(fine, LibraryService.MAX_FINE_AMOUNT)
    
    @staticmethod
    def renew_book(
        session: Session,
        issue_id: int,
        renewal_days: int = 14
    ) -> BookIssue:
        """Renew book issue"""
        issue = session.get(BookIssue, issue_id)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue record not found")
        
        if issue.status != IssueStatus.ISSUED:
            raise HTTPException(status_code=400, detail="Book not currently issued")
        
        if issue.renewal_count >= issue.max_renewals:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {issue.max_renewals} renewals allowed"
            )
        
        # Check for overdue
        if date.today() > issue.due_date:
            raise HTTPException(status_code=400, detail="Cannot renew overdue books")
        
        # Extend due date
        issue.due_date = issue.due_date + timedelta(days=renewal_days)
        issue.renewal_count += 1
        
        session.commit()
        session.refresh(issue)
        return issue
    
    @staticmethod
    def get_member_statistics(
        session: Session,
        member_id: int
    ) -> Dict:
        """Get member statistics"""
        member = session.get(LibraryMember, member_id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Get all issues
        stmt = select(BookIssue).where(BookIssue.library_member_id == member_id)
        issues = session.exec(stmt).all()
        
        total_issued = len(issues)
        total_returned = sum(1 for i in issues if i.status == IssueStatus.RETURNED)
        currently_issued = member.current_books_issued
        overdue = sum(1 for i in issues if i.status == IssueStatus.ISSUED and i.due_date < date.today())
        
        return {
            "member_id": member_id,
            "membership_number": member.membership_number,
            "total_books_issued": total_issued,
            "total_books_returned": total_returned,
            "currently_issued": currently_issued,
            "overdue_books": overdue,
            "total_fines": float(member.total_fines),
            "pending_fines": float(member.pending_fines),
            "is_active": member.is_active,
            "is_blocked": member.is_blocked
        }
