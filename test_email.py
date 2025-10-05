#!/usr/bin/env python3
"""
Test email sending functionality
"""
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime

# Your Gmail credentials
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'attechno8@gmail.com',
    'password': 'cdur zofb gwua wfur',
    'sender_name': 'IGNTU Computer Science Placement Cell'
}

def test_email_sending():
    try:
        print("🔄 Testing email sending...")
        print(f"📧 Using email: {EMAIL_CONFIG['email']}")
        print(f"🔑 Using password: {EMAIL_CONFIG['password'][:4]}****{EMAIL_CONFIG['password'][-4:]}")
        
        # Create test email
        msg = EmailMessage()
        msg['Subject'] = "Test Email from Placement Cell - " + str(datetime.now())
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = "attechno8@gmail.com"  # Send to yourself for testing
        
        # Simple HTML content
        html_content = """
        <h2>🎉 Email Test Successful!</h2>
        <p>Your placement cell email system is working correctly.</p>
        <p><strong>Test OTP:</strong> 123456</p>
        """
        
        msg.set_content(html_content, subtype='html')
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls(context=context)
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            server.send_message(msg)
        
        print("✅ Email sent successfully!")
        print("📧 Check your inbox: attechno8@gmail.com")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        print("\n🔧 Possible solutions:")
        print("1. Check Gmail App Password")
        print("2. Enable 2-Factor Authentication")
        print("3. Generate new App Password")
        print("4. Check Gmail security settings")
        return False

if __name__ == "__main__":
    print("📧 Gmail Email Test")
    print("=" * 40)
    test_email_sending()