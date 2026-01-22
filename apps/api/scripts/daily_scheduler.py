"""
Daily Scheduler Script
To be run via cron or scheduled task once per day (e.g., at 00:01 AM).

Purpose:
1. Check for Academic Batches where a new Semester starts TODAY.
2. Automatically promote students to the new semester.
3. Update specific flags (is_active) for BatchSemesters.

Usage:
    python3 scripts/daily_scheduler.py
"""
import sys
import os
from datetime import date
from sqlmodel import Session, select, func

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from app.db.session import engine
from app.models.academic.batch import AcademicBatch, BatchSemester
from app.models.student import Student, StudentStatus
from app.models.academic.student_history import StudentPromotionLog

def run_daily_jobs():
    print(f"[{date.today()}] Starting Daily Jobs...")
    
    with Session(engine) as session:
        # Job 1: Semester Auto-Promotion
        run_semester_promotion(session)
        
    print(f"[{date.today()}] Daily Jobs Completed.")

def run_semester_promotion(session: Session):
    """
    Check if any BatchSemester starts today. 
    If yes, activate it and promote students.
    """
    today = date.today()
    print(f"Checking for semesters starting on {today}...")

    # Find semesters starting today
    stmt = select(BatchSemester).where(BatchSemester.start_date == today)
    semesters_starting_today = session.exec(stmt).all()
    
    if not semesters_starting_today:
        print("No semesters scheduled to start today.")
        return

    for new_semester in semesters_starting_today:
        batch_id = new_semester.batch_id
        semester_name = new_semester.semester_name
        batch_name = new_semester.batch.batch_code if new_semester.batch else f"Batch #{batch_id}"
        
        print(f"\nProcessing Promotion for {batch_name} -> {semester_name}")
        
        # 1. Deactivate old active semesters for this batch
        active_semesters = session.exec(
            select(BatchSemester)
            .where(BatchSemester.batch_id == batch_id)
            .where(BatchSemester.is_active == True)
        ).all()
        
        for sem in active_semesters:
            if sem.id != new_semester.id:
                sem.is_active = False
                session.add(sem)
        
        # 2. Activate new semester
        new_semester.is_active = True
        session.add(new_semester)
        
        # 3. Promote Students
        # Get all ACTIVE students in this batch
        students = session.exec(
            select(Student)
            .where(Student.batch_id == batch_id)
            .where(Student.status == StudentStatus.ACTIVE)
        ).all()
        
        promoted_count = 0
        for student in students:
            # Skip if already in this semester (idempotency)
            if student.batch_semester_id == new_semester.id:
                continue
                
            old_semester_id = student.batch_semester_id
            
            # Update student
            student.batch_semester_id = new_semester.id
            student.program_year_id = new_semester.program_year_id
            session.add(student)
            
            # Log Promotion
            log = StudentPromotionLog(
                student_id=student.id,
                from_batch_semester_id=old_semester_id,
                to_batch_semester_id=new_semester.id,
                promotion_date=today,
                remarks="Auto-promotion by System Scheduler",
                is_automatic=True
            )
            session.add(log)
            promoted_count += 1
            
        print(f"  - Deactivated {len(active_semesters)} old semesters")
        print(f"  - Activated {semester_name}")
        print(f"  - Promoted {promoted_count} students")
        
    try:
        session.commit()
        print("\nAll changes committed successfully.")
    except Exception as e:
        session.rollback()
        print(f"Error committing changes: {str(e)}")

if __name__ == "__main__":
    run_daily_jobs()
