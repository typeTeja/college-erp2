"""
Bulk Batch Setup Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field

class BulkBatchSetupRequest(BaseModel):
    """Request schema for bulk batch setup"""
    program_id: int = Field(..., description="Program ID")
    joining_year: int = Field(..., description="Joining year (e.g., 2024)")
    regulation_id: int = Field(..., description="Regulation ID to bind to this batch")
    
    # Section configuration
    sections_per_semester: int = Field(default=1, ge=1, le=10, description="Number of sections per semester (e.g., 2 for Section A, B)")
    section_capacity: int = Field(default=60, ge=10, le=200, description="Maximum students per section")
    
    # Lab/Practical batch configuration
    labs_per_semester: int = Field(default=0, ge=0, le=20, description="Number of lab groups per semester (0 for no labs)")
    lab_capacity: int = Field(default=40, ge=5, le=50, description="Maximum students per lab group")
    
    # Optional customization
    batch_name_override: Optional[str] = Field(None, description="Custom batch name (auto-generated if not provided)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "program_id": 1,
                "joining_year": 2024,
                "regulation_id": 1,
                "sections_per_semester": 2,
                "section_capacity": 60,
                "labs_per_semester": 6,
                "lab_capacity": 20
            }
        }


class BulkBatchSetupResponse(BaseModel):
    """Response schema for bulk batch setup"""
    batch_id: int
    batch_code: str
    batch_name: str
    
    # Statistics
    years_created: int
    semesters_created: int
    sections_created: int
    labs_created: int
    
    # Summary
    total_section_capacity: int
    total_lab_capacity: int
    
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "batch_id": 1,
                "batch_code": "2024-2028",
                "batch_name": "Batch 2024-2028",
                "years_created": 4,
                "semesters_created": 8,
                "sections_created": 16,
                "labs_created": 48,
                "total_section_capacity": 960,
                "total_lab_capacity": 960,
                "message": "Successfully created batch with complete academic structure"
            }
        }
