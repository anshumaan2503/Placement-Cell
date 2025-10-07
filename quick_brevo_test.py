#!/usr/bin/env python3
"""
Quick Brevo Test - No user input required
"""

import os
import requests
import json

# Brevo configuration - Load from environment variables
import os
from dotenv import load_dotenv
load_dotenv()

BREVO_CONFIG = {
    'api_key': os.environ.get('BREVO_API_KEY', ''),
    'api_url': 'https://api.brevo.com/v3/smtp/email',
    'sender_email': os.environ.get('SENDER_EMAIL', 'your-email@domain.com'),
    'sender_name': os.environ.get('SENDER_NAME', 'IGNTU Computer Science Placement Cell')
}

def test_brevo_quick():
    """Quick test of Brevo API"""
    
    print("🧪 Quick Brevo Test")
    print("=" * 30)
    
    # Test with sender email
    test_email = BREVO_CONFIG['sender_email']
    
    headers = {
        'accept': 'application/json',
        'api-key': BREVO_CONFIG['api_key'],
        'content-type': 'application/json'
    }
    
    test_html = """
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h1 style="color: #283593;">🎉 Brevo Working!</h1>
            <p>Your Brevo email service is configured correctly.</p>
            <div style="background: #f0f8ff; padding: 15px; border-radius: 5px;">
                <p><strong>✅ API Key:</strong> Valid</p>
                <p><strong>✅ Sender:</strong> IGNTU Computer Science Placement Cell</p>
                <p><strong>✅ Status:</strong> Ready for production!</p>
            </div>
            <p>Your placement cell app can now send professional emails!</p>
        </div>
    </body>
    </html>
    """
    
    payload = {
        'sender': {
            'name': BREVO_CONFIG['sender_name'],
            'email': BREVO_CONFIG['sender_email']
        },
        'to': [
            {
                'email': test_email,
                'name': 'Test User'
            }
        ],
        'subject': '✅ Brevo Test - IGNTU Placement Cell Working!',
        'htmlContent': test_html
    }
    
    print(f"🚀 Sending test email to {test_email}...")
    
    try:
        response = requests.post(BREVO_CONFIG['api_url'], headers=headers, json=payload, timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print("✅ SUCCESS! Email sent via Brevo API")
            print(f"📧 Message ID: {result.get('messageId', 'N/A')}")
            print("\n🎉 Your Brevo integration is working perfectly!")
            print("📧 Check your email inbox for the test message")
            print("\n🚀 Your placement cell app is ready to send emails!")
            return True
        else:
            print(f"❌ Failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_brevo_quick()