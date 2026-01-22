# Email & SMS Configuration Guide

## Email Configuration (Google Workspace)

The application uses Google Workspace SMTP for sending emails. Add the following to your `.env` file:

```env
# Email Configuration (Google Workspace)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@yourdomain.com
SMTP_PASSWORD=your-app-specific-password
FROM_EMAIL=admissions@yourdomain.com
FROM_NAME=College ERP - Admissions
```

### Setting up Google Workspace App Password:

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Scroll to "App passwords"
4. Generate a new app password for "Mail"
5. Use this password in `SMTP_PASSWORD`

## SMS Configuration (MSG91)

The application uses MSG91 for sending SMS notifications. Add the following to your `.env` file:

```env
# SMS Configuration (MSG91)
MSG91_AUTH_KEY=your-msg91-auth-key
MSG91_SENDER_ID=COLEGE
MSG91_ROUTE=4
MSG91_COUNTRY_CODE=91
```

### Setting up MSG91:

1. Sign up at [https://msg91.com](https://msg91.com)
2. Get your Auth Key from Dashboard → API
3. Create a Sender ID (6 characters, e.g., "COLEGE")
4. Get it approved by MSG91 (usually takes 1-2 business days)
5. Use Route 4 for transactional SMS

### MSG91 Configuration Details:

- **Auth Key**: Found in MSG91 Dashboard under API section
- **Sender ID**: 6-character alphanumeric ID (must be approved)
- **Route**: 
  - `1` - Promotional
  - `4` - Transactional (recommended for OTP and credentials)
- **Country Code**: `91` for India

## Testing Email/SMS

### Test Email:
```python
from app.services.email_service import email_service

email_service.send_portal_credentials(
    to_email="test@example.com",
    name="Test User",
    application_number="APP2026001",
    username="test123",
    password="Test@123",
    portal_url="https://portal.college.edu"
)
```

### Test SMS:
```python
from app.services.sms_service import sms_service

sms_service.send_portal_credentials(
    mobile="9876543210",
    name="Test User",
    username="test123",
    password="Test@123",
    application_number="APP2026001"
)
```

## Admission Settings Configuration

Configure notification preferences in the Admin Settings UI:

1. Login as Admin
2. Go to Settings → Admission Settings
3. Configure:
   - Enable/Disable Application Fee
   - Set Fee Amount
   - Toggle Online/Offline Payment
   - **Enable Email Notifications** (recommended)
   - **Enable SMS Notifications** (optional, requires MSG91 setup)
   - Set Portal Base URL

## Troubleshooting

### Email Issues:
- **Authentication Failed**: Check if App Password is correct
- **Connection Timeout**: Verify SMTP_HOST and SMTP_PORT
- **Emails in Spam**: Add SPF/DKIM records to your domain

### SMS Issues:
- **Invalid Auth Key**: Verify MSG91_AUTH_KEY is correct
- **Sender ID Not Approved**: Wait for MSG91 approval or use default sender
- **SMS Not Delivered**: Check mobile number format (should be 10 digits without country code)
- **Rate Limiting**: MSG91 has rate limits, check your plan

## Production Checklist

- [ ] Configure Google Workspace SMTP credentials
- [ ] Test email delivery
- [ ] Set up MSG91 account
- [ ] Get Sender ID approved
- [ ] Test SMS delivery
- [ ] Configure Admission Settings in UI
- [ ] Set correct Portal Base URL
- [ ] Test complete Quick Apply flow
- [ ] Monitor email/SMS logs for failures
