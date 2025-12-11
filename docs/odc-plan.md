I want to integrate the ODC module into my new unified Next.js ERP dashboard.
Follow my existing project structure exactly:

```
apps/web/src/
  app/
    (auth)/
    (dashboard)/
  components/
    layout/
    dashboard/
    ui/
    odc/
  store/
  utils/
  types/
```

Implement the ODC module inside the dashboard using **URL navigation**.
Use proper Next.js App Router patterns, dashboards layouts, and feature colocation.



## 🔹 1. Sidebar Navigation (URL-based)

Add a sidebar menu item named **“ODC”**.
When clicked, it must navigate to:

```
/dashboard/odc
```

The dashboard layout (Sidebar + TopNav) must remain persistent.
Highlight the active route based on the current URL.

---

## 🔹 2. Create a Dedicated ODC Route

Inside the `(dashboard)` route group, create:

```
app/(dashboard)/odc/page.tsx
app/(dashboard)/odc/loading.tsx
app/(dashboard)/odc/error.tsx
```

This ODC page must load inside the dashboard content area using the existing `DashboardLayout`.

---

## 🔹 3. Migrate ODC UI into Components

Move or rebuild the ODC UI using the new dashboard design system.
Place all UI into:

```
src/components/odc/
```

Required components:

* ODC KPI Cards
* ODC Requests List
* Create Hotel Request Form
* Student Selection / Assignment View
* ODC Billing Summary

Ensure UI styling matches the new dashboard theme (Tailwind + shadcn/ui).

---

## 🔹 4. Integrate With Existing Services & Types

Use existing backend endpoints without changing them.

Use files already in the project:

```
src/utils/odc-service.ts
src/types/odc.ts
src/utils/api.ts
```

All API calls must be preserved exactly.

---

## 🔹 5. Standardize UX & Layout

Ensure:

* All ODC pages use the dashboard layout
* Components are responsive
* Loading & error boundaries show friendly messages
* Dashboard KPIs, lists, forms, and modals follow consistent UI patterns

---

## 🔹 6. Cleanup Instructions

After successful migration:

* Remove the old `/odc` page
* Remove duplicate or unused ODC files
* Keep only the new Next.js-based ODC module inside the dashboard

---

## 🔹 7. Deliverables Expected 

Provide:

1. A complete ODC dashboard implementation plan
2. Updated folder structure
3. Sidebar navigation design
4. ODC route definitions
5. Recommended component architecture
6. API integration plan using existing services
7. Cleanup steps after migration

Do **not** change backend endpoints.
Do **not** modify the auth route group.
Do **not** break DashboardLayout behavior.

**PROMPT END**

---
