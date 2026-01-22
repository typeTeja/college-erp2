import sys
import os
from datetime import date, time

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select, create_engine
from app.db.session import engine
from app.models.academic.batch import AcademicBatch, BatchSemester, ProgramYear
from app.models.master_data import PracticalBatch, Section, SubjectType
from app.models.academic.allocation import StudentPracticalBatchAllocation
from app.models.attendance import AttendanceSession, SessionStatus
from app.models.timetable import ClassSchedule, TimeSlot, DayOfWeek, SlotType
from app.models.student import Student
from app.models.subject import Subject
from app.models.program import Program
from app.models.academic.regulation import Regulation

from app.models.department import Department

def verify_refactor():
    with Session(engine) as session:
        print("🚀 Starting Verification of Academic Structure Refactor...")

        # 1. Setup minimal data
        
        # Create Department
        dept = Department(name="Test Dept", code="TD001", description="Test Department")
        session.add(dept)
        session.flush()

        # Create Dummy Program & Regulation
        program = Program(name="Test B.Tech", code="TEST_BTECH", duration_years=4, department_id=dept.id)
        session.add(program)
        session.flush()
        
        regulation = Regulation(program_id=program.id, regulation_code="R24", regulation_name="Test Regulation", year=2024)
        session.add(regulation)
        session.flush()
        
        # Create Batch
        batch = AcademicBatch(
            batch_code="TEST-2024-2028", 
            batch_name="Test Batch", 
            program_id=program.id, 
            regulation_id=regulation.id,
            joining_year=2024, start_year=2024, end_year=2028
        )
        session.add(batch)
        session.flush()
        
        # Create Program Year
        p_year = ProgramYear(batch_id=batch.id, year_no=1, year_name="1st Year")
        session.add(p_year)
        session.flush()
        
        # Create Batch Semester
        b_sem = BatchSemester(
            batch_id=batch.id, program_year_id=p_year.id, 
            year_no=1, semester_no=1, semester_name="Sem 1"
        )
        session.add(b_sem)
        session.flush()
        
        # Create Subject (Practical)
        subject = Subject(name="Test Lab", code="LAB101", credits=2)
        session.add(subject)
        session.flush()
        
        print("\n✅ Step 1: Base Academic Structure Created")

        # 2. Create Practical Batch (Sibling to Section)
        # Note: We don't even create a Section here to prove independence!
        lab_batch = PracticalBatch(
            name="Test Lab Batch A1",
            code="TL-A1",
            batch_semester_id=b_sem.id, # Direct link to semester
            max_strength=20
        )
        session.add(lab_batch)
        session.flush()
        
        if lab_batch.batch_semester_id == b_sem.id:
            print(f"✅ Step 2: PracticalBatch created linked to Semester ID {b_sem.id}")
        else:
            print("❌ Step 2 Failed: PracticalBatch not linked to Semester")

        # 3. Create Student & Allocation
        student = Student(
            name="John Doe", 
            admission_number="TEST001", 
            email="john@test.com",
            program_id=program.id,
            batch_id=batch.id,
            program_year_id=p_year.id,
            batch_semester_id=b_sem.id
        )
        session.add(student)
        session.flush()
        
        allocation = StudentPracticalBatchAllocation(
            student_id=student.id,
            practical_batch_id=lab_batch.id,
            batch_semester_id=b_sem.id,
            subject_id=subject.id
        )
        session.add(allocation)
        session.flush()
        
        print(f"✅ Step 3: Student {student.name} allocated to Lab Batch {lab_batch.code}")
        
        # 4. Create Attendance Session
        # Crucial: Passing practical_batch_id, NO section
        attendance = AttendanceSession(
            subject_id=subject.id,
            faculty_id=1, # Dummy ID, assuming foreign key check might fail if not present. Warning.
            # Let's hope FK constraints aren't strict for this test or we need a dummy faculty.
            # Creating dummy faculty just in case
            program_id=program.id,
            program_year_id=p_year.id,
            semester=1,
            # section=None, # Explicitly None
            practical_batch_id=lab_batch.id,
            session_date=date.today(),
            start_time=time(9, 0),
            end_time=time(10, 0),
            status=SessionStatus.SCHEDULED
        )
        
        # Note: Faculty FK might fail. Let's try inserting. If it fails, we know schema is checking.
        # Ideally we mock faculty too.
        
        try:
            # We need a faculty if FK exists
            from app.models.faculty import Faculty
            faculty = Faculty(
                name="Prof Test", 
                employee_id="EMP001", # Note: employee_id is not in model above? CHECK below
                email="prof@test.com", 
                designation="Professor", 
                department="Computer Science"
            )
            session.add(faculty)
            session.flush()
            attendance.faculty_id = faculty.id
            
            session.add(attendance)
            session.flush()
            print(f"✅ Step 4: Attendance Session created for Practical Batch {attendance.practical_batch_id}")
        except Exception as e:
            print(f"❌ Step 4 Failed: {str(e)}")

        # 5. Create Timetable Entry (ClassSchedule)
        # Crucial: Passing practical_batch_id, NO section
        try:
            # Need TimeSlot
            slot = TimeSlot(name="Lab Slot", start_time=time(9,0), end_time=time(11,0), type=SlotType.PRACTICAL)
            session.add(slot)
            session.flush()
            
            schedule = ClassSchedule(
                academic_year_id=1, # Dummy
                batch_semester_id=b_sem.id,
                # section_id=None,
                practical_batch_id=lab_batch.id,
                day_of_week=DayOfWeek.MONDAY,
                period_id=slot.id,
                subject_id=subject.id,
                faculty_id=faculty.id
            )
            session.add(schedule)
            session.flush()
            print(f"✅ Step 5: Timetable Entry created for Practical Batch {schedule.practical_batch_id}")
            
        except Exception as e:
            print(f"❌ Step 5 Failed: {str(e)}")

        # Rollback to clean up
        session.rollback()
        print("\n✨ Verification Complete (Rolled back changes)")

if __name__ == "__main__":
    try:
        verify_refactor()
    except Exception as e:
        print(f"CRITICAL FAILURE: {str(e)}")
