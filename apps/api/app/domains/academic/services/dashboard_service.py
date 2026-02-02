"""
Academic Dashboard Service
Aggregates academic structure data for dashboard view
"""
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.domains.academic.models import (
    AcademicBatch, ProgramYear, BatchSemester,
    Section, PracticalBatch, Regulation
)
from app.models.program import Program
from app.models.faculty import Faculty
from app.schemas.dashboard import (
    AcademicDashboardResponse,
    DashboardBatch,
    DashboardYear,
    DashboardSemester,
    DashboardSection,
    DashboardLabGroup
)


class AcademicDashboardService:
    """Service for academic dashboard operations"""
    
    @staticmethod
    def get_dashboard_data(
        session: Session,
        program_id: Optional[int] = None,
        batch_id: Optional[int] = None
    ) -> AcademicDashboardResponse:
        """
        Get complete academic dashboard data
        
        Args:
            session: Database session
            program_id: Optional filter by program
            batch_id: Optional filter by specific batch
            
        Returns:
            AcademicDashboardResponse with complete hierarchy
        """
        # Build query for batches
        query = select(AcademicBatch).options(
            selectinload(AcademicBatch.program),
            selectinload(AcademicBatch.regulation)
        )
        
        if program_id:
            query = query.where(AcademicBatch.program_id == program_id)
        if batch_id:
            query = query.where(AcademicBatch.id == batch_id)
        
        query = query.where(AcademicBatch.is_active == True)
        query = query.order_by(AcademicBatch.joining_year.desc())
        
        batches = session.exec(query).all()
        
        # Build dashboard batches
        dashboard_batches = []
        total_students = 0
        total_capacity = 0
        total_sections = 0
        total_labs = 0
        
        for batch in batches:
            dashboard_batch = AcademicDashboardService._build_batch_hierarchy(
                session, batch
            )
            dashboard_batches.append(dashboard_batch)
            
            total_students += dashboard_batch.total_students
            total_capacity += dashboard_batch.total_capacity
            
            # Count sections and labs
            for year in dashboard_batch.years:
                for semester in year.semesters:
                    total_sections += len(semester.sections)
                    total_labs += len(semester.lab_groups)
        
        # Build summary
        summary = {
            "total_batches": len(dashboard_batches),
            "total_students": total_students,
            "total_capacity": total_capacity,
            "total_sections": total_sections,
            "total_labs": total_labs,
            "overall_utilization": round(
                (total_students / total_capacity * 100) if total_capacity > 0 else 0,
                2
            )
        }
        
        return AcademicDashboardResponse(
            batches=dashboard_batches,
            summary=summary
        )
    
    @staticmethod
    def _build_batch_hierarchy(
        session: Session,
        batch: AcademicBatch
    ) -> DashboardBatch:
        """Build complete hierarchy for a batch"""
        
        # Get program years
        program_years = session.exec(
            select(ProgramYear)
            .where(ProgramYear.batch_id == batch.id)
            .order_by(ProgramYear.year_no)
        ).all()
        
        dashboard_years = []
        batch_total_students = 0
        batch_total_capacity = 0
        
        for program_year in program_years:
            # Get semesters for this year
            semesters = session.exec(
                select(BatchSemester)
                .where(BatchSemester.batch_id == batch.id)
                .where(BatchSemester.program_year_id == program_year.id)
                .order_by(BatchSemester.semester_no)
            ).all()
            
            dashboard_semesters = []
            year_total_students = 0
            year_total_capacity = 0
            
            for semester in semesters:
                # Get sections for this semester
                sections = session.exec(
                    select(Section)
                    .where(Section.batch_semester_id == semester.id)
                    .where(Section.is_active == True)
                    .order_by(Section.code)
                ).all()
                
                dashboard_sections = []
                semester_total_students = 0
                semester_total_capacity = 0
                
                # 1. Process Sections
                for section in sections:
                    # Get faculty name if assigned
                    faculty_name = None
                    if section.faculty_id:
                        faculty = session.get(Faculty, section.faculty_id)
                        if faculty:
                            faculty_name = faculty.name
                    
                    dashboard_sections.append(
                        DashboardSection(
                            id=section.id,
                            name=section.name,
                            code=section.code,
                            max_strength=section.max_strength,
                            current_strength=section.current_strength,
                            utilization_percentage=round(
                                (section.current_strength / section.max_strength * 100)
                                if section.max_strength > 0 else 0,
                                2
                            ),
                            faculty_id=section.faculty_id,
                            faculty_name=faculty_name
                        )
                    )
                    
                    semester_total_students += section.current_strength
                    semester_total_capacity += section.max_strength

                # 2. Process Lab Groups (Independent of Sections)
                lab_groups = session.exec(
                    select(PracticalBatch)
                    .where(PracticalBatch.batch_semester_id == semester.id)
                    .where(PracticalBatch.is_active == True)
                    .order_by(PracticalBatch.code)
                ).all()

                dashboard_labs = [
                    DashboardLabGroup(
                        id=lab.id,
                        name=lab.name,
                        code=lab.code,
                        max_strength=lab.max_strength,
                        current_strength=lab.current_strength,
                        utilization_percentage=round(
                            (lab.current_strength / lab.max_strength * 100)
                            if lab.max_strength > 0 else 0,
                            2
                        )
                    )
                    for lab in lab_groups
                ]

                # Note: Lab students are subsets of Section students usually, 
                # so we don't add lab capacity/strength to semester total to avoid double counting.
                
                dashboard_semesters.append(
                    DashboardSemester(
                        id=semester.id,
                        semester_no=semester.semester_no,
                        semester_name=semester.semester_name,
                        total_credits=semester.total_credits,
                        sections=dashboard_sections,
                        lab_groups=dashboard_labs,
                        total_students=semester_total_students,
                        total_capacity=semester_total_capacity
                    )
                )
                
                # Students progress through semesters, so year capacity is the max semester capacity
                # not the sum (same students move from Sem 1 to Sem 2)
                year_total_students += semester_total_students
                year_total_capacity = max(year_total_capacity, semester_total_capacity)
            
            dashboard_years.append(
                DashboardYear(
                    id=program_year.id,
                    year_no=program_year.year_no,
                    year_name=program_year.year_name,
                    semesters=dashboard_semesters,
                    total_students=year_total_students,
                    total_capacity=year_total_capacity
                )
            )
            
            # Batch capacity is the sum of year capacities (different cohorts per year)
            batch_total_students += year_total_students
            batch_total_capacity += year_total_capacity
        
        return DashboardBatch(
            id=batch.id,
            batch_code=batch.batch_code,
            batch_name=batch.batch_name,
            program_name=batch.program.name if batch.program else "Unknown",
            regulation_name=batch.regulation.regulation_name if batch.regulation else "Unknown",
            status=batch.status,
            years=dashboard_years,
            total_students=batch_total_students,
            total_capacity=batch_total_capacity,
            overall_utilization=round(
                (batch_total_students / batch_total_capacity * 100)
                if batch_total_capacity > 0 else 0,
                2
            )
        )
