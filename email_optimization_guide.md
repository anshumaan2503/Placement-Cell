# Email Delivery Optimization Guide

## Current Issue
Vercel deployment is experiencing slow email delivery times when sending registration links.

## Quick Solutions

### 1. Use SendGrid (Recommended)
SendGrid is faster and more reliable for transactional emails:

```python
# Install: pip install sendgrid
import sendgrid
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    
    message = Mail(
        from_email='placement@yourdomain.com',
        to_emails=to_email,
        subject=subject,
        html_content=body
    )
    
    try:
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False
```

### 2. Optimize Current Gmail Setup

Add these optimizations to your current `send_email` function:

```python
# Add timeout settings
with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=30) as server:
    server.sock.settimeout(30)  # Socket timeout
    server.starttls(context=context)
    server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
    server.send_message(msg)
```

### 3. Use Vercel Environment Variables
Ensure your email credentials are set in Vercel dashboard:
- SMTP_SERVER=smtp.gmail.com
- SMTP_PORT=587
- EMAIL_ADDRESS=your-email@gmail.com
- EMAIL_PASSWORD=your-app-password

### 4. Gmail App Password Check
1. Go to Google Account settings
2. Security → 2-Step Verification
3. App passwords → Generate new password
4. Use the 16-character password (not your regular Gmail password)

### 5. Alternative SMTP Servers
Try these faster SMTP options:

**Outlook/Hotmail:**
- Server: smtp-mail.outlook.com
- Port: 587

**Yahoo:**
- Server: smtp.mail.yahoo.com
- Port: 587

## Immediate Debugging Steps

1. Check Vercel function logs for timeout errors
2. Test email locally vs on Vercel
3. Monitor Gmail quota limits (500 emails/day for free accounts)
4. Check if emails are going to spam folder

## Performance Monitoring

Add timing to your email function:
```python
import time
start_time = time.time()
# ... email sending code ...
end_time = time.time()
print(f"Email took {end_time - start_time:.2f} seconds")
```