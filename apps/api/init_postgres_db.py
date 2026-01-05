"""
Initialize PostgreSQL database with all tables
"""
from app.db.session import engine
from sqlmodel import SQLModel

# Import all existing models to ensure they're registered
try:
    from app.models.user import User
    from app.models.role import Role
except ImportError:
    pass

try:
    from app.models.student import Student
except ImportError:
    pass

try:
    from app.models.department import Department
    from app.models.program import Program
except ImportError:
    pass

try:
    from app.models.academic_year import AcademicYear
except ImportError:
    pass

try:
    from app.models.admission import Application, ApplicationDocument
except ImportError:
    pass

try:
    from app.models.settings import SystemSettings, AuditLog
except ImportError:
    pass

try:
    from app.models.institute import InstituteInfo
except ImportError:
    pass

# Import academic foundation models (our new models)
from app.models.academic.regulation import (
    Regulation,
    RegulationSubject,
    RegulationSemester,
    RegulationPromotionRule
)
from app.models.academic.batch import (
    AcademicBatch,
    BatchSubject,
    BatchSemester,
    ProgramYear
)
from app.models.academic.student_history import (
    StudentSemesterHistory,
    StudentPromotionLog,
    StudentRegulationMigration
)

def init_db():
    """Create all tables in PostgreSQL database"""
    print("Creating all tables in PostgreSQL database...")
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    print("✅ All tables created successfully!")
    print("\nTables created:")
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    for table in sorted(tables):
        print(f"  ✓ {table}")
    
    print(f"\n📊 Total tables: {len(tables)}")

if __name__ == "__main__":
    init_db()
