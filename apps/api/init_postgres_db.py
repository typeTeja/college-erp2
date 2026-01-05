"""
Initialize PostgreSQL database with all tables
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine
from sqlmodel import SQLModel

def init_db():
    print("Initializing database...")
    
    # IMPORT ALL MODELS to register them with metadata
    
    # 1. Core Models
    from app.models.user import User
    from app.models.role import Role
    from app.models.user_role import UserRole
    from app.models.permission import Permission, RolePermission
    
    # 2. Academic Foundation (New) - Import before Program to ensure registry availability?
    from app.models.academic.regulation import Regulation, RegulationSubject, RegulationSemester
    from app.models.academic.batch import AcademicBatch, BatchSemester, BatchSubject, ProgramYear
    from app.models.academic.student_history import StudentSemesterHistory, StudentPromotionLog
    
    # 3. Institutional Models
    from app.models.department import Department
    from app.models.program import Program
    from app.models.institute import InstituteInfo
    
    # 4. Master Data (Imports Section, AcademicYear, etc.)
    from app.models.master_data import (
        AcademicYear, Section, PracticalBatch, SubjectConfig, 
        Board, PreviousQualification, StudyGroup
    )
    
    # 5. People
    from app.models.student import Student
    from app.models.faculty import Faculty
    from app.models.staff import Staff
    from app.models.parent import Parent
    
    # 6. Operations & Modules
    from app.models.subject import Subject
    from app.models.timetable import TimeSlot, Classroom, ClassSchedule
    from app.models.fee import FeeStructure, FeeComponent, StudentFee
    from app.models.attendance import AttendanceSession
    from app.models.odc import ODCHotel, ODCRequest
    from app.models.library import Book
    from app.models.hostel import HostelRoom
    from app.models.inventory import Asset
    from app.models.communication import Notification
    from app.models.settings import SystemSetting
    
    print("Models imported. Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    init_db()
