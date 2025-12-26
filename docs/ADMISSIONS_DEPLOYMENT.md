# Admissions Module - Deployment & Configuration Guide

## 🚀 Quick Start

### Prerequisites
```bash
# Backend
Python 3.11+
MySQL 8.0+
pip

# Frontend
Node.js 18+
npm

# Optional
Redis (for caching - future)
```

### Installation

#### 1. Backend Setup
```bash
cd apps/api

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

#### 2. Configure Environment Variables

**Backend (.env)**:
```env
# Database
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/college_erp

# JWT
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Payment Gateway (Easebuzz)
EASEBUZZ_MERCHANT_KEY=your_merchant_key
EASEBUZZ_SALT=your_salt_key
EASEBUZZ_ENV=test  # or prod
EASEBUZZ_BASE_URL=https://testpay.easebuzz.in

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=admissions@yourcollege.edu
FROM_NAME=College ERP - Admissions
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### 3. Database Migration
```bash
cd apps/api

# Run migrations
alembic upgrade head

# Seed initial data (roles, permissions)
python scripts/seed.py
```

#### 4. Create Upload Directory
```bash
mkdir -p uploads/applications
chmod 755 uploads
```

#### 5. Start Services

**Backend**:
```bash
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd apps/web
npm install
npm run dev
```

---

## 📧 Email Configuration

### Gmail Setup (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Select "Mail" and "Other (Custom name)"
   - Copy the generated password
3. **Update .env**:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=generated-app-password
   FROM_EMAIL=your-email@gmail.com
   ```

### SendGrid Setup (Recommended for Production)

1. **Create SendGrid Account**: https://sendgrid.com
2. **Generate API Key**
3. **Update email_service.py** to use SendGrid API instead of SMTP
4. **Update .env**:
   ```env
   SENDGRID_API_KEY=your-api-key
   FROM_EMAIL=admissions@yourcollege.edu
   ```

---

## 💳 Payment Gateway Configuration

### Easebuzz Setup

1. **Create Easebuzz Account**: https://easebuzz.in
2. **Get Credentials**:
   - Login to Easebuzz Dashboard
   - Navigate to Settings → API Keys
   - Copy Merchant Key and Salt
3. **Configure Webhook**:
   - Add webhook URL: `https://your-domain.com/api/v1/admissions/payment/webhook`
   - Enable POST method
4. **Update .env**:
   ```env
   EASEBUZZ_MERCHANT_KEY=your_merchant_key
   EASEBUZZ_SALT=your_salt_key
   EASEBUZZ_ENV=test  # Change to 'prod' for production
   ```

### Testing Payment Flow

1. **Use Test Credentials** (provided by Easebuzz)
2. **Test Cards**:
   - Success: 4111111111111111
   - Failure: 4000000000000002
3. **Test Amount**: Any amount (₹1 to ₹100000)

---

## 🔐 Security Checklist

### Before Production

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update `EASEBUZZ_ENV` to `prod`
- [ ] Use production database credentials
- [ ] Enable HTTPS/SSL
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting (install slowapi)
- [ ] Enable database backups
- [ ] Set up error monitoring (Sentry)
- [ ] Review all TODO comments in code
- [ ] Test all email templates
- [ ] Test payment flow end-to-end
- [ ] Set up file upload size limits in nginx/proxy

---

## 📁 File Upload Configuration

### Local Storage (Current)
Files are stored in `uploads/applications/{application_id}/`

**Nginx Configuration** (if using):
```nginx
location /uploads/ {
    alias /path/to/project/uploads/;
    internal;  # Only serve via backend
}
```

### S3/MinIO (Recommended for Production)

1. **Install boto3**:
   ```bash
   pip install boto3
   ```

2. **Update file_upload.py**:
   ```python
   import boto3
   
   s3_client = boto3.client(
       's3',
       aws_access_key_id='your-key',
       aws_secret_access_key='your-secret',
       region_name='your-region'
   )
   ```

3. **Update .env**:
   ```env
   AWS_ACCESS_KEY_ID=your-key
   AWS_SECRET_ACCESS_KEY=your-secret
   AWS_S3_BUCKET=your-bucket
   AWS_REGION=ap-south-1
   ```

---

## 🧪 Testing

### Backend Tests
```bash
cd apps/api

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/
```

### Frontend Tests
```bash
cd apps/web

# Run tests
npm test

# E2E tests
npm run test:e2e
```

### Manual Testing Checklist

#### Quick Apply Flow
- [ ] Fill quick apply form
- [ ] Choose ONLINE payment mode
- [ ] Submit and verify email received
- [ ] Initiate payment
- [ ] Complete payment (test card)
- [ ] Verify payment success email
- [ ] Verify application status = PAID

#### Offline Payment Flow
- [ ] Fill quick apply form
- [ ] Choose OFFLINE payment mode
- [ ] Submit and verify email received
- [ ] Admin verifies offline payment
- [ ] Verify application status = PAID

#### Document Upload
- [ ] Upload valid document (PDF, JPG)
- [ ] Verify file size validation (max 5MB)
- [ ] Verify file type validation
- [ ] Admin verifies document
- [ ] Verify email notification

#### Admission Confirmation
- [ ] Complete Stage 2 form
- [ ] Upload all required documents
- [ ] Admin confirms admission
- [ ] Verify User + Student created
- [ ] Verify admission email sent
- [ ] Verify password setup link

---

## 📊 Monitoring & Logs

### Application Logs
```bash
# Backend logs
tail -f logs/app.log

# Frontend logs
npm run dev  # Check console
```

### Database Monitoring
```sql
-- Check application counts by status
SELECT status, COUNT(*) as count 
FROM application 
GROUP BY status;

-- Check payment success rate
SELECT 
    COUNT(*) as total_payments,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful,
    ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
FROM applicationpayment;

-- Check activity logs
SELECT activity_type, COUNT(*) as count
FROM applicationactivitylog
GROUP BY activity_type
ORDER BY count DESC;
```

### Error Monitoring (Sentry - Optional)

1. **Install Sentry**:
   ```bash
   pip install sentry-sdk[fastapi]
   ```

2. **Configure in main.py**:
   ```python
   import sentry_sdk
   
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       traces_sample_rate=1.0,
   )
   ```

---

## 🔄 Deployment

### Docker Deployment

**Dockerfile (Backend)**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: ./apps/api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+pymysql://user:pass@db:3306/college_erp
    volumes:
      - ./uploads:/app/uploads
    depends_on:
      - db

  web:
    build: ./apps/web
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://api:8000/api/v1

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=college_erp
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Coolify Deployment

1. **Create New Service** in Coolify
2. **Configure Build**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. **Add Environment Variables** from .env
4. **Configure Persistent Storage**:
   - Mount `/app/uploads` to persistent volume
5. **Run Migration**:
   ```bash
   alembic upgrade head
   python scripts/seed.py
   ```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Email Not Sending
```bash
# Check SMTP credentials
python3 -c "from app.services.email_service import email_service; print(email_service.smtp_user)"

# Test email
python3 scripts/test_email.py
```

#### 2. Payment Webhook Not Working
- Check webhook URL is publicly accessible
- Verify Easebuzz webhook configuration
- Check logs for webhook errors
- Ensure hash verification is working

#### 3. File Upload Fails
```bash
# Check upload directory permissions
ls -la uploads/
chmod 755 uploads/
chmod 755 uploads/applications/

# Check disk space
df -h
```

#### 4. Database Migration Fails
```bash
# Check current migration version
alembic current

# Rollback one version
alembic downgrade -1

# Re-run migration
alembic upgrade head
```

---

## 📝 API Documentation

### Access Swagger UI
```
http://localhost:8000/docs
```

### Access ReDoc
```
http://localhost:8000/redoc
```

---

## 🎯 Next Steps

1. **Week 1**: Test payment gateway with real credentials
2. **Week 2**: Implement rate limiting and CSRF protection
3. **Week 3**: Add password setup/reset flow
4. **Week 4**: Build application detail page
5. **Week 5**: Comprehensive testing and bug fixes
6. **Week 6**: Production deployment

---

## 📞 Support

For issues or questions:
- Check logs: `logs/app.log`
- Review documentation: `docs/`
- Check API docs: `http://localhost:8000/docs`

---

**Last Updated**: December 26, 2025  
**Version**: 1.0.0  
**Status**: 90% Complete - Payment & Email Ready for Testing
