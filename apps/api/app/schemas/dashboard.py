"""
Academic Dashboard Schemas
"""
from typing import List, Optional
from pydantic import BaseModel

class DashboardLabGroup(BaseModel):
    """Lab group information"""
    id: int
    name: str
    code: str
    max_strength: int
    current_strength: int
    utilization_percentage: float

class DashboardSection(BaseModel):
    """Section information with labs"""
    id: int
    name: str
    code: str
    max_strength: int
    current_strength: int
    utilization_percentage: float
    faculty_id: Optional[int] = None
    faculty_name: Optional[str] = None
    lab_groups: List[DashboardLabGroup] = []

class DashboardSemester(BaseModel):
    """Semester information with sections"""
    id: int
    semester_no: int
    semester_name: str
    total_credits: int
    sections: List[DashboardSection] = []
    total_students: int
    total_capacity: int

class DashboardYear(BaseModel):
    """Program year information with semesters"""
    id: int
    year_no: int
    year_name: str
    semesters: List[DashboardSemester] = []
    total_students: int
    total_capacity: int

class DashboardBatch(BaseModel):
    """Batch information with complete hierarchy"""
    id: int
    batch_code: str
    batch_name: str
    program_name: str
    regulation_name: str
    status: str
    years: List[DashboardYear] = []
    total_students: int
    total_capacity: int
    overall_utilization: float

class AcademicDashboardResponse(BaseModel):
    """Complete academic dashboard data"""
    batches: List[DashboardBatch]
    summary: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "batches": [
                    {
                        "id": 1,
                        "batch_code": "2024-2028",
                        "batch_name": "Batch 2024-2028",
                        "program_name": "B.Sc Hotel Management",
                        "regulation_name": "R2024",
                        "status": "active",
                        "total_students": 240,
                        "total_capacity": 960,
                        "overall_utilization": 25.0,
                        "years": []
                    }
                ],
                "summary": {
                    "total_batches": 1,
                    "total_students": 240,
                    "total_capacity": 960,
                    "total_sections": 16,
                    "total_labs": 48
                }
            }
        }
