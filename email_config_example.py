# Email Configuration Example
# Uncomment and configure this section in app.py when you're ready to use real email sending

"""
# Add these imports to app.py:
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add this configuration after the app initialization:
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change to your SMTP server
    'smtp_port': 587,
    'email': 'your-email@gmail.com',  # Change to your email
    'password': 'your-app-password',  # Change to your app password (use App Password for Gmail)
    'sender_name': 'IGNTU Placement Cell'
}

# Replace the send_email function with this:
def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['email'], to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

# For Gmail, you'll need to:
# 1. Enable 2-factor authentication
# 2. Generate an App Password
# 3. Use the App Password instead of your regular password
"""

# SMS Configuration Example using Twilio
"""
# Install Twilio: pip install twilio
from twilio.rest import Client

SMS_CONFIG = {
    'account_sid': 'your_twilio_account_sid',
    'auth_token': 'your_twilio_auth_token',
    'from_number': '+1234567890'  # Your Twilio phone number
}

def send_sms(phone_number, message):
    try:
        client = Client(SMS_CONFIG['account_sid'], SMS_CONFIG['auth_token'])
        
        message = client.messages.create(
            body=message,
            from_=SMS_CONFIG['from_number'],
            to=phone_number
        )
        
        print(f"SMS sent successfully. SID: {message.sid}")
        return True
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False
"""