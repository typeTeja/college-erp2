"""
Batch Cloning Schemas
"""
from typing import Optional
from pydantic import BaseModel, Field


class CloneOptions(BaseModel):
    """Options for batch cloning"""
    clone_faculty_assignments: bool = Field(
        default=False,
        description="Clone faculty assignments to sections"
    )
    section_capacity_multiplier: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Multiply section capacities by this factor"
    )
    lab_capacity_multiplier: float = Field(
        default=1.0,
        ge=0.1,
        le=5.0,
        description="Multiply lab capacities by this factor"
    )
    custom_batch_name: Optional[str] = Field(
        default=None,
        description="Custom name for the cloned batch"
    )


class BatchCloneRequest(BaseModel):
    """Request to clone a batch"""
    new_joining_year: int = Field(..., ge=2020, le=2100)
    new_regulation_id: int = Field(..., gt=0)
    clone_options: CloneOptions = Field(default_factory=CloneOptions)


class BatchCloneResponse(BaseModel):
    """Response after cloning a batch"""
    batch_id: int
    batch_code: str
    batch_name: str
    source_batch_id: int
    years_created: int
    semesters_created: int
    sections_created: int
    labs_created: int
    message: str
