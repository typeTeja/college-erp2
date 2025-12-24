from sqlmodel import Session, select, delete
from sqlalchemy import create_engine
from app.config.settings import settings
from app.models.student import Student
from app.models.parent import Parent
from app.models.user import User
from app.models.odc import StudentODCApplication, ODCPayout, ODCRequest, ODCHotel
from app.models.import_log import ImportLog
from app.models.user_role import UserRole

def clear_students():
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as session:
        print("Starting cleanup...")
        
        # 0. Delete ODC Payouts (depends on Application)
        print("Deleting ODC Payouts...")
        session.exec(delete(ODCPayout))
        
        # 1. Delete Student ODC Applications (depends on Student)
        print("Deleting ODC Applications...")
        session.exec(delete(StudentODCApplication))
        
        # 2. Delete Parents (linked to students)
        print("DeleteMapping Parents...")
        session.exec(delete(Parent))
        
        # 3. Identify Users to delete
        students = session.exec(select(Student)).all()
        user_ids = [s.user_id for s in students if s.user_id and s.user_id != 1]
        
        # 4. Delete Students
        print("Deleting Students...")
        session.exec(delete(Student))
        
        # 5. Delete Users 
        if user_ids:
            print(f"Deleting {len(user_ids)} associated Users...")
            # Delete UserRoles first
            stmt_roles = delete(UserRole).where(UserRole.user_id.in_(user_ids))
            session.exec(stmt_roles)
            
            # Delete ImportLogs for these users (if any)
            # The previous error "constraint fails (`import_log`... FOREIGN KEY (`uploaded_by_id`))"
            # suggests logs exist for these users. We should delete them or nullify.
            # Deleting logs is safer for clean slate.
            stmt_logs = delete(ImportLog).where(ImportLog.uploaded_by_id.in_(user_ids))
            session.exec(stmt_logs)
            
            stmt = delete(User).where(User.id.in_(user_ids))
            session.exec(stmt)
            
        session.commit()
        print("Cleanup complete successfully.")

if __name__ == "__main__":
    clear_students()
