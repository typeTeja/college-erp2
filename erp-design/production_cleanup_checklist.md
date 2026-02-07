# Production Cleanup Checklist

## Security
- [x] Admin routes secured with `get_current_active_superuser`
- [x] Unused debug scripts deleted
- [x] Payment hash verification logic verified
- [ ] SSL/TLS enabled (Infrastructure level)
- [ ] Database backups configured

## Performance
- [x] Unused dependencies (`pandas`, `qrcode`) removed
- [x] Unused files deleted
- [ ] Redis caching enabled (Optional)
- [ ] Database indexing reviewed (Future task)

## Configuration
- [ ] `.env` updated for production (Set `ENVIRONMENT=production`)
- [ ] `SECRET_KEY` rotated and secured
- [ ] `BACKEND_BASE_URL` and `PORTAL_BASE_URL` set to HTTPS domains
- [ ] CORS origins restricted to production domains

## Deployment
- [ ] Build process verified (Frontend & Backend)
- [ ] Database migrations applied using `alembic upgrade head`
