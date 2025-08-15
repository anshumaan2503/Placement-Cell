#!/usr/bin/env python3
"""
Simple script to check MongoDB database contents
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def check_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
        
        # List all databases
        print("\n🗄️ All databases:")
        for db_name in client.list_database_names():
            print(f"  - {db_name}")
            
        # Check each database for student data
        for db_name in client.list_database_names():
            if db_name not in ['admin', 'config', 'local']:  # Skip system databases
                db = client[db_name]
                print(f"\n📁 Collections in '{db_name}' database:")
                collections = db.list_collection_names()
                if collections:
                    for coll_name in collections:
                        count = db[coll_name].count_documents({})
                        print(f"  - {coll_name}: {count} documents")
                        
                        # If this collection has documents, let's see what they look like
                        if count > 0:
                            sample_doc = db[coll_name].find_one()
                            if sample_doc and any(key in sample_doc for key in ['name', 'roll_number', 'company', 'student']):
                                print(f"    📋 Sample document structure:")
                                for key, value in sample_doc.items():
                                    print(f"      {key}: {value}")
        else:
            print("  (No collections found)")
            
        # Specifically check placement_cell database
        print(f"\n🎯 Checking 'placement_cell' database specifically:")
        try:
            db = client['placement_cell']
            collection = db['placed_students']
            
            # Check collection stats
            stats = db.command('collStats', 'placed_students')
            print(f"📊 Collection stats: {stats}")
            
            # Count documents
            count = collection.count_documents({})
            print(f"📈 Total documents in collection: {count}")
            
            # List all documents
            if count > 0:
                print("\n📋 All documents in collection:")
                for doc in collection.find():
                    print(f"  - ID: {doc.get('_id')}")
                    print(f"    Name: {doc.get('name')}")
                    print(f"    Roll Number: {doc.get('roll_number')}")
                    print(f"    Company: {doc.get('company')}")
                    print(f"    Package: {doc.get('package')} LPA")
                    print(f"    Year: {doc.get('year')}")
                    print(f"    Branch: {doc.get('branch')}")
                    print(f"    Date Added: {doc.get('date_added')}")
                    print("    ---")
            else:
                print("❌ No documents found in collection")
        except Exception as e:
            print(f"❌ Error checking placement_cell database: {e}")
            
    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("Please make sure MongoDB is running on localhost:27017")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_mongodb()
