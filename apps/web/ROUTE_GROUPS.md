# Route Group Ownership & Layout Isolation

## Overview

This document defines the ownership and security boundaries for route groups in the College ERP application. **Layouts are security boundaries**, not just UI wrappers.

## Route Groups

### `(dashboard)` - Admin & Staff Portal

**Layout:** `DashboardLayout` with `GroupedSidebar`  
**Access:** Admin, Faculty, Staff roles  
**Routes:**

- `/` - Dashboard home
- `/admissions` - Admin view of applications
- `/admissions/[id]` - Application details (admin)
- `/config/*` - System configuration
- `/setup/*` - Academic setup
- `/system/*` - System administration
- `/students/*` - Student management
- `/fees/*` - Fee management
- `/attendance/*` - Attendance tracking
- All other admin/staff features

**Security:** Full admin navigation with role-based filtering in sidebar.

---

### `(applicant)` - Applicant Portal

**Layout:** `ApplicantLayout` (minimal header only)  
**Access:** Applicants (students who applied but not yet admitted)  
**Routes:**

- `/admissions/complete` - Complete application form

**Security:**

- No admin sidebar
- No system navigation
- Only shows: Logo, User menu, Logout
- Cannot access any `(dashboard)` routes

---

### `(auth)` - Authentication

**Layout:** Minimal auth layout  
**Access:** Public  
**Routes:**

- `/login`
- `/register` (if applicable)

---

### Root Routes (No Group)

**Layout:** Root layout only  
**Access:** Public  
**Routes:**

- `/apply` - Public quick apply form
- `/apply/success` - Application success page
- `/apply/failure` - Application failure page

---

## Security Principles

1. **Route-group–level isolation** is the primary security control
2. **Role-based filtering** in sidebars is a secondary safeguard
3. **Never import admin layouts** into applicant routes
4. **Prefer moving routes** over adding role checks to existing layouts
5. **Treat layouts as security boundaries**, not just UI wrappers

## Adding New Routes

### For Admin/Staff Features

✅ Place under `app/(dashboard)/`  
✅ Will automatically use `DashboardLayout`  
✅ Will show admin sidebar with role filtering

### For Applicant Features

✅ Place under `app/(applicant)/`  
✅ Will automatically use `ApplicantLayout`  
✅ Will show minimal header only

### For Public Features

✅ Place under `app/` (root)  
✅ Create custom layout if needed  
✅ No authentication required

## Migration History

- **2026-02-07**: Created `(applicant)` route group
- **2026-02-07**: Moved `/admissions/complete` from `(dashboard)` to `(applicant)` to prevent admin navigation leakage

## Verification Checklist

When adding or moving routes:

- [ ] Route is in correct group for its role
- [ ] Layout matches security requirements
- [ ] No admin components in applicant layouts
- [ ] No applicant-specific logic in admin layouts
- [ ] Links use relative paths (work across route groups)
- [ ] Tested with appropriate user role
