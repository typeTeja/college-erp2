import sys
import os
from datetime import date

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.program import Program
from app.models.academic.regulation import Regulation, RegulationSemester
from app.models.master_data import PracticalBatch, Section
from app.models.department import Department
from app.services.bulk_setup_service import BulkBatchSetupService
from app.schemas.bulk_setup import BulkBatchSetupRequest

def test_bulk_setup():
    with Session(engine) as session:
        print("🚀 Starting Bulk Setup Verification...")

        import random
        suffix = random.randint(1000, 9999)

        # 1. Setup Master Data
        # Create Department
        dept = Department(name=f"Bulk Test Dept {suffix}", code=f"BTD{suffix}", description="Test Dept")
        session.add(dept)
        session.flush()

        # Create Program
        program = Program(name=f"Bulk Test Prog {suffix}", code=f"BTP_{suffix}", duration_years=4, department_id=dept.id)
        session.add(program)
        session.flush()
        
        
        # Create Regulation with Semesters
        reg = Regulation(program_id=program.id, regulation_code=f"R_BULK_{suffix}", regulation_name="Bulk Reg", year=2024)
        session.add(reg)
        session.flush()
        
        # Create semesters for regulation (mock just 2 sem)
        s1 = RegulationSemester(regulation_id=reg.id, program_year=1, semester_no=1, semester_name="Sem 1", total_credits=20)
        s2 = RegulationSemester(regulation_id=reg.id, program_year=1, semester_no=2, semester_name="Sem 2", total_credits=20)
        session.add(s1)
        session.add(s2)
        session.flush()

        # 2. Execute Bulk Setup
        # Use a future year + suffix to avoid collision if code is global unique
        start_year = 2025 + (suffix % 100)
        request = BulkBatchSetupRequest(
            program_id=program.id,
            regulation_id=reg.id,
            joining_year=start_year,
            sections_per_semester=2, # A, B
            section_capacity=60,
            labs_per_section=3,      # Should result in 2 * 3 = 6 labs per semester
            lab_capacity=20,
            batch_name_override=f"Test Bulk Batch {suffix}"
        )
        
        user_id = 1 # Dummy
        
        try:
            response = BulkBatchSetupService.create_bulk_batch(session, request, user_id)
            print(f"✅ Bulk Setup executed. Batch ID: {response.batch_id}")
            print(f"   Created Stats: Sections={response.sections_created}, Labs={response.labs_created}")
            
            # 3. Verify Lab Batches Structure
            # Check labs for Semester 1 of this batch
            
            # Fetch batch semesters
            from app.models.academic.batch import BatchSemester
            sem1 = session.exec(select(BatchSemester).where(
                BatchSemester.batch_id == response.batch_id, 
                BatchSemester.semester_no == 1
            )).first()
            
            if not sem1:
                print("❌ Failed: Semsester 1 not found")
                return

            labs = session.exec(select(PracticalBatch).where(PracticalBatch.batch_semester_id == sem1.id)).all()
            sections = session.exec(select(Section).where(Section.batch_semester_id == sem1.id)).all()
            
            print(f"\n   Semester 1 Check:")
            print(f"   - Sections Found: {len(sections)} (Expected 2)")
            print(f"   - Labs Found: {len(labs)} (Expected 6)")
            
            # Check linkage
            all_linked_to_semester = all(l.batch_semester_id == sem1.id for l in labs)
            # Check NO linkage to section (should fail schema check if we tried query, but good to know logic works)
            
            if len(labs) == 6 and all_linked_to_semester:
                print("✅ SUCCESS: 6 Labs created and linked directly to Semester 1")
            else:
                print(f"❌ FAILURE: Expected 6 labs linked to semester, found {len(labs)}")
            
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            import traceback
            traceback.print_exc()

        session.rollback()
        print("\n✨ Test Complete (Rolled back)")

if __name__ == "__main__":
    test_bulk_setup()
