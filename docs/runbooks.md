# Operational Runbooks

## Deployment & Maintenance

### Migrations
**Policy**: Always use Alembic. Never hand-edit the schema in production.
**Strategy**:
1. Add nullable column.
2. Backfill data.
3. Make non-nullable in a separate migration.

### Backups
- **Frequency**: Daily DB dumps + Weekly offsite copy.
- **Testing**: Test restore procedure quarterly.
- **Scripts**: Located in `apps/api/scripts/`.

### Secrets Management
- Use environment variables.
- Use a secrets manager (Vault or Cloud KMS) for production.
- **Never** hardcode secrets in the codebase.

## Development Guidelines

### Code Quality
- **Static Typing**: Use `mypy` and type hints everywhere.
- **Testing**: Keep PRs small and require passing CI/CD.
- **API Responses**: Use a consistent envelope pattern.

### Security
- **PII**: Encrypt sensitive columns (Aadhaar, PAN) at the application level.
- **Audit Logs**: Log who accessed what and when.
- **Auth**: Store minimal info in secure HTTP-only cookies.

### Performance
- **File Uploads**: Use presigned S3 URLs to avoid streaming through the backend.
- **Observability**: Instrument critical endpoints (login, payments) with metrics and Sentry.

## Infrastructure
- **VPS Strategy**: Start with a single powerful VPS using Docker Compose. Split DB and workers later as needed.
- **CI/CD**: Build Image -> Run Tests -> Push Registry -> Deploy.