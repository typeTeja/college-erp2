# Settings Audit - Current State Analysis

**Date:** February 4, 2026  
**Purpose:** Document current settings page structure for migration planning

---

## Current Settings Page Structure

### Tab Count: 20+ tabs

### Tab List (in order of appearance):

1. **Institute Information**
   - Current URL: `/settings?tab=institute`
   - New Location: `/setup/institute`
   - Category: Institutional Setup
   - Usage: One-time configuration
   - Priority: High

2. **Departments**
   - Current URL: `/settings?tab=departments`
   - New Location: `/setup/departments`
   - Category: Institutional Setup
   - Usage: Yearly updates
   - Priority: High

3. **Programs**
   - Current URL: `/settings?tab=programs`
   - New Location: `/setup/programs`
   - Category: Institutional Setup
   - Usage: Yearly updates
   - Priority: High

4. **Academic Years**
   - Current URL: `/settings?tab=academic-years`
   - New Location: `/setup/academic-years`
   - Category: Institutional Setup
   - Usage: Yearly
   - Priority: High

5. **Batches**
   - Current URL: `/settings?tab=batches`
   - New Location: `/setup/batches`
   - Category: Institutional Setup
   - Usage: Yearly
   - Priority: Medium

6. **Designations**
   - Current URL: `/settings?tab=designations`
   - New Location: `/setup/designations`
   - Category: Institutional Setup
   - Usage: Rare
   - Priority: Medium

7. **Fee Heads**
   - Current URL: `/settings?tab=fee-heads`
   - New Location: `/config/finance/fee-heads`
   - Category: Finance Configuration
   - Usage: Yearly
   - Priority: High

8. **Scholarships**
   - Current URL: `/settings?tab=scholarships`
   - New Location: `/config/finance/scholarships`
   - Category: Finance Configuration
   - Usage: Yearly
   - Priority: Medium

9. **Admission Settings**
   - Current URL: `/settings?tab=admission`
   - New Location: `/config/admission/settings`
   - Category: Admission Configuration
   - Usage: Yearly
   - Priority: High

10. **Boards**
    - Current URL: `/settings?tab=boards`
    - New Location: `/config/admission/boards`
    - Category: Admission Configuration
    - Usage: Rare
    - Priority: Low

11. **Categories**
    - Current URL: `/settings?tab=categories`
    - New Location: `/config/admission/categories`
    - Category: Admission Configuration
    - Usage: Rare
    - Priority: Low

12. **Sources**
    - Current URL: `/settings?tab=sources`
    - New Location: `/config/admission/sources`
    - Category: Admission Configuration
    - Usage: Rare
    - Priority: Low

13. **Academic Regulations**
    - Current URL: `/settings?tab=regulations`
    - New Location: `/config/academic/regulations`
    - Category: Academic Configuration
    - Usage: Yearly
    - Priority: High

14. **Academic Structure**
    - Current URL: `/settings?tab=structure`
    - New Location: `/config/academic/structure`
    - Category: Academic Configuration
    - Usage: Yearly
    - Priority: Medium

15. **Integrations**
    - Current URL: `/settings?tab=integrations`
    - New Location: `/system/integrations`
    - Category: System Administration
    - Usage: Rare
    - Priority: Medium

16. **Audit Logs**
    - Current URL: `/settings?tab=audit`
    - New Location: `/system/audit`
    - Category: System Administration
    - Usage: As needed
    - Priority: Low

17. **Profile** (User-specific)
    - Current URL: `/settings?tab=profile`
    - New Location: `/profile`
    - Category: User Preferences
    - Usage: Daily
    - Priority: High

18. **Security** (User-specific)
    - Current URL: `/settings?tab=security`
    - New Location: `/profile/security`
    - Category: User Preferences
    - Usage: Rare
    - Priority: Medium

19. **Notifications** (User-specific)
    - Current URL: `/settings?tab=notifications`
    - New Location: `/profile/notifications`
    - Category: User Preferences
    - Usage: Weekly
    - Priority: Medium

20. **Theme** (User-specific)
    - Current URL: `/settings?tab=theme`
    - New Location: `/profile/preferences`
    - Category: User Preferences
    - Usage: Rare
    - Priority: Low

---

## Migration Priority Matrix

### High Priority (Week 2)

- Institute Information
- Departments
- Programs
- Academic Years

### Medium Priority (Week 3)

- Fee Heads
- Admission Settings
- Academic Regulations
- Batches
- Designations

### Low Priority (Week 4)

- Scholarships
- Boards, Categories, Sources
- Academic Structure
- Integrations
- Audit Logs

### User Preferences (Week 4)

- Profile
- Security
- Notifications
- Theme

---

## Usage Analytics (To Be Collected)

### Most Accessed Tabs (Estimated)

1. Institute Information - ~50 views/month
2. Departments - ~30 views/month
3. Programs - ~40 views/month
4. Fee Heads - ~25 views/month
5. Admission Settings - ~35 views/month

### Least Accessed Tabs

1. Theme - ~5 views/month
2. Boards - ~3 views/month
3. Categories - ~4 views/month

---

## Dependencies

### Tabs with No Dependencies

- Institute Information
- Theme
- Notifications

### Tabs with Dependencies

- Programs (depends on Departments)
- Batches (depends on Programs, Academic Years)
- Fee Heads (depends on Programs)

---

## High-Risk Migrations

### Risk Level: HIGH

- **Programs**: Central to many features
- **Fee Heads**: Critical for finance operations
- **Admission Settings**: Active during admission season

### Risk Level: MEDIUM

- **Departments**: Referenced by many entities
- **Academic Years**: Time-sensitive

### Risk Level: LOW

- **Theme**: User-specific, no dependencies
- **Boards**: Rarely used

---

## Redirect Strategy

All old URLs will redirect to new locations:

```typescript
const redirects = [
  {
    source: "/settings?tab=institute",
    destination: "/setup/institute",
    permanent: false,
  },
  {
    source: "/settings?tab=departments",
    destination: "/setup/departments",
    permanent: false,
  },
  {
    source: "/settings?tab=programs",
    destination: "/setup/programs",
    permanent: false,
  },
  // ... (17 more redirects)
];
```

Redirects will be:

- **Temporary (302)** for first 4 weeks
- **Permanent (301)** after Week 9

---

## MovedFromBadge Display

All migrated pages will show a badge for 30 days:

```
┌─────────────────────────────────────────────┐
│ ℹ️ This page has moved from Settings       │
│ Old location: Settings > Programs           │
│ [Dismiss]                                   │
└─────────────────────────────────────────────┘
```

---

## Next Steps

1. ✅ Complete this audit
2. ⏳ Collect actual usage analytics
3. ⏳ Identify backend API dependencies
4. ⏳ Create migration schedule
5. ⏳ Begin Week 2 implementation
