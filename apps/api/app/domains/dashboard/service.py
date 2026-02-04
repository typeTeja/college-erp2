from typing import List, Optional
from sqlmodel import Session, select
from app.domains.dashboard.schemas import (
    PrincipalDashboardResponse, KPI, EnrollmentTrend, DepartmentPerformance,
    FeeCollectionSummary, PendingApproval, HighRiskAlert,
    ParentDashboardResponse, StudentProfile, ParentKPI,
    StudentDashboardResponse, StudentKPI,
    StaffDashboardResponse,
    FacultyDashboardResponse, FacultyKPI
)

# SERVICE LAYER - Currently returning MOCK data
# TODO: Replace with real DB queries in Phase 2.1

class DashboardService:
    
    def get_principal_dashboard(self, db: Session) -> PrincipalDashboardResponse:
        """
        Get executive summary for Principal/Admin
        """
        # Mock logic
        return PrincipalDashboardResponse(
            kpis=KPI(
                totalEnrollment=1234,
                enrollmentChange=12.5,
                feeCollection=4520000,
                feeCollectionRate=75.0,
                attendanceRate=87.5,
                highRiskStudents=23
            ),
            enrollmentTrends=[
                EnrollmentTrend(month="2024-01", count=320, department="BS"),
                EnrollmentTrend(month="2024-02", count=245, department="Eng")
            ],
            departmentPerformance=[
                DepartmentPerformance(department="Computer Science", students=320, attendance=92.0, avgGrade=8.2),
                DepartmentPerformance(department="Mechanical", students=240, attendance=85.0, avgGrade=7.8)
            ],
            feeCollectionSummary=[
                FeeCollectionSummary(category="Tuition", collected=3500000, expected=4500000),
                FeeCollectionSummary(category="Hostel", collected=1020000, expected=1200000)
            ],
            pendingApprovals=[
                PendingApproval(type="Leave Request", count=3, urgent=0),
                PendingApproval(type="Fee Waiver", count=7, urgent=2)
            ],
            highRiskAlerts=[
                HighRiskAlert(studentId=123, studentName="John Doe", reason="Attendance < 75%", severity="high")
            ]
        )

    def get_parent_dashboard(self, db: Session, user_id: int) -> ParentDashboardResponse:
        """
        Get dashboard for Parent
        """
        return ParentDashboardResponse(
            student=StudentProfile(
                id=1, name="Rahul Sharma", rollNo="CSE21001", 
                program="B.Tech CSE", semester=4, photo=None
            ),
            kpis=ParentKPI(attendance=88.5, cgpa=8.2, feeStatus="paid", alerts=0),
            attendanceOverview=[
                {"date": "2024-02-01", "status": "present"},
                {"date": "2024-02-02", "status": "absent"}
            ],
            academicPerformance=[
                {"subject": "Data Structures", "marks": 85, "total": 100, "grade": "A"}
            ],
            feePaymentStatus=[
                {"category": "Tuition", "amount": 50000, "paid": 50000, "dueDate": "2024-01-15", "status": "paid"}
            ],
            upcomingEvents=[
                {"title": "Mid-Sem Exam", "date": "2024-03-15", "type": "exam"}
            ],
            teacherMessages=[
                {"from_name": "Dr. Smith", "message": "Good progress", "date": "2024-02-01"}
            ]
        )

    def get_student_dashboard(self, db: Session, user_id: int) -> StudentDashboardResponse:
        """
        Get dashboard for Student
        """
        return StudentDashboardResponse(
            kpis=StudentKPI(attendance=87.5, cgpa=8.2, pendingAssignments=3, feeStatus="paid"),
            todaysTimetable=[
                {"time": "09:00 AM - 10:00 AM", "subject": "Data Structures", "faculty": "Dr. Smith", "room": "CS-101", "type": "lecture"}
            ],
            attendanceSummary=[
                {"subject": "Data Structures", "present": 28, "total": 32, "percentage": 87.5}
            ],
            internalMarks=[
                {"subject": "Data Structures", "test1": 18, "test2": 20, "assignment": 9, "total": 47}
            ],
            assignmentStatus=[
                {"title": "Binary Trees", "subject": "Data Structures", "dueDate": "2024-02-15", "status": "pending", "marks": None}
            ],
            examSchedule=[
                {"subject": "Data Structures", "date": "2024-03-15", "time": "10:00 AM", "room": "CS-101"}
            ]
        )

    def get_staff_dashboard(self, db: Session, role: str) -> StaffDashboardResponse:
        """
        Get dashboard for Staff (configurable role)
        """
        role = role.lower()
        if role == "librarian":
            return StaffDashboardResponse(
                role="librarian",
                kpis={
                    "booksIssuedToday": 15,
                    "overdueBooks": 4,
                    "newArrivals": 12,
                    "pendingReturns": 3
                },
                widgets={
                    "overdueBooks": [{"student": "Rahul S", "book": "Intro to Algo", "daysOverdue": 3}],
                    "stockAlerts": [{"book": "Clean Code", "current": 1, "minimum": 2}]
                }
            )
        # Default mock for others
        return StaffDashboardResponse(
            role=role,
            kpis={"pendingTasks": 5, "completedToday": 10},
            widgets={}
        )

    def get_faculty_dashboard(self, db: Session, user_id: int) -> FacultyDashboardResponse:
        """
        Get dashboard for Faculty
        """
        return FacultyDashboardResponse(
            kpis=FacultyKPI(
                classesToday=4,
                pendingAttendance=1,
                assignmentsToGrade=12,
                nextLecture="10:00 AM",
                nextLectureDetail="B.Tech CS - Year 2"
            ),
            todaysClasses=[
                {"id": 1, "time": "09:00 AM - 10:00 AM", "subject": "Data Structures", "room": "CS-101", "batch": "CSE-A", "status": "completed"},
                {"id": 2, "time": "10:00 AM - 11:00 AM", "subject": "Operating Systems", "room": "CS-102", "batch": "CSE-B", "status": "upcoming"}
            ],
            attendancePending=[
                {"id": 101, "date": "2024-02-04", "subject": "Operating Systems", "batch": "CSE-B", "period": 3, "status": "pending"}
            ],
            assignmentsToGrade=[
                {"id": 201, "title": "Binary Trees Implementation", "subject": "Data Structures", "submitted": 45, "total": 60, "dueDate": "2024-02-01"}
            ]
        )

dashboard_service = DashboardService()
