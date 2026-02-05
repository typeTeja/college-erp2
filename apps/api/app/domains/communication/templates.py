"""
Email and SMS templates for the communication domain.
"""

PORTAL_CREDENTIALS_EMAIL_SUBJECT = "Welcome to College ERP - Your Portal Credentials"

PORTAL_CREDENTIALS_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ width: 80%; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ padding: 20px; }}
        .credentials {{ background-color: #f9f9f9; padding: 15px; border-left: 5px solid #4CAF50; margin: 20px 0; }}
        .footer {{ font-size: 0.8em; color: #777; margin-top: 20px; text-align: center; }}
        .button {{ display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Welcome to College ERP</h2>
        </div>
        <div class="content">
            <p>Dear {name},</p>
            <p>Your application fee payment has been successfully processed. An account has been created for you to access the admission portal.</p>
            <p>You can use the following credentials to log in and complete your application form:</p>
            
            <div class="credentials">
                <p><strong>Portal URL:</strong> <a href="{portal_url}">{portal_url}</a></p>
                <p><strong>Username:</strong> {username}</p>
                <p><strong>Password:</strong> {password}</p>
            </div>
            
            <p>Please log in and modify your password after your first login.</p>
            
            <p style="text-align: center;">
                <a href="{portal_url}" class="button">Login to Portal</a>
            </p>
            
            <p>If you have any questions, please contact the admissions office.</p>
        </div>
        <div class="footer">
            <p>&copy; {year} College Management System. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
"""

PORTAL_CREDENTIALS_SMS_TEMPLATE = "Dear {name}, your portal account for College ERP has been created. Username: {username}, Password: {password}. Login here: {portal_url}"
