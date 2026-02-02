from .services.academic_service import academic_validation_service
from .services.batch_cloning_service import BatchCloningService
from .services.bulk_setup_service import BulkBatchSetupService
from .services.hall_ticket_service import HallTicketService
from .services.internal_exam_service import InternalExamService
from .services.student_assignment_service import StudentAssignmentService
from .services.university_exam_service import UniversityExamService

class AcademicService:
    """Consolidated Academic Service"""
    validation = academic_validation_service
    batch_cloning = BatchCloningService
    bulk_setup = BulkBatchSetupService
    hall_ticket = HallTicketService
    internal_exam = InternalExamService
    assignment = StudentAssignmentService
    university_exam = UniversityExamService

academic_service = AcademicService()
