from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.api import deps
from app.models.lesson import LessonPlan, SyllabusTopic, QuestionBank, Question, TopicStatus
from app.schemas.lesson import (
    LessonPlanCreate, LessonPlanRead, LessonPlanUpdate,
    SyllabusTopicCreate, SyllabusTopicRead, SyllabusTopicUpdate,
    QuestionCreate, QuestionRead, QuestionBankRead, PaperGenerateRequest
)
from datetime import datetime
from app.shared.enums import TopicStatus


router = APIRouter()

@router.post("/plans", response_model=LessonPlanRead)
def create_lesson_plan(
    *,
    session: Session = Depends(deps.get_session),
    plan_in: LessonPlanCreate
):
    """Create a new lesson plan with topics"""
    plan = LessonPlan(
        subject_id=plan_in.subject_id,
        faculty_id=plan_in.faculty_id,
        academic_year=plan_in.academic_year,
        total_hours_planned=plan_in.total_hours_planned
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)
    
    for topic_in in plan_in.topics:
        topic = SyllabusTopic(
            **topic_in.dict(),
            lesson_plan_id=plan.id
        )
        session.add(topic)
    
    session.commit()
    session.refresh(plan)
    return plan

@router.get("/plans/subject/{subject_id}", response_model=List[LessonPlanRead])
def get_subject_lesson_plans(
    subject_id: int,
    session: Session = Depends(deps.get_session)
):
    """Get all lesson plans for a subject"""
    plans = session.exec(select(LessonPlan).where(LessonPlan.subject_id == subject_id)).all()
    return plans

@router.put("/topics/{topic_id}/complete", response_model=SyllabusTopicRead)
def mark_topic_completed(
    topic_id: int,
    session: Session = Depends(deps.get_session)
):
    """Mark a syllabus topic as completed"""
    topic = session.get(SyllabusTopic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    topic.status = TopicStatus.COMPLETED
    topic.completion_date = datetime.utcnow().date()
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@router.post("/questions", response_model=QuestionRead)
def add_question(
    *,
    session: Session = Depends(deps.get_session),
    question_in: QuestionCreate
):
    """Add a question to a bank"""
    # Ensure bank exists or create one if needed
    bank = session.get(QuestionBank, question_in.bank_id)
    if not bank:
        raise HTTPException(status_code=404, detail="Question bank not found")
    
    question = Question(**question_in.dict())
    session.add(question)
    session.commit()
    session.refresh(question)
    return question

@router.get("/banks/{subject_id}", response_model=QuestionBankRead)
def get_question_bank(
    subject_id: int,
    session: Session = Depends(deps.get_session)
):
    """Get question bank for a subject"""
    bank = session.exec(select(QuestionBank).where(QuestionBank.subject_id == subject_id)).first()
    if not bank:
        # Create bank if it doesn't exist
        bank = QuestionBank(subject_id=subject_id)
        session.add(bank)
        session.commit()
        session.refresh(bank)
    return bank

@router.post("/generate-paper")
def generate_question_paper(
    request: PaperGenerateRequest,
    session: Session = Depends(deps.get_session)
):
    """Generate a question paper based on criteria (Mock Implementation)"""
    bank = session.exec(select(QuestionBank).where(QuestionBank.subject_id == request.subject_id)).first()
    if not bank:
        raise HTTPException(status_code=404, detail="No questions found for this subject")
    
    # In a real impl, we would use sophisticated selection logic based on weights
    # For now, just return all questions in the bank
    return {
        "subject_id": request.subject_id,
        "total_marks": request.total_marks,
        "questions": bank.questions
    }
