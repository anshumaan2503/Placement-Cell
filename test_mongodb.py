#!/usr/bin/env python3
"""
Test MongoDB Atlas connection
"""
from pymongo import MongoClient
import sys

# Replace this with your actual MongoDB Atlas connection string
MONGODB_URI = "mongodb+srv://testuser:testpass123@placement-cluster.twfnkpl.mongodb.net/studetsdb?retryWrites=true&w=majority"

def test_connection():
    try:
        print("🔄 Testing MongoDB Atlas connection...")
        
        # Connect to MongoDB Atlas
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command('ping')
        print("✅ MongoDB Atlas connection successful!")
        
        # Test database access
        db = client['studetsdb']
        print(f"📊 Connected to database: {db.name}")
        
        # Test collections
        collections = ['Placed', 'StudentTokens', 'OTPVerification']
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"📁 Collection '{collection_name}': {count} documents")
        
        print("🎉 All tests passed! Your MongoDB Atlas is ready!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your connection string")
        print("2. Verify username/password")
        print("3. Ensure IP is whitelisted")
        print("4. Check if cluster is running")
        return False
    
    return True

if __name__ == "__main__":
    print("🍃 MongoDB Atlas Connection Test")
    print("=" * 40)
    
    if "YOUR_PASSWORD" in MONGODB_URI:
        print("⚠️  Please update MONGODB_URI with your actual connection string!")
        sys.exit(1)
    
    test_connection()