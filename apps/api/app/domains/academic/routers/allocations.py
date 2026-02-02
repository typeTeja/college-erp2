from typing import List, Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db.session import get_session
from app.api import deps
from app.models.user import User
from app.domains.academic.models import StudentPracticalBatchAllocation, PracticalBatch
from app.models.student import Student

router = APIRouter()

# --- Schemas ---
class AllocationCreate(BaseModel):
    student_ids: List[int]
    practical_batch_id: int
    subject_id: int
    batch_semester_id: int

class AllocationResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    admission_number: str
    practical_batch_id: int
    subject_id: int

# --- Endpoints ---

@router.get("/batch/{practical_batch_id}", response_model=List[AllocationResponse])
def get_batch_allocations(
    practical_batch_id: int,
    subject_id: Optional[int] = None, # Optional filter
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all students allocated to a specific practical batch.
    Optionally filter by subject_id.
    """
    query = select(StudentPracticalBatchAllocation, Student)\
        .join(Student, StudentPracticalBatchAllocation.student_id == Student.id)\
        .where(StudentPracticalBatchAllocation.practical_batch_id == practical_batch_id)
    
    if subject_id:
        query = query.where(StudentPracticalBatchAllocation.subject_id == subject_id)
        
    results = session.exec(query).all()
    
    return [
        AllocationResponse(
            id=allocation.id,
            student_id=allocation.student_id,
            student_name=student.name,
            admission_number=student.admission_number,
            practical_batch_id=allocation.practical_batch_id,
            subject_id=allocation.subject_id
        )
        for allocation, student in results
    ]

@router.post("/bulk", response_model=Dict[str, int])
def bulk_allocate_students(
    data: AllocationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Bulk allocate students to a practical batch for a subject.
    Checks capacity and ignores duplicates.
    """
    # Verify Batch Exists
    batch = session.get(PracticalBatch, data.practical_batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Practical Batch not found")
        
    # Check Capacity
    current_count = session.exec(
        select(StudentPracticalBatchAllocation)
        .where(StudentPracticalBatchAllocation.practical_batch_id == data.practical_batch_id)
    ).all()
    
    # Just a simple count. Note: Capacity is usually per batch, regardless of subject? 
    # Or is it per subject? Typically a "Batch" is a physical group. 
    # If multiple subjects share the same "PracticalBatch" ID, they share the capacity.
    # The new schema links Allocation to (Student, Subject, BatchSemester). 
    # Wait, the `StudentPracticalBatchAllocation` has `practical_batch_id`.
    # `PracticalBatch` has `max_strength`.
    # So we should count explicit allocations to this batch ID.
    
    if len(current_count) + len(data.student_ids) > batch.max_strength:
        raise HTTPException(
            status_code=400, 
            detail=f"Batch capacity exceeded. Max: {batch.max_strength}, Current: {len(current_count)}, Attempting: {len(data.student_ids)}"
        )
        
    created_count = 0
    errors = []
    
    for student_id in data.student_ids:
        # Check if already allocated to THIS subject in THIS semester?
        # The unique constraint is (student_id, subject_id, batch_semester_id).
        # We should check if student is already allocated to ANY batch for this subject/semester.
        existing = session.exec(
            select(StudentPracticalBatchAllocation).where(
                StudentPracticalBatchAllocation.student_id == student_id,
                StudentPracticalBatchAllocation.subject_id == data.subject_id,
                StudentPracticalBatchAllocation.batch_semester_id == data.batch_semester_id
            )
        ).first()
        
        if existing:
            # If already assigned to THIS batch, skip.
            if existing.practical_batch_id == data.practical_batch_id:
                continue
            # If assigned to ANOTHER batch, we might want to overwrite or error? 
            # For now, let's error or skip. User should de-allocate first.
            # actually, maybe update?
            # Let's update it to move them.
            existing.practical_batch_id = data.practical_batch_id
            session.add(existing)
            created_count += 1 # Counted as handled
        else:
            # Create new
            alloc = StudentPracticalBatchAllocation(
                student_id=student_id,
                practical_batch_id=data.practical_batch_id,
                subject_id=data.subject_id,
                batch_semester_id=data.batch_semester_id
            )
            session.add(alloc)
            created_count += 1
            
    session.commit()
    
    # Update local batch strength cache?
    # PracticalBatch has `current_strength` field. We should update it.
    # But checking strictly, `current_strength` might be complex if it's per subject.
    # However, `PracticalBatch` represents a slot.
    # We will re-calculate total unique students in this batch.
    
    unique_students = session.exec(
        select(StudentPracticalBatchAllocation.student_id)
        .where(StudentPracticalBatchAllocation.practical_batch_id == data.practical_batch_id)
        .distinct()
    ).all()
    
    batch.current_strength = len(unique_students)
    session.add(batch)
    session.commit()
    
    return {"allocated": created_count, "capacity_remaining": batch.max_strength - batch.current_strength}

@router.delete("/{student_id}/{subject_id}", status_code=200)
def remove_allocation(
    student_id: int,
    subject_id: int,
    practical_batch_id: Optional[int] = None, # Optional verification
    session: Session = Depends(get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Remove a student from a practical batch for a subject.
    """
    query = select(StudentPracticalBatchAllocation).where(
        StudentPracticalBatchAllocation.student_id == student_id,
        StudentPracticalBatchAllocation.subject_id == subject_id
    )
    
    if practical_batch_id:
        query = query.where(StudentPracticalBatchAllocation.practical_batch_id == practical_batch_id)
        
    allocation = session.exec(query).first()
    
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
        
    p_batch_id = allocation.practical_batch_id
    session.delete(allocation)
    session.commit()
    
    # Update strength
    batch = session.get(PracticalBatch, p_batch_id)
    if batch:
        unique_students = session.exec(
            select(StudentPracticalBatchAllocation.student_id)
            .where(StudentPracticalBatchAllocation.practical_batch_id == p_batch_id)
            .distinct()
        ).all()
        batch.current_strength = len(unique_students)
        session.add(batch)
        session.commit()
        
    return {"message": "Allocation removed"}
