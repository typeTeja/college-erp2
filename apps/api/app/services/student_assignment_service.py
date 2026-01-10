"""
Student Assignment Service
Handles automatic and manual assignment of students to sections and labs
"""
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select, func
from fastapi import HTTPException, status

from app.models.student import Student
from app.models.master_data import Section, PracticalBatch
from app.models.academic.batch import AcademicBatch, BatchSemester
from app.models.academic.assignment import StudentSectionAssignment, StudentLabAssignment
from app.utils.audit import log_create, log_delete


class StudentAssignmentService:
    """Service for student assignment operations"""
    
    @staticmethod
    def assign_students_to_sections_auto(
        session: Session,
        batch_id: int,
        semester_no: int,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Automatically assign all unassigned students to sections
        
        Algorithm:
        1. Get all students in batch without section assignment for this semester
        2. Get all active sections for this semester
        3. Sort students by roll number
        4. Distribute round-robin across sections
        5. Respect capacity limits
        6. Create assignment records
        7. Update section current_strength
        
        Returns:
            Statistics about assignments created
        """
        # Get batch
        batch = session.get(AcademicBatch, batch_id)
        if not batch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Batch {batch_id} not found"
            )
        
        # Get semester
        semester = session.exec(
            select(BatchSemester)
            .where(BatchSemester.batch_id == batch_id)
            .where(BatchSemester.semester_no == semester_no)
        ).first()
        
        if not semester:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Semester {semester_no} not found for batch {batch_id}"
            )
        
        # Get sections for this semester
        sections = session.exec(
            select(Section)
            .where(Section.batch_semester_id == semester.id)
            .where(Section.is_active == True)
            .order_by(Section.code)
        ).all()
        
        if not sections:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No sections found for semester {semester_no}"
            )
        
        # Get already assigned student IDs for this semester
        assigned_student_ids = session.exec(
            select(StudentSectionAssignment.student_id)
            .where(StudentSectionAssignment.batch_id == batch_id)
            .where(StudentSectionAssignment.semester_no == semester_no)
            .where(StudentSectionAssignment.is_active == True)
        ).all()
        
        # Get unassigned students in this batch
        # TODO: Add proper student-batch relationship query
        # For now, assuming students have batch_id field
        unassigned_students = session.exec(
            select(Student)
            .where(Student.id.not_in(assigned_student_ids) if assigned_student_ids else True)
            .order_by(Student.admission_number)
        ).all()
        
        if not unassigned_students:
            return {
                "assigned_count": 0,
                "message": "No unassigned students found"
            }
        
        # Calculate available capacity per section
        section_capacities = {}
        for section in sections:
            available = section.max_strength - section.current_strength
            if available > 0:
                section_capacities[section.id] = available
        
        if not section_capacities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All sections are at full capacity"
            )
        
        # Distribute students round-robin
        assignments_created = 0
        section_index = 0
        section_list = list(section_capacities.keys())
        
        for student in unassigned_students:
            # Find next section with capacity
            attempts = 0
            while attempts < len(section_list):
                section_id = section_list[section_index]
                
                if section_capacities[section_id] > 0:
                    # Create assignment
                    assignment = StudentSectionAssignment(
                        student_id=student.id,
                        section_id=section_id,
                        batch_id=batch_id,
                        semester_no=semester_no,
                        assignment_type="AUTO",
                        assigned_by=user_id
                    )
                    session.add(assignment)
                    
                    # Update capacity
                    section_capacities[section_id] -= 1
                    
                    # Update section current_strength
                    section = session.get(Section, section_id)
                    section.current_strength += 1
                    
                    assignments_created += 1
                    
                    # Audit log
                    log_create(
                        session=session,
                        table_name="student_section_assignment",
                        record_id=assignment.id if assignment.id else 0,
                        new_values={
                            "student_id": student.id,
                            "section_id": section_id,
                            "assignment_type": "AUTO"
                        },
                        user_id=user_id
                    )
                    
                    # Move to next section
                    section_index = (section_index + 1) % len(section_list)
                    break
                
                # Try next section
                section_index = (section_index + 1) % len(section_list)
                attempts += 1
            
            if attempts >= len(section_list):
                # No more capacity in any section
                break
        
        session.commit()
        
        return {
            "assigned_count": assignments_created,
            "unassigned_count": len(unassigned_students) - assignments_created,
            "message": f"Successfully assigned {assignments_created} students to sections"
        }
    
    @staticmethod
    def assign_student_to_section_manual(
        session: Session,
        student_id: int,
        section_id: int,
        batch_id: int,
        semester_no: int,
        user_id: int
    ) -> StudentSectionAssignment:
        """
        Manually assign a student to a specific section
        
        Validates:
        - Student exists
        - Section exists and has capacity
        - Student not already assigned to this semester
        """
        # Validate student
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student {student_id} not found"
            )
        
        # Validate section
        section = session.get(Section, section_id)
        if not section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section {section_id} not found"
            )
        
        # Check capacity
        if section.current_strength >= section.max_strength:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {section.code} is at full capacity"
            )
        
        # Check if already assigned
        existing = session.exec(
            select(StudentSectionAssignment)
            .where(StudentSectionAssignment.student_id == student_id)
            .where(StudentSectionAssignment.batch_id == batch_id)
            .where(StudentSectionAssignment.semester_no == semester_no)
            .where(StudentSectionAssignment.is_active == True)
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student already assigned to section {existing.section_id}"
            )
        
        # Create assignment
        assignment = StudentSectionAssignment(
            student_id=student_id,
            section_id=section_id,
            batch_id=batch_id,
            semester_no=semester_no,
            assignment_type="MANUAL",
            assigned_by=user_id
        )
        session.add(assignment)
        
        # Update section strength
        section.current_strength += 1
        
        session.commit()
        session.refresh(assignment)
        
        # Audit log
        log_create(
            session=session,
            table_name="student_section_assignment",
            record_id=assignment.id,
            new_values={
                "student_id": student_id,
                "section_id": section_id,
                "assignment_type": "MANUAL"
            },
            user_id=user_id
        )
        
        return assignment
    
    @staticmethod
    def get_section_roster(
        session: Session,
        section_id: int
    ) -> List[Dict[str, Any]]:
        """Get list of students assigned to a section"""
        assignments = session.exec(
            select(StudentSectionAssignment)
            .where(StudentSectionAssignment.section_id == section_id)
            .where(StudentSectionAssignment.is_active == True)
        ).all()
        
        roster = []
        for assignment in assignments:
            student = session.get(Student, assignment.student_id)
            if student:
                roster.append({
                    "assignment_id": assignment.id,
                    "student_id": student.id,
                    "student_name": student.name,
                    "admission_number": student.admission_number,
                    "assignment_type": assignment.assignment_type,
                    "assigned_at": assignment.assigned_at
                })
        
        return roster
    
    @staticmethod
    def get_unassigned_students(
        session: Session,
        batch_id: int,
        semester_no: int
    ) -> List[Student]:
        # Get students not assigned to any section for this semester
        assigned_student_ids_query = select(StudentSectionAssignment.student_id).where(
            StudentSectionAssignment.batch_id == batch_id,
            StudentSectionAssignment.semester_no == semester_no,
            StudentSectionAssignment.deleted_at.is_(None)
        )
        assigned_student_ids = session.exec(assigned_student_ids_query).all()
        
        # Get unassigned students
        unassigned_students = session.exec(
            select(Student)
            .where(
                Student.batch_id == batch_id,
                Student.id.not_in(assigned_student_ids) if assigned_student_ids else True
            )
            .order_by(Student.registration_number)
        ).all()
        
        return unassigned_students
    
    @staticmethod
    def reassign_student(
        session: Session,
        assignment_id: int,
        new_section_id: int,
        user_id: int
    ) -> StudentSectionAssignment:
        """Reassign student to a different section"""
        # Get existing assignment
        assignment = session.get(StudentSectionAssignment, assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assignment {assignment_id} not found"
            )
        
        old_section_id = assignment.section_id
        
        # Validate new section
        new_section = session.get(Section, new_section_id)
        if not new_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section {new_section_id} not found"
            )
        
        # Check capacity
        if new_section.current_strength >= new_section.max_strength:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section {new_section.code} is at full capacity"
            )
        
        # Update old section strength
        old_section = session.get(Section, old_section_id)
        old_section.current_strength -= 1
        
        # Update new section strength
        new_section.current_strength += 1
        
        # Update assignment
        assignment.section_id = new_section_id
        assignment.assignment_type = "MANUAL"  # Reassignment is manual
        assignment.assigned_by = user_id
        
        session.commit()
        session.refresh(assignment)
        
        return assignment
    
    @staticmethod
    def delete_assignment(
        session: Session,
        assignment_id: int,
        user_id: int
    ) -> None:
        """Delete a student section assignment"""
        assignment = session.get(StudentSectionAssignment, assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assignment {assignment_id} not found"
            )
        
        # Update section strength
        section = session.get(Section, assignment.section_id)
        section.current_strength -= 1
        
        # Soft delete
        assignment.is_active = False
        
        session.commit()
        
        # Audit log
        log_delete(
            session=session,
            table_name="student_section_assignment",
            record_id=assignment_id,
            old_values={
                "student_id": assignment.student_id,
                "section_id": assignment.section_id
            },
            user_id=user_id
        )
