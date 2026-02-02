"""
Entrance Exam Service
Handles entrance test configurations, hall tickets, and result processing.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from sqlmodel import Session, select, func
from ..models import EntranceTestConfig, EntranceExamResult, Application
from app.services.pdf_service import pdf_service

class EntranceExamService:
    @staticmethod
    def create_test_config(session: Session, data: Dict[str, Any]) -> EntranceTestConfig:
        config = EntranceTestConfig(**data)
        session.add(config)
        session.commit()
        session.refresh(config)
        return config

    @staticmethod
    def get_test_config(session: Session, config_id: int) -> Optional[EntranceTestConfig]:
        return session.get(EntranceTestConfig, config_id)

    @staticmethod
    def list_test_configs(session: Session, active_only: bool = True) -> List[EntranceTestConfig]:
        statement = select(EntranceTestConfig)
        if active_only:
            statement = statement.where(EntranceTestConfig.is_active == True)
        return session.exec(statement).all()

    @staticmethod
    def process_results(session: Session, config_id: int, results: List[Dict[str, Any]], entered_by: int) -> int:
        count = 0
        for res in results:
            # Logic to create or update EntranceExamResult
            # Should also link back to Application
            pass
        return count

    @staticmethod
    def generate_hall_ticket(session: Session, admission_id: int) -> str:
        # Link to pdf_service for hall ticket generation
        return "hall_ticket_url"
