from fastapi import APIRouter

from .routers.regulations import router as regulations_router
from .routers.batches import router as batches_router
from .routers.student_promotion import router as promotion_router
from .routers.academic_dashboard import router as dashboard_router
from .routers.sections import router as sections_router
from .routers.allocations import router as allocations_router
from .routers.exams import router as exams_router
from .routers.attendance import router as attendance_router
from .routers.timetable import router as timetable_router
from .routers.student_assignment import router as student_assignment_router
from .routers.internal_exam import router as internal_exam_router
from .routers.university_exam import router as university_exam_router
from .routers.hall_ticket import router as hall_ticket_router

router = APIRouter()

router.include_router(regulations_router, prefix="/regulations", tags=["Regulations"])
router.include_router(batches_router, prefix="/batches", tags=["Academic Batches"])
router.include_router(promotion_router, prefix="/promotion", tags=["Promotion"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Academic Dashboard"])
router.include_router(sections_router, prefix="/sections", tags=["Sections"])
router.include_router(allocations_router, prefix="/allocations", tags=["Allocations"])
router.include_router(exams_router, prefix="/exams", tags=["Exams"])
router.include_router(attendance_router, prefix="/attendance", tags=["Attendance"])
router.include_router(timetable_router, prefix="/timetable", tags=["Timetable"])
router.include_router(student_assignment_router, prefix="/assignments", tags=["Assignments"])
router.include_router(internal_exam_router, prefix="/exams/internal", tags=["Internal Exams"])
router.include_router(university_exam_router, prefix="/exams/university", tags=["University Exams"])
router.include_router(hall_ticket_router, prefix="/hall-tickets", tags=["Hall Tickets"])
