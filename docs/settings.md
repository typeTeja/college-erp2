**Role:**
Act as a **Senior Full-Stack ERP Architect & UI/UX Designer** with experience building **role-based enterprise systems** for educational institutions.

---

### 📌 Objective

Design and implement a **/settings module** for a **College Management ERP** that acts as the **central control panel** for users, administrators, and super administrators.

The system must be **secure, role-aware, scalable, and audit-ready**.

---

## 🧩 Functional Scope

### 1️⃣ User Settings (ALL ROLES)

Available to: Student, Faculty, Staff, Admin, Super Admin

Build the following features:

**Profile Management**

* View: Name, Role, Employee/Student ID
* Update profile picture (with validation & preview)

**Security**

* Change password (current password verification)
* Logout from all active sessions

**Notification Preferences**

* In-app notification toggle
* Email alerts toggle (fees, attendance, approvals)
* SMS alerts toggle (LOP, emergency notices)

**Interface Preferences**

* Dark / Light mode
* Language selection (future-ready, even if single language now)

---

### 2️⃣ Institutional Settings (ADMIN & SUPER ADMIN)

Available to: Admin, Super Admin

**Institute Identity**

* Institute name
* Short code (e.g., Regency)
* Address
* Contact email & phone
* Logo upload (stored securely)

**Academic Configuration**

* Active Academic Year (lock once attendance/exams exist)
* Semester start & end dates
* Working days selection (Mon–Sat, etc.)

**Module Rules**

* Attendance:

  * Grace time (minutes)
  * Late → LOP conversion rules
* Fees:

  * Late fee per day
  * Grace period before fine
* All rule changes must support “effective from” dates

---

### 3️⃣ Integration & API Settings (SUPER ADMIN ONLY)

**Communication Gateways**

* SMS (Msg91): API key, sender ID, template mapping
* Email (Gmail API): OAuth Client ID / Secret
* Push Notifications: Firebase Cloud Messaging keys

**Payment Gateway**

* Easebuzz: Key, Salt, Environment (TEST / PROD)

**Security Rules**

* Encrypt all secrets at rest
* Mask sensitive values in UI
* Provide “Test Connection” button for each integration

---

### 4️⃣ System & Security Settings (SUPER ADMIN ONLY)

**Role Permission Matrix**

* Toggle-based permission UI
* System roles are read-only (cannot be altered/deleted)

**Audit Logs**

* Track:

  * Login events
  * Permission changes
  * Settings updates
* Filters: User / Module / Date
* CSV export support

**Maintenance Mode**

* Global ERP lock toggle
* Super Admin bypass allowed
* Maintenance message customization

---

## 🧠 Intelligence & Rules

* **Single Source of Truth**: Settings stored as encrypted key-value pairs in a `SystemSetting` table.
* **Smart Caching**: In-memory caching for high-frequency settings (Active Year, Role rules) with TTL.
* **Maker-Checker Flow**: Critical configuration changes (Active Year, API Keys) require a second Admin approval.
* **Environment-Aware**: Support for TEST/PROD environment labels for all integration keys.
* **Role-Awareness**: Render tabs dynamically based on user role; no hardcoded role checks.
* **Auditability**: Every setting change triggers a structured `AuditLog` entry.

---

## 🎨 UI / UX REQUIREMENTS

![Image](https://community.tadabase.io/uploads/default/e593f79fe16dcc074a86e56a618a8b8dbd8a483f)

![Image](https://cdn.dribbble.com/userupload/13067993/file/original-a2de980c93a97ccec36de6659feff185.png)

![Image](https://cdn.dribbble.com/userupload/4060330/file/original-e0347df781b3e4c73a2ba263ece65cf4.png?format=webp\&resize=400x300\&vertical=center)


* Vertical sidebar navigation inside `/settings`
* Card-based grouping (Profile, Security, Rules, Integrations)
* Inline validation + save status indicators
* Clean, enterprise-grade design (blue/white or neutral theme)
* Fully responsive (desktop first)

---

## 🗂️ Expected File Structure (Frontend)

```
/settings
 ├── page.tsx                // Entry point
 ├── SettingsTabs.tsx        // Role-based tab rendering
 ├── UserSettings.tsx
 ├── InstituteSettings.tsx
 ├── IntegrationSettings.tsx
 ├── SystemSecurity.tsx
 ├── components/
 │    ├── ProfileCard.tsx
 │    ├── PasswordChange.tsx
 │    ├── NotificationPrefs.tsx
 │    └── SaveStatusIndicator.tsx
```

---

## 🧪 Quality & Constraints

* No hard-coded role checks in UI
* No direct access to Super Admin settings via URL
* Secure defaults for all integrations
* Future-proof for mobile app usage
* Clean separation: UI ≠ Business Logic ≠ Persistence

---

### ✅ Final Output Expected from AI Agent

* Fully wired Settings UI (role-based)
* Secure backend APIs for settings
* Clean DB schema / key-value model
* Audit logging implemented
* Ready for production & compliance audits


