from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from app.models.program import Program, ProgramType, ProgramStatus
from app.models.program_year import LegacyProgramYear
from app.models.semester import Semester
from app.models.department import Department
from app.schemas.program import ProgramCreate

class ProgramService:
    @staticmethod
    def create_program(session: Session, program_in: ProgramCreate) -> Program:
        """Create a new program and auto-generate its structure"""
        
        # Check for existing code
        existing = session.exec(select(Program).where(Program.code == program_in.code)).first()
        if existing:
            raise HTTPException(status_code=400, detail="Program with this code already exists")
            
        # Create Program
        program_data = program_in.dict()
        program = Program(**program_data)
        session.add(program)
        session.commit()
        session.refresh(program)
        
        # Generate Structure (Years and Semesters)
        ProgramService.generate_structure(session, program)
        
        # Reload with department for response schema
        return session.exec(
            select(Program).where(Program.id == program.id).options(selectinload(Program.department))
        ).one()

    @staticmethod
    def generate_structure(session: Session, program: Program) -> None:
        """Generate Years and Semesters based on duration"""
        
        total_years = program.duration_years
        
        # Handle 18-month programs (1.5 years) -> 2 years structure but only 3 semesters
        # Or standard logic: 1 year = 2 semesters
        
        semesters_count = 0
        
        for year_num in range(1, total_years + 1):
            # Create Year
            year_name = f"Year {year_num}"
            program_year = LegacyProgramYear(
                program_id=program.id,
                year_number=year_num,
                name=year_name,
                is_active=True
            )
            session.add(program_year)
            session.commit()
            session.refresh(program_year)
            
            # Create 2 Semesters per year (Standard)
            # Custom logic can be applied later via update API
            for sem_num_in_year in [1, 2]:
                semesters_count += 1
                sem_name = f"Semester {semesters_count}"
                
                # Default Logic: Odd/Even
                # For 1.5 year programs (e.g. Diploma), we might want to disable 4th sem later
                
                semester = Semester(
                    program_year_id=program_year.id,
                    semester_number=sem_num_in_year,
                    name=sem_name,
                    is_internship=False,
                    is_project_semester=False
                )
                session.add(semester)
            
        session.commit()

    @staticmethod
    def get_program(session: Session, program_id: int) -> Optional[Program]:
        return session.exec(
            select(Program).where(Program.id == program_id).options(selectinload(Program.department))
        ).first()

    @staticmethod
    def get_programs(session: Session, skip: int = 0, limit: int = 100, 
                     type: Optional[ProgramType] = None, 
                     status: Optional[ProgramStatus] = None) -> List[Program]:
        query = select(Program).options(selectinload(Program.department))
        if type:
            query = query.where(Program.program_type == type)
        if status:
            query = query.where(Program.status == status)
            
        # Default Filter: Don't show Archived unless requested? 
        # For now, show all
        
        return session.exec(query.offset(skip).limit(limit)).all()
        
    @staticmethod
    def update_structure(session: Session, program_id: int, structure_data: Dict[str, Any]) -> Program:
        """
        Complex update for renaming semesters, setting flags like internship, etc.
        Expecting JSON structure like:
        {
            "years": [
                {
                    "id": 1, 
                    "semesters": [
                        {"id": 10, "name": "Foundational Sem", "is_internship": false},
                        {"id": 11, "name": "Internship Phase", "is_internship": true}
                    ]
                }
            ]
        }
        """
        program = session.get(Program, program_id)
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
            
        # Iterate and update
        # This is a simplified version, robust implementation would validate IDs belong to program
        for year_data in structure_data.get("years", []):
            year_id = year_data.get("id")
            for sem_data in year_data.get("semesters", []):
                sem_id = sem_data.get("id")
                semester = session.get(Semester, sem_id)
                if semester and semester.program_year.program_id == program_id:
                    if "name" in sem_data:
                        semester.name = sem_data["name"]
                    if "is_internship" in sem_data:
                        semester.is_internship = sem_data["is_internship"]
                    if "is_project_semester" in sem_data:
                        semester.is_project_semester = sem_data["is_project_semester"]
                    session.add(semester)
        
        session.commit()
        session.commit()
        # Reload with department for response schema
        return session.exec(
            select(Program).where(Program.id == program_id).options(selectinload(Program.department))
        ).one()

    @staticmethod
    def delete_program(session: Session, program_id: int) -> bool:
        program = session.get(Program, program_id)
        if not program:
            raise HTTPException(status_code=404, detail="Program not found")
            
        # Check dependencies (Students)
        if len(program.students) > 0:
             raise HTTPException(status_code=400, detail="Cannot delete program with enrolled students.")
             
        session.delete(program)
        session.commit()
        return True
