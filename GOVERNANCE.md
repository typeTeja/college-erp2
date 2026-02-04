# Frontend Architecture Governance

This document establishes the rules and processes for maintaining the integrity of the College ERP frontend architecture.

**Last Updated:** February 2026
**Owner:** Frontend Architecture Team

---

## 1. Dashboard Contracts (IMMUTABLE)

The 7 core dashboards have strictly defined purposes that must not valid. See `dashboard-contracts.ts` for technical definitions.

| Dashboard       | Allowed Purpose                                   | Forbidden Content                               |
| --------------- | ------------------------------------------------- | ----------------------------------------------- |
| **Principal**   | High-level trends, financial overview, compliance | Operational details, individual student records |
| **Parent**      | My children's progress, fees, attendance          | Other students' data, staff features            |
| **Student**     | My timetable, marks, assignments                  | Administrative functions, other students' data  |
| **Applicant**   | Application progress, document upload             | Enrolled student features (timetable, exams)    |
| **Faculty**     | My classes, attendance marking, grading           | Financial management, system settings           |
| **Staff**       | Role-specific tasks (Library, Hostel, Accounts)   | Academic management (unless authorized)         |
| **Super Admin** | System configuration, user management             | none                                            |

**Rule 1.1:** Do not add a widget to a dashboard unless it explicitly serves the dashboard's defined purpose.
**Rule 1.2:** Never bypass `DashboardShell` layout or `contract.validate()` checks.

---

## 2. Navigation Structure (Max Depth 2)

The navigation system uses a strict 4-layer taxonomy.

- **Setup**: One-time institutional configuration (e.g., Institute Profile)
- **Config**: Domain-specific settings (e.g., Fee Structure, Academic Year)
- **System**: Technical administration (e.g., Audit Logs, Integrations)
- **Profile**: Personal user settings (e.g., Password, Preferences)

**Rule 2.1:** Maximum navigation depth is 2 levels (Group -> Item).
**Rule 2.2:** All navigation items must be defined in `navigation.ts`. Single source of truth.
**Rule 2.3:** Do not create ad-hoc links or sidebars outside the central configuration.

---

## 3. Component Library & UX

We follow specific UX laws to ensure consistency.

- **Fitts's Law**: clickable elements must be large enough. Use standard button sizes.
- **Hick's Law**: Minimize choices. Use progressive disclosure for complex forms.
- **Jakob's Law**: Use standard patterns. Don't reinvent the wheel.

**Rule 3.1:** Use `shadcn/ui` components for all standard elements.
**Rule 3.2:** All destructive actions must use `ConfirmDialog`.
**Rule 3.3:** All empty states must use `EmptyState`.
**Rule 3.4:** All async data loading must use `LoadingState` or specific skeletons.

---

## 4. Change Management Process

To modify the architecture (e.g., add a new dashboard or navigation group):

1. **Proposal**: Create an Architecture Decision Record (ADR) explaining the need.
2. **Review**: Architecture team reviews against core principles.
3. **Approval**: Must be approved by Lead Frontend Engineer.
4. **Implementation**: Update `GOVERNANCE.md` if rules change.

---

## 5. Code Review Checklist

Reviewers must check:

- [ ] Does this match the dashboard contract?
- [ ] Is the navigation depth <= 2?
- [ ] Are UI components used correctly?
- [ ] Are feature flags used for risky changes?
- [ ] Are type definitions updated?

---

**Violations of these rules will result in PR rejection.**
