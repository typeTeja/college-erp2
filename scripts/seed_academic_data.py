
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
from app.domains.academic.models import Program, AcademicBatch, Regulation, AcademicYear
from app.domains.admission.models import AdmissionSettings
from datetime import datetime

async def seed_data():
    print("--- Seeding Academic Data ---")
    try:
        with Session(engine) as session:
            current_year = datetime.now().year
            
            # 1. Create Academic Year
            academic_year = session.exec(select(AcademicYear).where(AcademicYear.name == f"{current_year}-{current_year+1}")).first()
            if not academic_year:
               print(f"Creating Academic Year: {current_year}-{current_year+1}")
               academic_year = AcademicYear(
                   name=f"{current_year}-{current_year+1}",
                   start_date=datetime(current_year, 6, 1),
                   end_date=datetime(current_year+1, 5, 31),
                   is_active=True
               )
               session.add(academic_year)
               session.commit()
               session.refresh(academic_year)

            # 2. Create Program
            program = session.exec(select(Program).where(Program.code == "BTECH-CSE")).first()
            if not program:
                print("Creating Program: B.Tech CSE")
                program = Program(
                    name="B.Tech Computer Science",
                    code="BTECH-CSE",
                    program_type="UG",
                    duration_years=4,
                    description="Bachelor of Technology in Computer Science",
                    is_active=True
                )
                session.add(program)
                session.commit()
                session.refresh(program)

            # 3. Create Regulation
            regulation = session.exec(select(Regulation).where(Regulation.name == "R24")).first()
            if not regulation:
               print("Creating Regulation: R24")
               regulation = Regulation(
                   name="R24",
                   code="R24",
                   program_id=program.id,
                   start_year=current_year,
                   total_credits=160,
                   duration_years=4,
                   description="Regulation 2024",
                   is_active=True
               )
               session.add(regulation)
               session.commit()
               session.refresh(regulation)

            # 4. Create Academic Batch
            batch_name = f"CSE-{current_year}"
            batch = session.exec(select(AcademicBatch).where(AcademicBatch.name == batch_name)).first()
            
            if not batch:
                print(f"Creating Academic Batch for {current_year}")
                batch = AcademicBatch(
                    name=batch_name,
                    admission_year_id=academic_year.id,
                    program_id=program.id,
                    regulation_id=regulation.id,
                    current_year=1,
                    current_semester=1,
                    status="ACTIVE",
                    is_active=True
                )
                session.add(batch)
                session.commit()
                session.refresh(batch)
            else:
                print(f"Academic Batch for {current_year} already exists.")

            # 3. Admission Settings
            settings = session.exec(select(AdmissionSettings)).first()
            if not settings:
                print("Creating Admission Settings")
                settings = AdmissionSettings(
                    admission_year=current_year,
                    application_fee_enabled=True,
                    application_fee_amount=500.0,
                    auto_create_student_account=True
                )
                session.add(settings)
                session.commit()
            else:
                settings.auto_create_student_account = True
                session.add(settings)
                session.commit()
                print("Admission Settings updated to enable auto-create student.")

            print("--- Seeding Completed Successfully ---")

    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(seed_data())
