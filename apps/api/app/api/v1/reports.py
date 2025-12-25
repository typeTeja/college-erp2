from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from app.api import deps
from app.models.student import Student
from app.models.fee import FeePayment
from app.models.attendance import AttendanceRecord
from app.models.inventory import Asset
from app.models.lesson import SyllabusTopic
from app.models.user import User
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/academic/syllabus-progress")
def get_syllabus_progress_report(
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Aggregate syllabus completion % per subject/department"""
    # Simple aggregation for demonstration
    topics = session.exec(select(SyllabusTopic)).all()
    total = len(topics)
    completed = len([t for t in topics if t.is_completed])
    
    return {
        "total_topics": total,
        "completed_topics": completed,
        "completion_percentage": (completed / total * 100) if total > 0 else 0,
        # In a real app, group by subject_id
    }

@router.get("/academic/attendance-summary")
def get_attendance_summary(
    session: Session = Depends(deps.get_session)
):
    """Overall attendance trends"""
    records = session.exec(select(AttendanceRecord)).all()
    total = len(records)
    present = len([r for r in records if r.status == "PRESENT"])
    
    return {
        "total_records": total,
        "overall_percentage": (present / total * 100) if total > 0 else 0
    }

@router.get("/financial/fee-collection")
def get_fee_collection_report(
    session: Session = Depends(deps.get_session)
):
    """Daily fee collection stats for the last 30 days"""
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    payments = session.exec(
        select(FeePayment).where(FeePayment.payment_date >= thirty_days_ago)
    ).all()
    
    total_collected = sum(p.amount for p in payments)
    
    return {
        "count": len(payments),
        "total_collected": total_collected,
        "currency": "INR"
    }

@router.get("/inventory/stock-status")
def get_inventory_report(
    session: Session = Depends(deps.get_session)
):
    """Inventory levels and valuation"""
    assets = session.exec(select(Asset)).all()
    total_value = sum(a.total_stock * float(a.unit_price) for a in assets)
    low_stock_count = len([a for a in assets if a.available_stock <= a.reorder_level])
    
    return {
        "total_items": len(assets),
        "total_valuation": total_value,
        "low_stock_items": low_stock_count
    }

@router.get("/hr/faculty-workload")
def get_faculty_workload(
    session: Session = Depends(deps.get_session)
):
    """Stub for faculty workload report"""
    return {"message": "Reporting endpoints for faculty workload are being implemented."}
