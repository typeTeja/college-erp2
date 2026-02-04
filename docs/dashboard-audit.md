# Dashboard Audit - Current State Analysis

**Date:** February 4, 2026  
**Purpose:** Document current dashboard implementation for migration planning

---

## Current Dashboard Implementation

### Existing Dashboards: 3

1. **AdminDashboard**
2. **FacultyDashboard**
3. **StudentDashboard** (currently serves both applicants and enrolled students)

---

## AdminDashboard Analysis

### Current Usage

Used by 8 roles:

- SUPER_ADMIN
- ADMIN
- PRINCIPAL ⚠️ (needs separate dashboard)
- ADMISSION_OFFICER
- ODC_COORDINATOR
- ACCOUNTS ⚠️ (needs staff dashboard)
- LIBRARIAN ⚠️ (needs staff dashboard)
- WARDEN ⚠️ (needs staff dashboard)

### Current Widgets

1. **KPI Cards (4)**
   - Total Students
   - Active Students
   - Total Faculty
   - Pending Admissions

2. **Recent Admissions Table**
   - Shows latest applications
   - Columns: Name, Course, Contact, Status, Date

### Issues

- ❌ Too generic for specialized roles
- ❌ Principal sees same view as Librarian
- ❌ Missing role-specific insights
- ❌ No drill-down capabilities
- ❌ Static trends (hardcoded "+5.2% from last month")

### Data Source

- API: `/api/dashboard/stats`
- API: `/api/admissions/recent`

---

## FacultyDashboard Analysis

### Current Usage

- FACULTY role only

### Current Widgets

1. **KPI Cards (4)**
   - Today's Classes: "4" (hardcoded)
   - Pending Attendance: "1 Class" (hardcoded)
   - Assignments to Grade: "12" (hardcoded)
   - Next Lecture: "10:00 AM" (hardcoded)

2. **Upcoming Lectures**
   - Empty state: "No lectures scheduled"

### Issues

- ❌ All data is hardcoded
- ❌ No real API integration
- ❌ Missing timetable integration
- ❌ No student list
- ❌ No attendance marking interface

### Data Source

- None (all hardcoded)

### Required APIs

- `/api/faculty/{id}/classes/today`
- `/api/faculty/{id}/attendance/pending`
- `/api/faculty/{id}/assignments/to-grade`
- `/api/faculty/{id}/timetable`

---

## StudentDashboard Analysis

### Current Usage

- STUDENT role
- Serves both applicants AND enrolled students ⚠️

### Current Widgets (Applicant-focused)

1. **Application Info Cards (3)**
   - Application Number
   - Current Status
   - Payment Status

2. **Application Timeline (5 steps)**
   - Quick Apply
   - Payment
   - Application Form
   - Verification
   - Admission Confirmed

3. **Action Required Alert**
   - Shows when payment pending or form incomplete

### Strengths

- ✅ Excellent applicant workflow
- ✅ Clear progress timeline
- ✅ Action-oriented alerts
- ✅ Payment status tracking

### Issues

- ❌ No enrolled student features
- ❌ Missing: Attendance, Grades, Timetable, Assignments
- ❌ Lifecycle confusion (applicant vs. enrolled)

### Data Source

- API: `/api/admissions/my-application`

### Required for Enrolled Students

- `/api/students/{id}/attendance`
- `/api/students/{id}/grades`
- `/api/students/{id}/timetable`
- `/api/students/{id}/assignments`
- `/api/students/{id}/fees`

---

## Missing Dashboards

### 1. Principal Dashboard

**Priority:** 🔥 HIGH

**Required Widgets:**

- Enrollment trends (YoY, Dept-wise)
- Attendance compliance heatmap
- Detention/shortage risk count
- Fee collection vs. expected
- Hostel P&L snapshot
- High-risk alerts
- Pending escalated approvals
- Department performance table

**Required APIs:**

- `/api/dashboard/principal`
- `/api/reports/enrollment-trends`
- `/api/reports/attendance-compliance`
- `/api/reports/financial-summary`
- `/api/reports/department-performance`

### 2. Parent Dashboard

**Priority:** 🔥 HIGH

**Required Widgets:**

- Student profile card
- Attendance calendar
- Grade report
- Fee ledger
- Weekly timetable
- Announcements list

**Required APIs:**

- `/api/dashboard/parent/{parent_id}`
- `/api/parents/{id}/student`
- `/api/students/{id}/attendance/calendar`
- `/api/students/{id}/grades/latest`
- `/api/students/{id}/fees/ledger`
- `/api/students/{id}/timetable`
- `/api/announcements`

### 3. Enrolled Student Dashboard

**Priority:** 🔥 HIGH

**Required Widgets:**

- Today's timetable
- Attendance summary (subject-wise)
- Internal marks
- Assignment status
- Exam schedule
- Fee alerts

**Required APIs:**

- `/api/dashboard/student/{student_id}`
- `/api/students/{id}/timetable/today`
- `/api/students/{id}/attendance/summary`
- `/api/students/{id}/marks/internal`
- `/api/students/{id}/assignments`
- `/api/students/{id}/exams/upcoming`

### 4. Staff Dashboard (Configurable)

**Priority:** 🟡 MEDIUM

**Role-Specific Widgets:**

**Librarian:**

- Books issued today
- Overdue books
- New arrivals
- Stock alerts

**Warden:**

- Hostel occupancy
- Gate passes today
- Pending fines
- Complaints open

**Accounts:**

- Collections today
- Pending dues
- Failed payments
- Concession requests

**SSE:**

- Attendance risks
- Calls pending
- Follow-ups due
- Issues raised

**Required APIs:**

- `/api/dashboard/staff/{staff_id}?role={role}`
- Role-specific endpoints

---

## Backend API Gaps

### APIs That Exist

- ✅ `/api/dashboard/stats`
- ✅ `/api/admissions/recent`
- ✅ `/api/admissions/my-application`

### APIs Needed (High Priority)

- ⏳ `/api/dashboard/principal`
- ⏳ `/api/dashboard/parent/{parent_id}`
- ⏳ `/api/dashboard/student/{student_id}`
- ⏳ `/api/faculty/{id}/classes/today`
- ⏳ `/api/students/{id}/attendance/calendar`
- ⏳ `/api/students/{id}/grades/latest`
- ⏳ `/api/students/{id}/fees/ledger`

### APIs Needed (Medium Priority)

- ⏳ `/api/dashboard/staff/{staff_id}`
- ⏳ `/api/faculty/{id}/attendance/pending`
- ⏳ `/api/faculty/{id}/assignments/to-grade`
- ⏳ `/api/students/{id}/timetable/today`
- ⏳ `/api/students/{id}/assignments`

---

## Dashboard Routing Logic

### Current (apps/web/src/app/page.tsx)

```typescript
switch (userRole) {
  case 'SUPER_ADMIN':
  case 'ADMIN':
  case 'PRINCIPAL':          // ⚠️ Uses AdminDashboard
  case 'ADMISSION_OFFICER':
  case 'ODC_COORDINATOR':
  case 'ACCOUNTS':
  case 'LIBRARIAN':
  case 'WARDEN':
    return <AdminDashboard />;
  case 'FACULTY':
    return <FacultyDashboard />;
  case 'STUDENT':
    return <StudentDashboard />; // ⚠️ No lifecycle check
}
```

### Proposed

```typescript
switch (userRole) {
  case 'PRINCIPAL':
    return <PrincipalDashboard />;

  case 'PARENT':
    return <ParentDashboard />;

  case 'STUDENT':
    if (user?.enrollment_status === 'ENROLLED') {
      return <EnrolledStudentDashboard />;
    } else {
      return <ApplicantDashboard />;
    }

  case 'FACULTY':
    return <FacultyDashboard />; // Enhanced version

  case 'LIBRARIAN':
  case 'WARDEN':
  case 'ACCOUNTS':
  case 'SSE':
    return <StaffDashboard />;

  case 'SUPER_ADMIN':
  case 'ADMIN':
    return <AdminDashboard />; // Keep for super admin
}
```

---

## Implementation Priority

### Week 4: Principal Dashboard

- Create PrincipalDashboard component
- Create 8 principal-specific widgets
- Integrate with backend API
- Test with mock data first

### Week 5: Parent + Enrolled Student

- Rename StudentDashboard to ApplicantDashboard
- Create EnrolledStudentDashboard
- Create ParentDashboard
- Create 12 widgets total
- Update routing logic

### Week 6: Faculty + Staff

- Enhance FacultyDashboard with real data
- Create StaffDashboard with role configs
- Create 16 staff widgets (4 roles × 4 widgets)
- Test role switching

---

## Testing Strategy

### Dashboard-Specific Tests

**Principal Dashboard:**

- [ ] All KPIs load correctly
- [ ] Charts render with data
- [ ] Tables are sortable/filterable
- [ ] Alerts display properly
- [ ] Data refreshes every minute

**Parent Dashboard:**

- [ ] Student profile displays
- [ ] Attendance calendar interactive
- [ ] Fee payment button works
- [ ] Announcements load

**Enrolled Student Dashboard:**

- [ ] Timetable shows today's classes
- [ ] Attendance percentage accurate
- [ ] Assignment submission works
- [ ] Fee alerts show when due

**Faculty Dashboard:**

- [ ] Today's classes from real API
- [ ] Attendance marking functional
- [ ] Assignment grading works

**Staff Dashboard:**

- [ ] Role switching works
- [ ] Each role sees correct widgets
- [ ] No cross-role data leakage

---

## Performance Considerations

### Data Fetching

- Use React Query for caching
- Set appropriate stale times
- Implement optimistic updates
- Add loading skeletons

### Lazy Loading

- Lazy load dashboard components
- Lazy load heavy widgets (charts)
- Code split by dashboard

### Monitoring

- Track dashboard load times
- Monitor API response times
- Track widget render times
- Set up error boundaries

---

## Next Steps

1. ✅ Complete this audit
2. ⏳ Document backend API requirements
3. ⏳ Create mock data for testing
4. ⏳ Begin Week 4 implementation (Principal Dashboard)
5. ⏳ Set up dashboard analytics tracking
