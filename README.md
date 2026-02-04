# College ERP - Frontend Architecture

This repository contains the Next.js frontend application for the College ERP system.

## 🚀 Architecture Overview (New 2026)

The frontend has undergone a complete architectural overhaul to support role-based dashboards, strict governance, and scalable navigation.

### Core Principles

1.  **Role-Based Dashboards**: 7 distinct dashboards (Principal, Parent, Student, etc.) with immutable contracts.
2.  **Strict Navigation**: A 4-layer taxonomy (Setup, Config, System, Profile) with max-depth of 2.
3.  **Governance**: All changes must adhere to `GOVERNANCE.md` rules.

### Directory Structure

```
apps/web/
├── src/
│   ├── app/
│   │   ├── (dashboard)/       # Main authenticated layout
│   │   │   ├── principal/     # Principal dashboard
│   │   │   ├── parent/        # Parent dashboard
│   │   │   ├── student/       # Enrolled student dashboard
│   │   │   └── ...            # Other role dashboards
│   │   └── setup/             # Institutional setup pages
│   ├── components/
│   │   ├── navigation/        # New GroupedSidebar & CommandPalette
│   │   └── widgets/           # Dashboard-specific widgets
│   ├── config/
│   │   ├── feature-flags.ts   # Rollout control
│   │   └── navigation.ts      # Single source of truth for nav
│   └── store/                 # Zustand stores (Auth, etc.)
```

## 🛠 Features

- **Command Palette**: `Cmd+K` global search with aliases.
- **Permanent Redirects**: Legacy paths automatically redirect to new structure.
- **Performance Optimized**: Lazy loaded widgets, react-query caching (5m stale time).
- **Accessibility**: ARIA compliant, keyboard navigable.

## 🚦 Governance

See [GOVERNANCE.md](./GOVERNANCE.md) for detailed rules on:

- Adding new widgets
- Modifying navigation
- Code review checklists

## 📦 Tech Stack

- **Framework**: Next.js 14
- **UI**: Tailwind CSS + Shadcn/UI
- **State**: Zustand + TanStack Query
- **Icons**: Lucide React

## 🏃‍♂️ Getting Started

```bash
npm install
npm run dev
```

The application will start at `http://localhost:3000`.
