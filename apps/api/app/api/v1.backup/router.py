from fastapi import APIRouter
from app.api.v1 import (
    dashboard, admissions, import_api, fees, staff, operations, 
    programs, library, hostel, faculty, lesson, inventory, 
    communication, reports, settings, institute, files, master_data, 
    audit, easebuzz, auth
)
from app.domains.academic.router import router as academic_router
from app.domains.student.router import router as student_router
from app.domains.finance.router import router as finance_router
from app.domains.campus.router import router as campus_router
from app.domains.hr.router import router as hr_router
from app.domains.communication.router import router as communication_router
from app.domains.system.router import router as system_router

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(communication_router, prefix="/communication", tags=["Communication Domain"])
api_router.include_router(system_router, prefix="/system", tags=["System Domain"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(academic_router, prefix="/academic", tags=["Academic"])
# ODC and other student modules now under /students/ prefix in Domain Router
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(admissions.router, prefix="/admissions", tags=["admissions"])
api_router.include_router(import_api.router, prefix="/import", tags=["import"])
api_router.include_router(finance_router, prefix="/finance", tags=["Finance Domain"])
api_router.include_router(student_router, prefix="/students", tags=["Student Domain"])
api_router.include_router(campus_router, prefix="/campus", tags=["Campus Domain"])
api_router.include_router(hr_router, prefix="/hr", tags=["People & HR Domain"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(programs.router, prefix="/programs", tags=["programs"])
api_router.include_router(faculty.router, prefix="/faculty", tags=["faculty"])
api_router.include_router(lesson.router, prefix="/lesson", tags=["lesson"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(institute.router, prefix="/institute", tags=["institute"])
api_router.include_router(audit.router, prefix="/audit-logs", tags=["audit"])
api_router.include_router(master_data.router, prefix="/master", tags=["master-data"])
