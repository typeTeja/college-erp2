# Domain Migration Inventory

**Generated:** /Users/teja/Projects/college-erp2/apps/api

---

## Summary Statistics

- **Total Files:** 310
- **Legacy Files:** 139
- **Domain Files:** 151
- **Core Files:** 13

### Files by Action

- **DELETE:** 59 files
- **KEEP:** 60 files
- **MERGE:** 154 files
- **MOVE:** 32 files
- **REVIEW:** 5 files

### Files by Domain

- **academic:** 50 files
- **admission:** 22 files
- **campus:** 44 files
- **communication:** 14 files
- **core:** 10 files
- **finance:** 24 files
- **hr:** 19 files
- **student:** 37 files
- **system:** 41 files
- **unknown:** 49 files

---

## High-Risk Files (Require Manual Review)

| File | Layer | Domain | Action | Notes |
|------|-------|--------|--------|-------|
| main.py | mixed | unknown | REVIEW | Domain assignment unclear; Requires manual review |
| domains/campus/transport/routers/transport.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/transport/models/logistics.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/transport/services/logistics.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/hostel/routers/hostel.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/hostel/models/infrastructure.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/hostel/models/operations.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/hostel/services/residency.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/library/routers/library.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/library/models/resource.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/library/models/circulation.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/library/services/circulation.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/inventory/routers/inventory.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/inventory/models/asset.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/inventory/services/asset.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/infrastructure/models/maintenance.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/infrastructure/models/facility.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/campus/infrastructure/services/facility.py | domain | campus | MERGE | May conflict with existing domain file |
| domains/admission/models.py | domain | admission | KEEP | Large file (>10KB) |
| domains/admission/schemas.py | domain | admission | KEEP | Large file (>10KB) |
| domains/admission/routers/application.py | domain | admission | MERGE | May conflict with existing domain file |
| domains/admission/routers/admin.py | domain | admission | MERGE | May conflict with existing domain file |
| domains/admission/routers/enhanced.py | domain | admission | MERGE | May conflict with existing domain file |
| domains/admission/services/merit_service.py | domain | admission | MERGE | May conflict with existing domain file |
| domains/admission/services/entrance_service.py | domain | admission | MERGE | May conflict with existing domain file |
| domains/admission/services/admission_service.py | domain | admission | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/student/routers/odc.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/routers/portal.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/routers/document.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/routers/students.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/odc.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/portal.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/parent.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/document.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/enrollment.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/models/student.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/schemas/odc.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/schemas/student.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/services/odc.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/services/portal.py | domain | student | MERGE | May conflict with existing domain file |
| domains/student/services/document.py | domain | student | MERGE | May conflict with existing domain file |
| domains/academic/routers/regulations.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/routers/student_promotion.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/routers/sections.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/attendance.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/hall_ticket.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/routers/exams.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/internal_exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/university_exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/timetable.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/student_assignment.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/allocations.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/academic_dashboard.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/routers/batches.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/models/exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/attendance.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/batch.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/student_history.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/regulation.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/hall_ticket.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/setup.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/internal_exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/university_exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/timetable.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/assignment.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/allocation.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/models/entrance_exam.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/services/student_assignment_service.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/services/bulk_setup_service.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/services/internal_exam_service.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/services/hall_ticket_service.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/services/dashboard_service.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/services/academic_service.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/academic/services/university_exam_service.py | domain | academic | MERGE | May conflict with existing domain file; Large file (>10KB) |
| domains/academic/services/batch_cloning_service.py | domain | academic | MERGE | May conflict with existing domain file |
| domains/system/routers/files.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/routers/audit.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/routers/imports.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/routers/settings.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/routers/institute.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/models/files.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/models/system.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/models/imports.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/schemas/files.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/schemas/system.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/schemas/imports.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/schemas/institute.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/services/import_service.py | domain | system | MERGE | May conflict with existing domain file |
| domains/system/services/storage_service.py | domain | system | MERGE | May conflict with existing domain file |
| domains/hr/routers/designation.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/routers/staff.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/routers/faculty.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/models/designation.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/models/staff.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/models/faculty.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/schemas/designation.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/schemas/staff.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/schemas/faculty.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/hr/services/hr_service.py | domain | hr | MERGE | May conflict with existing domain file |
| domains/finance/routers/fees.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/routers/gateway.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/routers/easebuzz.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/models/gateway.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/models/config.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/models/fee.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/services/gateway.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/services/fee.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/finance/services/easebuzz.py | domain | finance | MERGE | May conflict with existing domain file |
| domains/communication/routers/communication.py | domain | communication | MERGE | May conflict with existing domain file |
| domains/communication/models/communication.py | domain | communication | MERGE | May conflict with existing domain file |
| domains/communication/schemas/communication.py | domain | communication | MERGE | May conflict with existing domain file |
| domains/communication/services/sms_service.py | domain | communication | MERGE | May conflict with existing domain file |
| domains/communication/services/email_service.py | domain | communication | MERGE | May conflict with existing domain file |
| models/user.py | legacy | system | MERGE | May conflict with existing domain file |
| models/user_role.py | legacy | system | MERGE | May conflict with existing domain file |
| models/enhanced_admission.py | legacy | admission | MERGE | May conflict with existing domain file |
| models/permission.py | legacy | system | MERGE | May conflict with existing domain file |
| models/subject.py | legacy | academic | MERGE | May conflict with existing domain file |
| models/admissions.py | legacy | admission | MERGE | May conflict with existing domain file |
| models/lesson.py | legacy | academic | MERGE | May conflict with existing domain file |
| models/role.py | legacy | system | MERGE | May conflict with existing domain file |
| models/settings/notifications.py | legacy | communication | MERGE | May conflict with existing domain file |
| models/campus/infrastructure.py | legacy | campus | MERGE | May conflict with existing domain file |
| schemas/odc.py | legacy | student | MERGE | May conflict with existing domain file |
| schemas/exam.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/library.py | legacy | campus | MERGE | May conflict with existing domain file |
| schemas/file_schema.py | legacy | system | MERGE | May conflict with existing domain file |
| schemas/permission.py | legacy | system | MERGE | May conflict with existing domain file |
| schemas/subject.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/admissions.py | legacy | admission | MERGE | May conflict with existing domain file |
| schemas/attendance.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/lesson.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/role.py | legacy | system | MERGE | May conflict with existing domain file |
| schemas/fee.py | legacy | finance | MERGE | May conflict with existing domain file |
| schemas/hostel.py | legacy | campus | MERGE | May conflict with existing domain file |
| schemas/communication.py | legacy | communication | MERGE | May conflict with existing domain file |
| schemas/timetable.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/student_assignment.py | legacy | student | MERGE | May conflict with existing domain file |
| schemas/batch_cloning.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/student.py | legacy | student | MERGE | May conflict with existing domain file |
| schemas/master_data.py | legacy | unknown | MOVE | Domain assignment unclear; Large file (>10KB) |
| schemas/import_schema.py | legacy | system | MERGE | May conflict with existing domain file |
| schemas/easebuzz.py | legacy | finance | MERGE | May conflict with existing domain file |
| schemas/audit_log.py | legacy | system | MERGE | May conflict with existing domain file |
| schemas/inventory.py | legacy | campus | MERGE | May conflict with existing domain file |
| schemas/academic/batch.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/academic/student_history.py | legacy | student | MERGE | May conflict with existing domain file |
| schemas/academic/regulation.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/academic/hall_ticket.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/academic/internal_exam.py | legacy | academic | MERGE | May conflict with existing domain file |
| schemas/academic/entrance_exam.py | legacy | admission | MERGE | May conflict with existing domain file |
| api/deps.py | mixed | unknown | REVIEW | Domain assignment unclear; Requires manual review |
| api/api.py | mixed | unknown | REVIEW | Domain assignment unclear; Requires manual review |
| api/v1/roles.py | legacy | system | MERGE | May conflict with existing domain file |
| api/v1/admissions.py | legacy | admission | MERGE | May conflict with existing domain file |
| api/v1/documents.py | legacy | student | MERGE | May conflict with existing domain file |
| api/v1/lesson.py | legacy | academic | MERGE | May conflict with existing domain file |
| api/v1/master_data.py | legacy | unknown | MOVE | Domain assignment unclear; Large file (>10KB) |
| api/v1/students.py | legacy | student | MERGE | May conflict with existing domain file |
| api/endpoints/auth.py | mixed | unknown | REVIEW | Domain assignment unclear; Requires manual review |
| api/endpoints/dashboard.py | mixed | unknown | REVIEW | Domain assignment unclear; Requires manual review |
| services/admission_status.py | legacy | admission | MERGE | May conflict with existing domain file |
| services/admission_service.py | legacy | admission | MERGE | May conflict with existing domain file |

---

## Files Marked for Deletion

- `routers.py` - Domain assignment unclear
- `models/odc.py` - 
- `models/staff.py` - 
- `models/library.py` - 
- `models/admission_settings.py` - 
- `models/payment_gateway.py` - 
- `models/documents.py` - 
- `models/parent.py` - 
- `models/fee.py` - 
- `models/hostel.py` - 
- `models/communication.py` - 
- `models/enrollment.py` - 
- `models/student.py` - 
- `models/import_log.py` - 
- `models/student_portal.py` - 
- `models/audit_log.py` - 
- `models/file_metadata.py` - 
- `models/institute.py` - 
- `models/inventory.py` - 
- `models/faculty.py` - 
- `models/settings/system.py` - Domain assignment unclear
- `models/finance/fee_config.py` - 
- `schemas/staff.py` - 
- `schemas/settings.py` - 
- `schemas/institute.py` - 
- `schemas/faculty.py` - 
- `api/v1/odc.py` - 
- `api/v1/files.py` - 
- `api/v1/fees.py` - 
- `api/v1/staff.py` - 
- `api/v1/library.py` - 
- `api/v1/audit.py` - 
- `api/v1/transport.py` - 
- `api/v1/payment_gateway.py` - 
- `api/v1/import_api.py` - 
- `api/v1/hostel.py` - 
- `api/v1/communication.py` - 
- `api/v1/settings.py` - 
- `api/v1/fee_management.py` - 
- `api/v1/student_portal.py` - 
- `api/v1/easebuzz.py` - 
- `api/v1/institute.py` - 
- `api/v1/inventory.py` - 
- `api/v1/faculty.py` - 
- `workers/celery_app.py` - Domain assignment unclear
- `services/easebuzz_service.py` - 
- `services/odc_service.py` - 
- `services/payment_gateway_service.py` - 
- `services/hr_service.py` - Domain assignment unclear
- `services/sms_service.py` - 
- `services/document_service.py` - 
- `services/transport_service.py` - 
- `services/hostel_service.py` - 
- `services/email_service.py` - 
- `services/library_service.py` - 
- `services/fee_service.py` - 
- `services/student_portal_service.py` - 
- `services/import_service.py` - 
- `services/storage_service.py` - Domain assignment unclear

---

## Complete Inventory

| File Path | Layer | Domain | Action |
|-----------|-------|--------|--------|
| api/v1/lesson.py | legacy | academic | MERGE |
| domains/academic/models/__init__.py | domain | academic | KEEP |
| domains/academic/models/allocation.py | domain | academic | MERGE |
| domains/academic/models/assignment.py | domain | academic | MERGE |
| domains/academic/models/attendance.py | domain | academic | MERGE |
| domains/academic/models/batch.py | domain | academic | MERGE |
| domains/academic/models/entrance_exam.py | domain | academic | MERGE |
| domains/academic/models/exam.py | domain | academic | MERGE |
| domains/academic/models/hall_ticket.py | domain | academic | MERGE |
| domains/academic/models/internal_exam.py | domain | academic | MERGE |
| domains/academic/models/regulation.py | domain | academic | MERGE |
| domains/academic/models/setup.py | domain | academic | MERGE |
| domains/academic/models/student_history.py | domain | academic | MERGE |
| domains/academic/models/timetable.py | domain | academic | MERGE |
| domains/academic/models/university_exam.py | domain | academic | MERGE |
| domains/academic/router.py | domain | academic | KEEP |
| domains/academic/routers/academic_dashboard.py | domain | academic | MERGE |
| domains/academic/routers/allocations.py | domain | academic | MERGE |
| domains/academic/routers/attendance.py | domain | academic | MERGE |
| domains/academic/routers/batches.py | domain | academic | MERGE |
| domains/academic/routers/exams.py | domain | academic | MERGE |
| domains/academic/routers/hall_ticket.py | domain | academic | MERGE |
| domains/academic/routers/internal_exam.py | domain | academic | MERGE |
| domains/academic/routers/regulations.py | domain | academic | MERGE |
| domains/academic/routers/sections.py | domain | academic | MERGE |
| domains/academic/routers/student_assignment.py | domain | academic | MERGE |
| domains/academic/routers/student_promotion.py | domain | academic | MERGE |
| domains/academic/routers/timetable.py | domain | academic | MERGE |
| domains/academic/routers/university_exam.py | domain | academic | MERGE |
| domains/academic/service.py | domain | academic | KEEP |
| domains/academic/services/academic_service.py | domain | academic | MERGE |
| domains/academic/services/batch_cloning_service.py | domain | academic | MERGE |
| domains/academic/services/bulk_setup_service.py | domain | academic | MERGE |
| domains/academic/services/dashboard_service.py | domain | academic | MERGE |
| domains/academic/services/hall_ticket_service.py | domain | academic | MERGE |
| domains/academic/services/internal_exam_service.py | domain | academic | MERGE |
| domains/academic/services/student_assignment_service.py | domain | academic | MERGE |
| domains/academic/services/university_exam_service.py | domain | academic | MERGE |
| models/lesson.py | legacy | academic | MERGE |
| models/subject.py | legacy | academic | MERGE |
| schemas/academic/batch.py | legacy | academic | MERGE |
| schemas/academic/hall_ticket.py | legacy | academic | MERGE |
| schemas/academic/internal_exam.py | legacy | academic | MERGE |
| schemas/academic/regulation.py | legacy | academic | MERGE |
| schemas/attendance.py | legacy | academic | MERGE |
| schemas/batch_cloning.py | legacy | academic | MERGE |
| schemas/exam.py | legacy | academic | MERGE |
| schemas/lesson.py | legacy | academic | MERGE |
| schemas/subject.py | legacy | academic | MERGE |
| schemas/timetable.py | legacy | academic | MERGE |
| api/v1/admissions.py | legacy | admission | MERGE |
| domains/admission/__init__.py | domain | admission | KEEP |
| domains/admission/models.py | domain | admission | KEEP |
| domains/admission/router.py | domain | admission | KEEP |
| domains/admission/routers/__init__.py | domain | admission | KEEP |
| domains/admission/routers/admin.py | domain | admission | MERGE |
| domains/admission/routers/application.py | domain | admission | MERGE |
| domains/admission/routers/enhanced.py | domain | admission | MERGE |
| domains/admission/schemas.py | domain | admission | KEEP |
| domains/admission/service.py | domain | admission | KEEP |
| domains/admission/services/__init__.py | domain | admission | KEEP |
| domains/admission/services/admission_service.py | domain | admission | MERGE |
| domains/admission/services/entrance_service.py | domain | admission | MERGE |
| domains/admission/services/merit_service.py | domain | admission | MERGE |
| domains/admission/status_service.py | domain | admission | KEEP |
| models/admission_settings.py | legacy | admission | DELETE |
| models/admissions.py | legacy | admission | MERGE |
| models/enhanced_admission.py | legacy | admission | MERGE |
| schemas/academic/entrance_exam.py | legacy | admission | MERGE |
| schemas/admissions.py | legacy | admission | MERGE |
| services/admission_service.py | legacy | admission | MERGE |
| services/admission_status.py | legacy | admission | MERGE |
| api/v1/hostel.py | legacy | campus | DELETE |
| api/v1/inventory.py | legacy | campus | DELETE |
| api/v1/library.py | legacy | campus | DELETE |
| api/v1/transport.py | legacy | campus | DELETE |
| domains/campus/hostel/models/__init__.py | domain | campus | KEEP |
| domains/campus/hostel/models/infrastructure.py | domain | campus | MERGE |
| domains/campus/hostel/models/operations.py | domain | campus | MERGE |
| domains/campus/hostel/routers/hostel.py | domain | campus | MERGE |
| domains/campus/hostel/services/__init__.py | domain | campus | KEEP |
| domains/campus/hostel/services/residency.py | domain | campus | MERGE |
| domains/campus/infrastructure/models/__init__.py | domain | campus | KEEP |
| domains/campus/infrastructure/models/facility.py | domain | campus | MERGE |
| domains/campus/infrastructure/models/maintenance.py | domain | campus | MERGE |
| domains/campus/infrastructure/services/__init__.py | domain | campus | KEEP |
| domains/campus/infrastructure/services/facility.py | domain | campus | MERGE |
| domains/campus/inventory/models/__init__.py | domain | campus | KEEP |
| domains/campus/inventory/models/asset.py | domain | campus | MERGE |
| domains/campus/inventory/routers/inventory.py | domain | campus | MERGE |
| domains/campus/inventory/services/__init__.py | domain | campus | KEEP |
| domains/campus/inventory/services/asset.py | domain | campus | MERGE |
| domains/campus/library/models/__init__.py | domain | campus | KEEP |
| domains/campus/library/models/circulation.py | domain | campus | MERGE |
| domains/campus/library/models/resource.py | domain | campus | MERGE |
| domains/campus/library/routers/library.py | domain | campus | MERGE |
| domains/campus/library/services/__init__.py | domain | campus | KEEP |
| domains/campus/library/services/circulation.py | domain | campus | MERGE |
| domains/campus/models/__init__.py | domain | campus | KEEP |
| domains/campus/orchestration/student_exit.py | domain | campus | KEEP |
| domains/campus/router.py | domain | campus | KEEP |
| domains/campus/transport/models/__init__.py | domain | campus | KEEP |
| domains/campus/transport/models/logistics.py | domain | campus | MERGE |
| domains/campus/transport/routers/transport.py | domain | campus | MERGE |
| domains/campus/transport/services/__init__.py | domain | campus | KEEP |
| domains/campus/transport/services/logistics.py | domain | campus | MERGE |
| models/campus/infrastructure.py | legacy | campus | MERGE |
| models/hostel.py | legacy | campus | DELETE |
| models/inventory.py | legacy | campus | DELETE |
| models/library.py | legacy | campus | DELETE |
| schemas/hostel.py | legacy | campus | MERGE |
| schemas/inventory.py | legacy | campus | MERGE |
| schemas/library.py | legacy | campus | MERGE |
| services/hostel_service.py | legacy | campus | DELETE |
| services/library_service.py | legacy | campus | DELETE |
| services/transport_service.py | legacy | campus | DELETE |
| api/v1/communication.py | legacy | communication | DELETE |
| domains/communication/models/__init__.py | domain | communication | KEEP |
| domains/communication/models/communication.py | domain | communication | MERGE |
| domains/communication/router.py | domain | communication | KEEP |
| domains/communication/routers/communication.py | domain | communication | MERGE |
| domains/communication/schemas/communication.py | domain | communication | MERGE |
| domains/communication/services/__init__.py | domain | communication | KEEP |
| domains/communication/services/email_service.py | domain | communication | MERGE |
| domains/communication/services/sms_service.py | domain | communication | MERGE |
| models/communication.py | legacy | communication | DELETE |
| models/settings/notifications.py | legacy | communication | MERGE |
| schemas/communication.py | legacy | communication | MERGE |
| services/email_service.py | legacy | communication | DELETE |
| services/sms_service.py | legacy | communication | DELETE |
| config/logging_conf.py | core | core | KEEP |
| config/settings.py | core | core | KEEP |
| core/events.py | core | core | KEEP |
| core/permissions.py | core | core | KEEP |
| core/rbac.py | core | core | KEEP |
| core/security.py | core | core | KEEP |
| db/alembic/env.py | core | core | KEEP |
| db/base.py | core | core | KEEP |
| db/session.py | core | core | KEEP |
| middleware/rate_limit.py | core | core | KEEP |
| api/v1/easebuzz.py | legacy | finance | DELETE |
| api/v1/fee_management.py | legacy | finance | DELETE |
| api/v1/fees.py | legacy | finance | DELETE |
| api/v1/payment_gateway.py | legacy | finance | DELETE |
| domains/finance/models/__init__.py | domain | finance | KEEP |
| domains/finance/models/config.py | domain | finance | MERGE |
| domains/finance/models/fee.py | domain | finance | MERGE |
| domains/finance/models/gateway.py | domain | finance | MERGE |
| domains/finance/router.py | domain | finance | KEEP |
| domains/finance/routers/easebuzz.py | domain | finance | MERGE |
| domains/finance/routers/fees.py | domain | finance | MERGE |
| domains/finance/routers/gateway.py | domain | finance | MERGE |
| domains/finance/services/__init__.py | domain | finance | KEEP |
| domains/finance/services/easebuzz.py | domain | finance | MERGE |
| domains/finance/services/fee.py | domain | finance | MERGE |
| domains/finance/services/gateway.py | domain | finance | MERGE |
| models/fee.py | legacy | finance | DELETE |
| models/finance/fee_config.py | legacy | finance | DELETE |
| models/payment_gateway.py | legacy | finance | DELETE |
| schemas/easebuzz.py | legacy | finance | MERGE |
| schemas/fee.py | legacy | finance | MERGE |
| services/easebuzz_service.py | legacy | finance | DELETE |
| services/fee_service.py | legacy | finance | DELETE |
| services/payment_gateway_service.py | legacy | finance | DELETE |
| api/v1/faculty.py | legacy | hr | DELETE |
| api/v1/staff.py | legacy | hr | DELETE |
| domains/hr/models/__init__.py | domain | hr | KEEP |
| domains/hr/models/designation.py | domain | hr | MERGE |
| domains/hr/models/faculty.py | domain | hr | MERGE |
| domains/hr/models/staff.py | domain | hr | MERGE |
| domains/hr/router.py | domain | hr | KEEP |
| domains/hr/routers/designation.py | domain | hr | MERGE |
| domains/hr/routers/faculty.py | domain | hr | MERGE |
| domains/hr/routers/staff.py | domain | hr | MERGE |
| domains/hr/schemas/designation.py | domain | hr | MERGE |
| domains/hr/schemas/faculty.py | domain | hr | MERGE |
| domains/hr/schemas/staff.py | domain | hr | MERGE |
| domains/hr/services/__init__.py | domain | hr | KEEP |
| domains/hr/services/hr_service.py | domain | hr | MERGE |
| models/faculty.py | legacy | hr | DELETE |
| models/staff.py | legacy | hr | DELETE |
| schemas/faculty.py | legacy | hr | DELETE |
| schemas/staff.py | legacy | hr | DELETE |
| api/v1/documents.py | legacy | student | MERGE |
| api/v1/odc.py | legacy | student | DELETE |
| api/v1/student_portal.py | legacy | student | DELETE |
| api/v1/students.py | legacy | student | MERGE |
| domains/student/models/__init__.py | domain | student | KEEP |
| domains/student/models/document.py | domain | student | MERGE |
| domains/student/models/enrollment.py | domain | student | MERGE |
| domains/student/models/odc.py | domain | student | MERGE |
| domains/student/models/parent.py | domain | student | MERGE |
| domains/student/models/portal.py | domain | student | MERGE |
| domains/student/models/student.py | domain | student | MERGE |
| domains/student/router.py | domain | student | KEEP |
| domains/student/routers/document.py | domain | student | MERGE |
| domains/student/routers/odc.py | domain | student | MERGE |
| domains/student/routers/portal.py | domain | student | MERGE |
| domains/student/routers/students.py | domain | student | MERGE |
| domains/student/schemas/__init__.py | domain | student | KEEP |
| domains/student/schemas/odc.py | domain | student | MERGE |
| domains/student/schemas/student.py | domain | student | MERGE |
| domains/student/service.py | domain | student | KEEP |
| domains/student/services/__init__.py | domain | student | KEEP |
| domains/student/services/document.py | domain | student | MERGE |
| domains/student/services/odc.py | domain | student | MERGE |
| domains/student/services/portal.py | domain | student | MERGE |
| models/documents.py | legacy | student | DELETE |
| models/enrollment.py | legacy | student | DELETE |
| models/odc.py | legacy | student | DELETE |
| models/parent.py | legacy | student | DELETE |
| models/student.py | legacy | student | DELETE |
| models/student_portal.py | legacy | student | DELETE |
| schemas/academic/student_history.py | legacy | student | MERGE |
| schemas/odc.py | legacy | student | MERGE |
| schemas/student.py | legacy | student | MERGE |
| schemas/student_assignment.py | legacy | student | MERGE |
| services/document_service.py | legacy | student | DELETE |
| services/odc_service.py | legacy | student | DELETE |
| services/student_portal_service.py | legacy | student | DELETE |
| api/v1/audit.py | legacy | system | DELETE |
| api/v1/files.py | legacy | system | DELETE |
| api/v1/import_api.py | legacy | system | DELETE |
| api/v1/institute.py | legacy | system | DELETE |
| api/v1/roles.py | legacy | system | MERGE |
| api/v1/settings.py | legacy | system | DELETE |
| domains/system/models/__init__.py | domain | system | KEEP |
| domains/system/models/files.py | domain | system | MERGE |
| domains/system/models/imports.py | domain | system | MERGE |
| domains/system/models/system.py | domain | system | MERGE |
| domains/system/router.py | domain | system | KEEP |
| domains/system/routers/audit.py | domain | system | MERGE |
| domains/system/routers/files.py | domain | system | MERGE |
| domains/system/routers/imports.py | domain | system | MERGE |
| domains/system/routers/institute.py | domain | system | MERGE |
| domains/system/routers/settings.py | domain | system | MERGE |
| domains/system/schemas/files.py | domain | system | MERGE |
| domains/system/schemas/imports.py | domain | system | MERGE |
| domains/system/schemas/institute.py | domain | system | MERGE |
| domains/system/schemas/system.py | domain | system | MERGE |
| domains/system/services/__init__.py | domain | system | KEEP |
| domains/system/services/import_service.py | domain | system | MERGE |
| domains/system/services/storage_service.py | domain | system | MERGE |
| models/audit_log.py | legacy | system | DELETE |
| models/file_metadata.py | legacy | system | DELETE |
| models/import_log.py | legacy | system | DELETE |
| models/institute.py | legacy | system | DELETE |
| models/permission.py | legacy | system | MERGE |
| models/role.py | legacy | system | MERGE |
| models/user.py | legacy | system | MERGE |
| models/user_role.py | legacy | system | MERGE |
| schemas/audit_log.py | legacy | system | MERGE |
| schemas/file_schema.py | legacy | system | MERGE |
| schemas/import_schema.py | legacy | system | MERGE |
| schemas/institute.py | legacy | system | DELETE |
| schemas/permission.py | legacy | system | MERGE |
| schemas/role.py | legacy | system | MERGE |
| schemas/settings.py | legacy | system | DELETE |
| services/import_service.py | legacy | system | DELETE |
| utils/audit.py | core | system | KEEP |
| utils/file_upload.py | core | system | KEEP |
| api/api.py | mixed | unknown | REVIEW |
| api/deps.py | mixed | unknown | REVIEW |
| api/endpoints/auth.py | mixed | unknown | REVIEW |
| api/endpoints/dashboard.py | mixed | unknown | REVIEW |
| api/v1/analytics.py | legacy | unknown | MOVE |
| api/v1/auth.py | legacy | unknown | MOVE |
| api/v1/dashboard.py | legacy | unknown | MOVE |
| api/v1/hr.py | legacy | unknown | MOVE |
| api/v1/master_data.py | legacy | unknown | MOVE |
| api/v1/operations.py | legacy | unknown | MOVE |
| api/v1/password.py | legacy | unknown | MOVE |
| api/v1/placement.py | legacy | unknown | MOVE |
| api/v1/programs.py | legacy | unknown | MOVE |
| api/v1/reports.py | legacy | unknown | MOVE |
| api/v1/router.py | legacy | unknown | MOVE |
| main.py | mixed | unknown | REVIEW |
| models/__init__.py | legacy | unknown | KEEP |
| models/campus/__init__.py | legacy | unknown | KEEP |
| models/department.py | legacy | unknown | MOVE |
| models/enums.py | legacy | unknown | MOVE |
| models/finance/__init__.py | legacy | unknown | KEEP |
| models/master_data.py | legacy | unknown | MOVE |
| models/operations.py | legacy | unknown | MOVE |
| models/placement/__init__.py | legacy | unknown | KEEP |
| models/placement/company.py | legacy | unknown | MOVE |
| models/program.py | legacy | unknown | MOVE |
| models/settings/__init__.py | legacy | unknown | KEEP |
| models/settings/registration.py | legacy | unknown | MOVE |
| models/settings/system.py | legacy | unknown | DELETE |
| routers.py | mixed | unknown | DELETE |
| schemas/academic/__init__.py | legacy | unknown | KEEP |
| schemas/auth.py | legacy | unknown | MOVE |
| schemas/bulk_setup.py | legacy | unknown | MOVE |
| schemas/dashboard.py | legacy | unknown | MOVE |
| schemas/json_fields.py | legacy | unknown | MOVE |
| schemas/master_data.py | legacy | unknown | MOVE |
| schemas/operations.py | legacy | unknown | MOVE |
| schemas/program.py | legacy | unknown | MOVE |
| services/activity_logger.py | legacy | unknown | MOVE |
| services/analytics_service.py | legacy | unknown | MOVE |
| services/auth_service.py | legacy | unknown | MOVE |
| services/hr_service.py | legacy | unknown | DELETE |
| services/password_service.py | legacy | unknown | MOVE |
| services/pdf_service.py | legacy | unknown | MOVE |
| services/placement_service.py | legacy | unknown | MOVE |
| services/program_service.py | legacy | unknown | MOVE |
| services/storage_service.py | legacy | unknown | DELETE |
| utils/academic_validation.py | core | unknown | KEEP |
| workers/celery_app.py | mixed | unknown | DELETE |
