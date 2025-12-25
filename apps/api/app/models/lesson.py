from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .subject import Subject
    from .faculty import Faculty

class TopicStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class QuestionType(str, Enum):
    MCQ = "MCQ"
    THEORETICAL = "THEORETICAL"
    PRACTICAL = "PRACTICAL"

class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class LessonPlan(SQLModel, table=True):
    """Overall lesson plan for a subject and faculty"""
    __tablename__ = "lesson_plan"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    faculty_id: int = Field(foreign_key="faculty.id", index=True)
    academic_year: str = Field(index=True)  # e.g., "2024-2025"
    
    total_hours_planned: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    subject: "Subject" = Relationship()
    faculty: "Faculty" = Relationship()
    topics: List["SyllabusTopic"] = Relationship(back_populates="lesson_plan", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class SyllabusTopic(SQLModel, table=True):
    """Specific topic within a lesson plan"""
    __tablename__ = "syllabus_topic"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    lesson_plan_id: int = Field(foreign_key="lesson_plan.id", index=True)
    
    unit_number: int
    title: str
    description: Optional[str] = None
    planned_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: TopicStatus = Field(default=TopicStatus.PENDING)
    
    # Relationships
    lesson_plan: LessonPlan = Relationship(back_populates="topics")

class QuestionBank(SQLModel, table=True):
    """Container for questions related to a subject"""
    __tablename__ = "question_bank"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)
    
    # Relationships
    subject: "Subject" = Relationship()
    questions: List["Question"] = Relationship(back_populates="bank", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Question(SQLModel, table=True):
    """Individual question in the bank"""
    id: Optional[int] = Field(default=None, primary_key=True)
    bank_id: int = Field(foreign_key="question_bank.id", index=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="syllabus_topic.id")
    
    text: str
    type: QuestionType = Field(default=QuestionType.THEORETICAL)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM)
    marks: int = Field(default=1)
    answer_key: Optional[str] = None
    options: Optional[str] = None  # JSON string for MCQ options
    
    # Relationships
    bank: QuestionBank = Relationship(back_populates="questions")
    topic: Optional[SyllabusTopic] = Relationship()
