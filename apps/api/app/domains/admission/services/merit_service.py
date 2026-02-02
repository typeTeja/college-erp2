"""
Merit and Scholarship Service
Handles scholarship slab determination and merit-based fee calculations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlmodel import Session, select
from ..models import (
    ScholarshipCalculation, 
    TentativeAdmission, 
    Application,
    TentativeAdmissionStatus
)
from app.domains.finance.models import ScholarshipSlab

class MeritService:
    @staticmethod
    def calculate_scholarship(
        session: Session, 
        application_id: int, 
        calculated_by: int,
        entrance_weightage: float = 0.5,
        prev_weightage: float = 0.5
    ) -> ScholarshipCalculation:
        """
        Calculates merit score and determines scholarship slab.
        """
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")

        # Logic for merit calculation
        # 1. Get entrance marks (EntranceExamResult)
        # 2. Get previous marks (Application.previous_marks_percentage)
        # 3. Apply weights
        # 4. Find matching ScholarshipSlab
        
        calc = ScholarshipCalculation(
            application_id=application_id,
            student_name=application.name,
            course=application.program.name if application.program else "Unknown",
            calculated_by=calculated_by,
            calculation_date=datetime.utcnow()
        )
        
        # Placeholder logic
        calc.is_calculated = True
        session.add(calc)
        session.commit()
        session.refresh(calc)
        return calc

    @staticmethod
    def generate_tentative_admission(
        session: Session,
        application_id: int,
        base_fee: float
    ) -> TentativeAdmission:
        """
        Generates tentative admission structure based on scholarship.
        """
        # Logic to create TentativeAdmission
        pass
