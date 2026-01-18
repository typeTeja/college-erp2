# Fresh Database Deployment Guide

## Overview

This guide walks through setting up a fresh database and running all 16 migrations for the College ERP system.

---

## Prerequisites

- PostgreSQL installed
- Python 3.11+
- All backend dependencies installed

---

## Step 1: Create Fresh Database

### Option A: Using psql
```bash
# Connect to PostgreSQL
psql -U postgres

# Create new database
CREATE DATABASE college_erp_fresh;

# Create user (if needed)
CREATE USER college_erp_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE college_erp_fresh TO college_erp_user;

# Exit
\q
```

### Option B: Using createdb command
```bash
createdb -U postgres college_erp_fresh
```

---

## Step 2: Update Environment Configuration

Update `apps/api/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://college_erp_user:your_secure_password@localhost:5432/college_erp_fresh

# Or for local development
DATABASE_URL=postgresql://postgres:password@localhost:5432/college_erp_fresh
```

---

## Step 3: Run Migrations

```bash
cd apps/api

# Check current status
alembic current

# Run all migrations
alembic upgrade head

# Verify
alembic current
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002
...
INFO  [alembic.runtime.migration] Running upgrade 015 -> 016
```

---

## Step 4: Verify Database Schema

```bash
# Connect to database
psql -U postgres -d college_erp_fresh

# List all tables
\dt

# Should see 57 tables
```

Expected tables:
- student
- entrance_exam_result, scholarship_slab
- fee_structure, student_fee, student_fee_installment, fee_payment, fee_concession
- internal_exam, internal_exam_subject, internal_exam_marks
- hall_ticket_config, hall_ticket, discipline_block
- university_exam, university_exam_registration, university_exam_result
- document_category, student_document, document_verification
- student_portal_access, student_activity, notification
- payment_gateway_config, online_payment, payment_receipt
- And 35 more tables...

---

## Step 5: Create Initial Data (Optional)

### Create Admin User
```python
# Run Python script or use API
from app.models.user import User
from app.core.security import get_password_hash

admin = User(
    email="admin@college.edu",
    hashed_password=get_password_hash("admin123"),
    role="SUPER_ADMIN",
    is_active=True
)
# Save to database
```

### Create Academic Year
```python
from app.models.master_data import AcademicYear

academic_year = AcademicYear(
    year="2024-25",
    start_date="2024-06-01",
    end_date="2025-05-31",
    is_current=True
)
# Save to database
```

---

## Step 6: Test API Server

```bash
# Start server
uvicorn app.main:app --reload

# Test health endpoint
curl http://localhost:8000/health

# Test API docs
open http://localhost:8000/docs
```

---

## Step 7: Verify All Endpoints

Test critical endpoints:

```bash
# Fee Management
curl http://localhost:8000/api/v1/fees/structures

# Exams
curl http://localhost:8000/api/v1/internal-exams

# Library
curl http://localhost:8000/api/v1/library/books

# Hostel
curl http://localhost:8000/api/v1/hostel/hostels

# And so on...
```

---

## Migration Details

### All 16 Migrations in Order:

1. **001_enhance_student_model** - Student table enhancements
2. **002_entrance_exam_system** - Entrance exam tables
3. **003_enhance_fee_system** - Fee management tables
4. **004_internal_exam_system** - Internal exam tables
5. **005_hall_ticket_system** - Hall ticket tables
6. **006_university_exam_system** - University exam tables
7. **007_document_management** - Document tables
8. **008_student_portal** - Portal tables
9. **009_online_payment** - Payment tables
10. **010_attendance_communication** - Attendance tables
11. **011_library_management** - Library tables
12. **012_hostel_management** - Hostel tables
13. **013_transport_management** - Transport tables
14. **014_placement_training** - Placement tables
15. **015_hr_payroll** - HR tables
16. **016_rcms_admission_enhancements** - RCMS tables

---

## Rollback Plan

If something goes wrong:

```bash
# Rollback all migrations
alembic downgrade base

# Or rollback to specific version
alembic downgrade 015

# Then upgrade again
alembic upgrade head
```

---

## Troubleshooting

### Issue: Migration fails
```bash
# Check alembic version
alembic current

# Check database connection
psql -U postgres -d college_erp_fresh -c "SELECT 1"

# View migration history
alembic history
```

### Issue: Table already exists
- This means database is not fresh
- Drop and recreate database
- Run migrations again

### Issue: Foreign key constraint fails
- Check migration order
- Ensure all dependencies are met
- Review migration file

---

## Success Criteria

- ✅ All 16 migrations run successfully
- ✅ 57 tables created
- ✅ No errors in logs
- ✅ API server starts
- ✅ Endpoints respond correctly

---

## Next Steps

1. ✅ Database setup complete
2. Load initial/seed data
3. Test all API endpoints
4. Start frontend integration
5. User acceptance testing

---

**Document Version:** 1.0  
**Last Updated:** January 10, 2026  
**Status:** Ready for Execution
