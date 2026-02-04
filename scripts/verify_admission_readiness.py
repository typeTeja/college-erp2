
import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "apps" / "api"))

from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / "apps" / "api" / ".env"
load_dotenv(env_path)

from sqlmodel import Session, select
from app.db.session import engine
from app.domains.academic.models import Program, AcademicBatch
from app.domains.admission.models import AdmissionSettings
from datetime import datetime

async def verify_readiness():
    print("--- Verifying Admission Readiness ---")
    try:
        with Session(engine) as session:
            # Check Admission Settings
            settings = session.exec(select(AdmissionSettings)).first()
            if not settings:
                print("[X] Admission Settings: MISSING (Will be auto-created on access)")
            else:
                print(f"[OK] Admission Settings found. Application Fee: {settings.application_fee_amount}")

            # Check Programs
            programs = session.exec(select(Program)).all()
            if not programs:
                print("[X] Programs: NONE FOUND. Admission cannot proceed.")
            else:
                print(f"[OK] Programs found: {len(programs)}")
                for p in programs:
                    print(f" - {p.name} (ID: {p.id})")

            # Check Batches for Current Year
            current_year = datetime.now().year
            from app.domains.academic.models import AcademicYear
            ac_year = session.exec(select(AcademicYear).where(AcademicYear.name.like(f"{current_year}%"))).first()
            if not ac_year:
                 print(f"[X] Academic Year {current_year}: NOT FOUND")
            else:
                batches = session.exec(select(AcademicBatch).where(AcademicBatch.admission_year_id == ac_year.id)).all()
                if not batches:
                    print(f"[X] Academic Batches for {current_year}: NONE FOUND.")
                    print("    AdmissionService.confirm_admission will FAIL.")
                    print("    Action: Create an AcademicBatch for the program.")
                else:
                    print(f"[OK] Academic Batches for {current_year}: Found {len(batches)}")
                    for b in batches:
                        print(f" - {b.name} (Program ID: {b.program_id})")

    except Exception as e:
        print(f"Error during verification: {e}")

if __name__ == "__main__":
    asyncio.run(verify_readiness())
