from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel
from app.models.lesson import TopicStatus, QuestionType, DifficultyLevel

# Syllabus Topic Schemas
class SyllabusTopicBase(BaseModel):
    unit_number: int
    title: str
    description: Optional[str] = None
    planned_date: Optional[date] = None
    status: TopicStatus = TopicStatus.PENDING

class SyllabusTopicCreate(SyllabusTopicBase):
    lesson_plan_id: int

class SyllabusTopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    planned_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[TopicStatus] = None

class SyllabusTopicRead(SyllabusTopicBase):
    id: int
    lesson_plan_id: int
    completion_date: Optional[date] = None

    class Config:
        from_attributes = True

# Lesson Plan Schemas
class LessonPlanBase(BaseModel):
    subject_id: int
    faculty_id: int
    academic_year: str
    total_hours_planned: int = 0

class LessonPlanCreate(LessonPlanBase):
    topics: List[SyllabusTopicBase] = []

class LessonPlanUpdate(BaseModel):
    total_hours_planned: Optional[int] = None
    academic_year: Optional[str] = None

class LessonPlanRead(LessonPlanBase):
    id: int
    created_at: datetime
    updated_at: datetime
    topics: List[SyllabusTopicRead] = []

    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    text: str
    type: QuestionType = QuestionType.THEORETICAL
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    marks: int = 1
    answer_key: Optional[str] = None
    options: Optional[str] = None
    topic_id: Optional[int] = None

class QuestionCreate(QuestionBase):
    bank_id: int

class QuestionRead(QuestionBase):
    id: int
    bank_id: int

    class Config:
        from_attributes = True

# Question Bank Schemas
class QuestionBankBase(BaseModel):
    subject_id: int

class QuestionBankCreate(QuestionBankBase):
    pass

class QuestionBankRead(QuestionBankBase):
    id: int
    questions: List[QuestionRead] = []

    class Config:
        from_attributes = True

# Paper Generation Schema
class PaperGenerateRequest(BaseModel):
    subject_id: int
    total_marks: int
    easy_weight: int = 30  # percentage
    medium_weight: int = 40
    hard_weight: int = 30
    topics: Optional[List[int]] = None
