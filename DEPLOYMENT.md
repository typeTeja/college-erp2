# College ERP - Coolify Deployment Guide (Nixpacks)

This guide will help you deploy the College ERP system to your VPS using **Coolify** and **Nixpacks**.

## Prerequisites

- A VPS with Coolify installed.
- **Remote MySQL database** (version 8.0 or higher recommended).
- GitHub repository with the code.

## Coolify Setup

Coolify uses Nixpacks to automatically detect and build your application. For this monorepo, you will create two separate services in Coolify.

### 1. Backend API Service (`apps/api`)

1.  **Create a New Resource**: Select "Public Repository" or "Private Repository" and point to your repo.
2.  **Base Directory**: Set to `apps/api`.
3.  **Build Pack**: Select `nixpacks`.
4.  **Environment Variables**:
    ```env
    DATABASE_URL=mysql+pymysql://user:password@host:3306/college_erp
    SECRET_KEY=your_secure_random_key
    ALGORITHM=HS256
    ```
5.  **Exposed Port**: 8000.
6.  **Domains**: Set your API domain (e.g., `api.yourdomain.com`).

### 2. Frontend Web Service (`apps/web`)

1.  **Create a New Resource**: Point to the same repository.
2.  **Base Directory**: Set to `apps/web`.
3.  **Build Pack**: Select `nixpacks`.
4.  **Install Command**: `npm install`.
5.  **Build Command**: `npm run build`.
6.  **Start Command**: `npm start`.
7.  **Environment Variables**:
    ```env
    NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    ```
8.  **Exposed Port**: 3000.
9.  **Domains**: Set your main domain (e.g., `yourdomain.com`).

---

## Database Migrations

Since Nixpacks builds are ephemeral, you should run migrations manually after the first deployment or as part of your CI/CD.

To run migrations via Coolify:
1.  Go to the API service **Terminal**.
2.  Run:
    ```bash
    alembic upgrade head
    ```

To seed initial data (optional):
1.  Run:
    ```bash
    python scripts/seed.py
    ```

---

## Troubleshooting

- **Build Failures**: Check the Coolify deployment logs. Nixpacks usually provides clear error messages if a dependency is missing.
- **CORS Issues**: Ensure `NEXT_PUBLIC_API_URL` is correctly set in the Web service and that the API service allows that origin.
- **MySQL Connection**: Ensure your MySQL server allows connections from the Coolify server's IP.

---

## Maintenance

### Update Application
Coolify handles updates automatically when you push to the configured branch. You can also manually trigger a redeploy in the Coolify dashboard.

### Backup
Regularly backup your remote MySQL database. Coolify can also manage database backups if you host the MySQL database within Coolify.
