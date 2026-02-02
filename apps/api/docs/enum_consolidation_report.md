# Enum Consolidation Report

**Total files with enums:** 21

**Total enum definitions found:** 54

## Enums by Domain

### Academic (10 enums)

- **AttendanceStatus** (4 values) - `domains/academic/models/attendance.py`
- **SessionStatus** (3 values) - `domains/academic/models/attendance.py`
- **ExamType** (4 values) - `domains/academic/models/exam.py`
- **ExamStatus** (3 values) - `domains/academic/models/exam.py`
- **DayOfWeek** (7 values) - `domains/academic/models/timetable.py`
- **SlotType** (4 values) - `domains/academic/models/timetable.py`
- **AdjustmentStatus** (4 values) - `domains/academic/models/timetable.py`
- **AcademicYearStatus** (3 values) - `models/enums.py`
- **SubjectType** (5 values) - `models/enums.py`
- **ExamType** (3 values) - `models/enums.py`

### Admission (3 enums)

- **ApplicationPaymentStatus** (3 values) - `domains/admission/models.py`
- **ApplicationStatus** (6 values) - `domains/student/models/odc.py`
- **ScholarshipCategory** (5 values) - `models/enums.py`

### Campus (11 enums)

- **HostelType** (4 values) - `domains/campus/hostel/models/infrastructure.py`
- **RoomType** (3 values) - `domains/campus/hostel/models/infrastructure.py`
- **GatePassType** (3 values) - `domains/campus/hostel/models/operations.py`
- **GatePassStatus** (6 values) - `domains/campus/hostel/models/operations.py`
- **ComplaintStatus** (4 values) - `domains/campus/hostel/models/operations.py`
- **AssetCategory** (6 values) - `domains/campus/inventory/models/asset.py`
- **AllocationStatus** (4 values) - `domains/campus/inventory/models/asset.py`
- **UniformSize** (7 values) - `domains/campus/inventory/models/asset.py`
- **IssueStatus** (4 values) - `domains/campus/library/models/circulation.py`
- **BookStatus** (4 values) - `domains/campus/library/models/resource.py`
- **MemberType** (3 values) - `domains/campus/library/models/resource.py`

### Communication (3 enums)

- **CircularTarget** (6 values) - `domains/communication/models/communication.py`
- **NotificationType** (4 values) - `domains/communication/models/communication.py`
- **NotificationChannel** (4 values) - `domains/communication/models/communication.py`

### Finance (6 enums)

- **FeeCategory** (4 values) - `domains/finance/models/fee.py`
- **PaymentMode** (5 values) - `domains/finance/models/fee.py`
- **PaymentStatus** (4 values) - `domains/finance/models/fee.py`
- **PaymentStatus** (6 values) - `domains/finance/models/gateway.py`
- **PaymentMode** (5 values) - `domains/finance/models/gateway.py`
- **PaymentMethod** (4 values) - `domains/student/models/odc.py`

### Generic (8 enums)

- **Gender** (3 values) - `models/enums.py`
- **BloodGroup** (8 values) - `models/enums.py`
- **RoomType** (8 values) - `models/enums.py`
- **TopicStatus** (2 values) - `models/lesson.py`
- **QuestionType** (3 values) - `models/lesson.py`
- **TicketStatus** (4 values) - `models/operations.py`
- **ProgramType** (5 values) - `models/program.py`
- **ProgramStatus** (3 values) - `models/program.py`

### Other (3 enums)

- **CreatedFrom** (3 values) - `models/enums.py`
- **DifficultyLevel** (3 values) - `models/lesson.py`
- **TicketPriority** (4 values) - `models/operations.py`

### Student (5 enums)

- **GenderPreference** (3 values) - `domains/student/models/odc.py`
- **ODCStatus** (4 values) - `domains/student/models/odc.py`
- **PayoutStatus** (2 values) - `domains/student/models/odc.py`
- **BillingStatus** (4 values) - `domains/student/models/odc.py`
- **StudentStatus** (9 values) - `models/enums.py`

### System (5 enums)

- **SettingGroup** (5 values) - `domains/system/models/system.py`
- **AuditLogAction** (7 values) - `domains/system/models/system.py`
- **ImportRowStatus** (4 values) - `domains/system/schemas/imports.py`
- **ImportRowStatus** (4 values) - `domains/system/schemas/system.py`
- **ImportRowStatus** (4 values) - `schemas/import_schema.py`

## Files with Enums

- `domains/academic/models/attendance.py`
- `domains/academic/models/exam.py`
- `domains/academic/models/timetable.py`
- `domains/admission/models.py`
- `domains/campus/hostel/models/infrastructure.py`
- `domains/campus/hostel/models/operations.py`
- `domains/campus/inventory/models/asset.py`
- `domains/campus/library/models/circulation.py`
- `domains/campus/library/models/resource.py`
- `domains/communication/models/communication.py`
- `domains/finance/models/fee.py`
- `domains/finance/models/gateway.py`
- `domains/student/models/odc.py`
- `domains/system/models/system.py`
- `domains/system/schemas/imports.py`
- `domains/system/schemas/system.py`
- `models/enums.py`
- `models/lesson.py`
- `models/operations.py`
- `models/program.py`
- `schemas/import_schema.py`
