#!/usr/bin/env python3
"""
Simple script to keep Render app awake by pinging it every 10 minutes
Run this on your local machine or use a service like UptimeRobot
"""

import requests
import time
import schedule

APP_URL = "https://igntu-placement-cell.onrender.com"

def ping_app():
    try:
        response = requests.get(APP_URL, timeout=30)
        if response.status_code == 200:
            print(f"✅ App is awake - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"⚠️ App responded with status {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to ping app: {e}")

# Ping every 10 minutes
schedule.every(10).minutes.do(ping_app)

if __name__ == "__main__":
    print("🚀 Starting keep-alive service...")
    print(f"📡 Pinging: {APP_URL}")
    
    # Initial ping
    ping_app()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute