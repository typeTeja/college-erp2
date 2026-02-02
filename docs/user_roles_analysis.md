# User Roles Analysis: College ERP System

This document provides a consolidated list and description of all user roles identified within the system. These roles are used to control access to different modules and functionalities.

## 1. Core System Roles
These are the foundational roles used for general system access and user classification.

| Role Name | Description | Source |
| :--- | :--- | :--- |
| **SUPER_ADMIN** | Full system access, can manage all entities including roles and configurations. | System Initialization |
| **ADMIN** | High-level administrative access for daily operations. | System Initialization |
| **FACULTY** | Academic staff (Lecturers, Professors) who manage courses, attendance, and internal marks. | System Initialization |
| **STUDENT** | Registered students and applicants (post-payment). | System Initialization |
| **PARENT** | Parents or guardians of students for monitoring progress and fees. | System Initialization |
| **STAFF** | Non-academic administrative staff. | System Initialization |

## 2. Specialized Administrative & Functional Roles
These roles are used for specific departmental functions and are often seeded for various college units.

| Role Name | Primary Responsibility | Source |
| :--- | :--- | :--- |
| **PRINCIPAL** | Executive oversight and high-level dashboard access. | Seed Data |
| **ADMISSION_OFFICER** | Manages the student admission pipeline and document verification. | Seed Data |
| **ACCOUNTS** | Handles fee management, financial reporting, and payment verification. | Seed Data |
| **EXAM_CELL** | Manages exam schedules, hall tickets, and university/internal results. | Seed Data |
| **LIBRARIAN** | Manages books, issues, returns, and library fines. | Seed Data |
| **WARDEN** | Manages hostel blocks, room allocations, gate passes, and complaints. | Seed Data |
| **ODC_COORDINATOR** | Manages "On-Duty-Catering" student placements at partner hotels. | Seed Data |
| **SSE** | Student Support Executive for handling student grievances and services. | Seed Data |
| **SECURITY** | Manages gate access, entry logs, and campus security. | Seed Data |

## 3. Role Management and Extensibility
The system utilizes a flexible **Role-Based Access Control (RBAC)** architecture:
- **Dynamic Roles**: New roles can be created via the API (`/api/v1/roles/`).
- **Permission Mapping**: Each role can be assigned a granular set of permissions (e.g., `list_students`, `create_invoice`, `generate_hall_ticket`).
- **Audit Logs**: Changes to role-permission mappings are recorded in the `PermissionAuditLog` for security.

## 4. Key Notes on Specific Modules
- **Admissions**: As noted in the `application_analysis.md`, applicants are assigned the `STUDENT` role after their initial payment to allow portal access.
- **Faculty/Staff**: While there are `Faculty` and `Staff` models, they are linked to `User` accounts that carry the respective `FACULTY` or `STAFF` roles.
