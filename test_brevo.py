#!/usr/bin/env python3
"""
Brevo Email Service Test Script
Test your Brevo configuration before using it in the main application.
"""

import os
import requests
import json
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Brevo configuration
BREVO_CONFIG = {
    'api_key': os.environ.get('BREVO_API_KEY', ''),
    'api_url': 'https://api.brevo.com/v3/smtp/email',
    'sender_email': os.environ.get('SENDER_EMAIL', 'placement@yourdomain.com'),
    'sender_name': os.environ.get('SENDER_NAME', 'IGNTU Placement Cell')
}

def test_brevo_api():
    """Test Brevo API connection and send a test email"""
    
    print("🧪 Testing Brevo Email Service")
    print("=" * 50)
    
    # Check if API key is configured
    if not BREVO_CONFIG['api_key']:
        print("❌ BREVO_API_KEY not found in environment variables")
        print("💡 Please add your Brevo API key to .env file")
        return False
    
    print(f"✅ API Key configured: {BREVO_CONFIG['api_key'][:10]}...")
    print(f"📧 Sender: {BREVO_CONFIG['sender_name']} <{BREVO_CONFIG['sender_email']}>")
    
    # Get test email from user
    test_email = input("\n📮 Enter test email address: ").strip()
    if not test_email or '@' not in test_email:
        print("❌ Invalid email address")
        return False
    
    # Prepare test email
    headers = {
        'accept': 'application/json',
        'api-key': BREVO_CONFIG['api_key'],
        'content-type': 'application/json'
    }
    
    test_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #283593, #3949ab); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="margin: 0; font-size: 24px;">🎓 IGNTU Placement Cell</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Brevo Email Service Test</p>
            </div>
            
            <div style="background: white; padding: 30px; border: 1px solid #e0e0e0; border-radius: 0 0 10px 10px;">
                <h2 style="color: #283593; margin-top: 0;">✅ Email Service Working!</h2>
                
                <p style="font-size: 16px; margin-bottom: 25px;">
                    Congratulations! Your Brevo email service is configured correctly and working perfectly.
                </p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #283593; margin-top: 0;">📊 Test Details</h3>
                    <p><strong>Service:</strong> Brevo API</p>
                    <p><strong>Sender:</strong> {BREVO_CONFIG['sender_name']}</p>
                    <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Status:</strong> ✅ Successfully Delivered</p>
                </div>
                
                <div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h4 style="color: #155724; margin-top: 0;">
                        🎉 Ready for Production!
                    </h4>
                    <p style="color: #155724; margin: 0;">
                        Your placement cell application can now send professional emails to students for registration links, OTPs, and notifications.
                    </p>
                </div>
                
                <div style="border-top: 2px solid #e0e0e0; padding-top: 20px; margin-top: 30px;">
                    <p style="color: #666; font-size: 14px; margin: 0;">
                        <strong>Next Steps:</strong><br>
                        • Your application is ready to send real emails<br>
                        • Monitor delivery in your Brevo dashboard<br>
                        • Check email analytics and performance
                    </p>
                </div>
            </div>
            
            <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
                <p style="margin: 0;">© 2025 Department of Computer Science, IGNTU. All rights reserved.</p>
            </div>
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
                'name': test_email.split('@')[0]
            }
        ],
        'subject': '🧪 Brevo Email Service Test - IGNTU Placement Cell',
        'htmlContent': test_html
    }
    
    print(f"\n🚀 Sending test email to {test_email}...")
    
    try:
        response = requests.post(BREVO_CONFIG['api_url'], headers=headers, json=payload, timeout=30)
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Email sent successfully!")
            print(f"📧 Message ID: {result.get('messageId', 'N/A')}")
            print("\n🎉 Brevo integration is working perfectly!")
            print("💡 Check your email inbox (and spam folder) for the test message")
            return True
        else:
            print(f"❌ Failed to send email")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - check your internet connection")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_brevo_account():
    """Check Brevo account information"""
    
    if not BREVO_CONFIG['api_key']:
        print("❌ API key not configured")
        return
    
    headers = {
        'accept': 'application/json',
        'api-key': BREVO_CONFIG['api_key']
    }
    
    try:
        # Get account info
        response = requests.get('https://api.brevo.com/v3/account', headers=headers, timeout=10)
        
        if response.status_code == 200:
            account = response.json()
            print("\n📊 Brevo Account Information:")
            print(f"   Email: {account.get('email', 'N/A')}")
            print(f"   Company: {account.get('companyName', 'N/A')}")
            print(f"   Plan: {account.get('plan', [{}])[0].get('type', 'N/A')}")
            
            # Get email statistics
            stats_response = requests.get('https://api.brevo.com/v3/smtp/statistics/aggregatedReport', headers=headers, timeout=10)
            if stats_response.status_code == 200:
                stats = stats_response.json()
                print(f"   Emails sent today: {stats.get('requests', 0)}")
                print(f"   Delivered: {stats.get('delivered', 0)}")
        else:
            print(f"❌ Failed to get account info: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking account: {e}")

if __name__ == "__main__":
    print("🎯 Brevo Email Service Test")
    print("This script will test your Brevo configuration\n")
    
    # Check account first
    check_brevo_account()
    
    # Run the test
    success = test_brevo_api()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Your Brevo integration is ready!")
        print("🚀 Your placement cell app can now send emails!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Test failed. Please check your configuration.")
        print("📖 See BREVO_SETUP_GUIDE.md for help")
        print("=" * 50)