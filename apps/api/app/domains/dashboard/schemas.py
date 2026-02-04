from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from datetime import date

# ==========================================
# Principal Dashboard Schemas
# ==========================================

class KPI(BaseModel):
    totalEnrollment: int
    enrollmentChange: float
    feeCollection: float
    feeCollectionRate: float
    attendanceRate: float
    highRiskStudents: int

class EnrollmentTrend(BaseModel):
    month: str
    count: int
    department: str

class DepartmentPerformance(BaseModel):
    department: str
    students: int
    attendance: float
    avgGrade: float

class FeeCollectionSummary(BaseModel):
    category: str
    collected: float
    expected: float

class PendingApproval(BaseModel):
    type: str
    count: int
    urgent: int

class HighRiskAlert(BaseModel):
    studentId: int
    studentName: str
    reason: str
    severity: str  # "high" | "medium" | "low"

class PrincipalDashboardResponse(BaseModel):
    kpis: KPI
    enrollmentTrends: List[EnrollmentTrend]
    departmentPerformance: List[DepartmentPerformance]
    feeCollectionSummary: List[FeeCollectionSummary]
    pendingApprovals: List[PendingApproval]
    highRiskAlerts: List[HighRiskAlert]


# ==========================================
# Parent Dashboard Schemas
# ==========================================

class StudentProfile(BaseModel):
    id: int
    name: str
    rollNo: str
    program: str
    semester: int
    photo: Optional[str] = None

class ParentKPI(BaseModel):
    attendance: float
    cgpa: float
    feeStatus: str  # "paid" | "pending" | "overdue"
    alerts: int

class AttendanceRecord(BaseModel):
    date: str
    status: str  # "present" | "absent" | "leave"

class AcademicPerformance(BaseModel):
    subject: str
    marks: float
    total: float
    grade: str

class FeePaymentRecord(BaseModel):
    category: str
    amount: float
    paid: float
    dueDate: str
    status: str

class UpcomingEvent(BaseModel):
    title: str
    date: str
    type: str

class TeacherMessage(BaseModel):
    from_name: str
    message: str
    date: str

class ParentDashboardResponse(BaseModel):
    student: StudentProfile
    kpis: ParentKPI
    attendanceOverview: List[AttendanceRecord]
    academicPerformance: List[AcademicPerformance]
    feePaymentStatus: List[FeePaymentRecord]
    upcomingEvents: List[UpcomingEvent]
    teacherMessages: List[TeacherMessage]


# ==========================================
# Student Dashboard Schemas
# ==========================================

class StudentKPI(BaseModel):
    attendance: float
    cgpa: float
    pendingAssignments: int
    feeStatus: str

class TimetableEntry(BaseModel):
    time: str
    subject: str
    faculty: str
    room: str
    type: str

class AttendanceSummary(BaseModel):
    subject: str
    present: int
    total: int
    percentage: float

class InternalMark(BaseModel):
    subject: str
    test1: float
    test2: float
    assignment: float
    total: float

class AssignmentStatus(BaseModel):
    title: str
    subject: str
    dueDate: str
    status: str
    marks: Optional[float] = None

class ExamSchedule(BaseModel):
    subject: str
    date: str
    time: str
    room: str

class StudentDashboardResponse(BaseModel):
    kpis: StudentKPI
    todaysTimetable: List[TimetableEntry]
    attendanceSummary: List[AttendanceSummary]
    internalMarks: List[InternalMark]
    assignmentStatus: List[AssignmentStatus]
    examSchedule: List[ExamSchedule]


# ==========================================
# Staff Dashboard Schemas
# ==========================================

class StaffDashboardResponse(BaseModel):
    role: str
    kpis: Dict[str, Union[int, str]]
    widgets: Dict[str, List[Any]]


# ==========================================
# Faculty Dashboard Schemas
# ==========================================

class FacultyKPI(BaseModel):
    classesToday: int
    pendingAttendance: int
    assignmentsToGrade: int
    nextLecture: str
    nextLectureDetail: str

class FacultyClass(BaseModel):
    id: int
    time: str
    subject: str
    room: str
    batch: str
    status: str

class FacultyAttendancePending(BaseModel):
    id: int
    date: str
    subject: str
    batch: str
    period: int
    status: str

class FacultyAssignment(BaseModel):
    id: int
    title: str
    subject: str
    submitted: int
    total: int
    dueDate: str

class FacultyDashboardResponse(BaseModel):
    kpis: FacultyKPI
    todaysClasses: List[FacultyClass]
    attendancePending: List[FacultyAttendancePending]
    assignmentsToGrade: List[FacultyAssignment]
