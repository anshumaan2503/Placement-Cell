#!/usr/bin/env python3
"""
Quick email performance test for Vercel deployment
"""
import time
import smtplib
import ssl
from email.message import EmailMessage

# Your current email config
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'attechno8@gmail.com',
    'password': 'cdur zofb gwua wfur',
    'sender_name': 'IGNTU Computer Science Placement Cell'
}

def test_email_speed():
    """Test email sending speed with timing"""
    print("🚀 Testing email delivery speed...")
    
    start_time = time.time()
    
    try:
        # Create test email
        msg = EmailMessage()
        msg['Subject'] = f"Speed Test - {time.strftime('%H:%M:%S')}"
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['email']}>"
        msg['To'] = "attechno8@gmail.com"
        
        html_content = f"""
        <h2>⚡ Speed Test Email</h2>
        <p>Sent at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Test OTP: <strong>123456</strong></p>
        """
        
        msg.set_content(html_content, subtype='html')
        
        # Time the connection
        connect_start = time.time()
        context = ssl.create_default_context()
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'], timeout=30) as server:
            connect_time = time.time() - connect_start
            print(f"📡 SMTP connection: {connect_time:.2f}s")
            
            # Time TLS
            tls_start = time.time()
            server.starttls(context=context)
            tls_time = time.time() - tls_start
            print(f"🔐 TLS setup: {tls_time:.2f}s")
            
            # Time login
            login_start = time.time()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            login_time = time.time() - login_start
            print(f"🔑 Login: {login_time:.2f}s")
            
            # Time sending
            send_start = time.time()
            server.send_message(msg)
            send_time = time.time() - send_start
            print(f"📤 Send message: {send_time:.2f}s")
        
        total_time = time.time() - start_time
        print(f"\n✅ Total email time: {total_time:.2f} seconds")
        
        if total_time > 10:
            print("⚠️  Email is slow (>10s)")
            print("💡 Consider switching to SendGrid or Mailgun")
        elif total_time > 5:
            print("⚠️  Email is moderately slow (>5s)")
        else:
            print("🚀 Email speed is good!")
            
        return True
        
    except Exception as e:
        total_time = time.time() - start_time
        print(f"❌ Email failed after {total_time:.2f}s: {e}")
        return False

if __name__ == "__main__":
    test_email_speed()