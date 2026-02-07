> You are a **senior full-stack engineer**.
>
> I want to **prepare my ERP application for production deployment**.
>
> **Tech stack:**
>
> * Frontend: **Next.js 16.1.6 (App Router, TypeScript)**
> * Backend: **Python FastAPI**
> * Database: **PostgreSQL**
> * Cache: **Redis (optional)**
> * Storage: **MinIO**
> * Payment Gateway: **Easebuzz**
>
> The application is already working.
> **Do NOT add new features.**
>
> ### Your tasks:
>
> 1. Find and list **unused files, test files, debug code, dead routes, and duplicate logic** in both frontend and backend.
> 2. Clearly separate **safe to delete** vs **should refactor**.
> 3. Remove **unused API routes**, **unused pages/components**, and **unused database models or fields**.
> 4. Clean `package.json` and Python dependencies by removing **unused packages**.
> 5. Check Redis usage — if unused, suggest removing it.
> 6. Ensure **admin routes are not exposed to public users**.
> 7. Ensure **Easebuzz payment logic is minimal and secure**.
> 8. Clean `.env` and configs for **production readiness**.
>
> ### Output format:
>
> * Files/folders safe to delete
> * Files to refactor
> * Dependencies to remove
> * Dependencies to keep
> * Final production cleanup checklist
>
> Focus on **stability, simplicity, and safe deployment**.
