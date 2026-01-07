from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from app.models.program import Program, ProgramType, ProgramStatus
from app.models.department import Department
from app.schemas.program import ProgramCreate

class ProgramService:
    @staticmethod
    def create_program(session: Session, program_in: ProgramCreate) -> Program:
        """Create a new program"""
        
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
        
        # RELOAD with department for response schema
        return session.exec(
            select(Program).where(Program.id == program.id).options(selectinload(Program.department))
        ).one()

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
