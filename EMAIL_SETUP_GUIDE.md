# Email Setup Guide for OTP Delivery

## Current Status
- **OTPs are currently displayed in the console/terminal** where you run `python app.py`
- **OTPs are also visible in the admin panel** at `/admin-view-tokens`
- To send real emails, follow the setup below

## Quick Setup for Gmail

### Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Security → 2-Step Verification
3. Turn on 2-Step Verification

### Step 2: Generate App Password
1. Go to Google Account → Security
2. 2-Step Verification → App passwords
3. Select app: "Mail"
4. Select device: "Other" → Enter "IGNTU Placement Cell"
5. Copy the 16-character app password

### Step 3: Update app.py
Replace these lines in `app.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your-email@gmail.com',  # Replace with your Gmail
    'password': 'your-app-password',  # Replace with App Password from Step 2
    'sender_name': 'IGNTU Placement Cell'
}
```

### Step 4: Test
1. Restart your Flask app
2. Generate a student registration link
3. Check if email is sent successfully

## Alternative: Using Console/Admin Panel (Current Setup)

### For Testing/Development:
1. Generate student registration link
2. Check the **console/terminal** where you run `python app.py`
3. Or visit **Admin Dashboard → View OTPs** to see all active OTPs
4. Copy the OTP and use it in the registration form

## Other Email Providers

### Outlook/Hotmail:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp-mail.outlook.com',
    'smtp_port': 587,
    'email': 'your-email@outlook.com',
    'password': 'your-password',
    'sender_name': 'IGNTU Placement Cell'
}
```

### Yahoo Mail:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.mail.yahoo.com',
    'smtp_port': 587,
    'email': 'your-email@yahoo.com',
    'password': 'your-app-password',  # Generate app password
    'sender_name': 'IGNTU Placement Cell'
}
```

## Professional Email Services

For production use, consider:
- **SendGrid** (free tier available)
- **Mailgun** (free tier available)
- **Amazon SES** (very cheap)
- **Twilio SendGrid**

## SMS Setup (Optional)

For SMS delivery, you can integrate:
- **Twilio** (most popular)
- **AWS SNS**
- **MSG91** (Indian service)
- **TextLocal** (Indian service)

## Current Workflow (No Email Setup Needed)

1. **Admin**: Generate student link
2. **Admin**: Go to "View OTPs" in dashboard
3. **Admin**: Copy the OTP and share with student manually
4. **Student**: Use the registration link and enter the OTP
5. **Student**: Complete registration

This works perfectly for testing and small-scale use!