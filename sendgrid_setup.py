# SendGrid Setup for Faster Email Delivery
# Install: pip install sendgrid

import os
import sendgrid
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(to_email, subject, body):
    """Fast email sending with SendGrid"""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        
        message = Mail(
            from_email='placement@yourdomain.com',  # Use your domain
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        
        response = sg.send(message)
        print(f"✅ SendGrid email sent: {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ SendGrid error: {e}")
        return False

# To use SendGrid:
# 1. Sign up at sendgrid.com (free tier: 100 emails/day)
# 2. Get API key from SendGrid dashboard
# 3. Add SENDGRID_API_KEY to Vercel environment variables
# 4. Replace send_email function with send_email_sendgrid