"""
Student Assignment API Endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api import deps
from app.models.user import User
from app.services.student_assignment_service import StudentAssignmentService
from app.schemas.student_assignment import (
    AutoAssignRequest,
    AutoAssignResponse,
    StudentSectionAssignmentCreate,
    StudentSectionAssignmentRead,
    ReassignRequest,
    SectionRosterResponse,
    SectionRosterStudent,
    UnassignedStudentsResponse
)
from app.models.master_data import Section

router = APIRouter()


@router.post("/sections/auto-assign", response_model=AutoAssignResponse)
def auto_assign_students_to_sections(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    data: AutoAssignRequest
):
    """
    Automatically assign all unassigned students to sections
    
    Distributes students evenly across available sections using round-robin algorithm.
    Respects section capacity limits.
    """
    result = StudentAssignmentService.assign_students_to_sections_auto(
        session=session,
        batch_id=data.batch_id,
        semester_no=data.semester_no,
        user_id=current_user.id
    )
    return result


@router.post("/sections/manual-assign", response_model=StudentSectionAssignmentRead)
def manual_assign_student_to_section(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    data: StudentSectionAssignmentCreate
):
    """
    Manually assign a specific student to a section
    
    Validates capacity and prevents duplicate assignments.
    """
    assignment = StudentAssignmentService.assign_student_to_section_manual(
        session=session,
        student_id=data.student_id,
        section_id=data.section_id,
        batch_id=data.batch_id,
        semester_no=data.semester_no,
        user_id=current_user.id
    )
    return assignment


@router.patch("/sections/{assignment_id}/reassign", response_model=StudentSectionAssignmentRead)
def reassign_student_to_section(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    assignment_id: int,
    data: ReassignRequest
):
    """
    Reassign a student to a different section
    
    Updates section capacities and creates audit trail.
    """
    assignment = StudentAssignmentService.reassign_student(
        session=session,
        assignment_id=assignment_id,
        new_section_id=data.new_section_id,
        user_id=current_user.id
    )
    return assignment


@router.delete("/sections/{assignment_id}")
def delete_section_assignment(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    assignment_id: int
):
    """
    Delete a student section assignment
    
    Soft deletes the assignment and updates section capacity.
    """
    StudentAssignmentService.delete_assignment(
        session=session,
        assignment_id=assignment_id,
        user_id=current_user.id
    )
    return {"message": "Assignment deleted successfully"}


@router.get("/sections/{section_id}/roster", response_model=SectionRosterResponse)
def get_section_roster(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    section_id: int
):
    """
    Get list of students assigned to a section
    
    Returns student details with assignment information.
    """
    section = session.get(Section, section_id)
    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section {section_id} not found"
        )
    
    roster = StudentAssignmentService.get_section_roster(
        session=session,
        section_id=section_id
    )
    
    return SectionRosterResponse(
        section_id=section.id,
        section_name=section.name,
        section_code=section.code,
        current_strength=section.current_strength,
        max_strength=section.max_strength,
        students=[SectionRosterStudent(**student) for student in roster]
    )


@router.get("/batches/{batch_id}/unassigned", response_model=UnassignedStudentsResponse)
def get_unassigned_students(
    *,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_active_superuser),
    batch_id: int,
    semester_no: int
):
    """
    Get students not assigned to any section for a semester
    
    Useful for identifying students who need assignment.
    """
    students = StudentAssignmentService.get_unassigned_students(
        session=session,
        batch_id=batch_id,
        semester_no=semester_no
    )
    
    return UnassignedStudentsResponse(
        batch_id=batch_id,
        semester_no=semester_no,
        count=len(students),
        students=[{
            "id": s.id,
            "name": s.name,
            "roll_number": s.roll_number,
            "email": s.email
        } for s in students]
    )
