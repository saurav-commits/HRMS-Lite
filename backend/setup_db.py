#!/usr/bin/env python
"""
MongoDB Database Setup Script for HRMS Lite (MongoDB Atlas)
- Works without local MongoDB
- Idempotent (safe to run multiple times)
- Creates collections, indexes, and optional sample data
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# ------------------------------------------------------------------
# Environment setup
# ------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

load_dotenv()

# ------------------------------------------------------------------
# MongoDB connection
# ------------------------------------------------------------------

def check_mongodb_connection():
    try:
        mongodb_uri = os.getenv("MONGODB_URI")

        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found. Please create a .env file.")

        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")

        print("✅ Connected to MongoDB Atlas")
        return True, client, mongodb_uri

    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        return False, None, None

# ------------------------------------------------------------------
# Index creation (safe & idempotent)
# ------------------------------------------------------------------

def create_indexes(db):
    print("📌 Ensuring indexes...")

    employees = db["employees"]
    attendance = db["attendance"]

    # Employees indexes
    emp_indexes = employees.index_information()

    if "employee_id_1" not in emp_indexes:
        employees.create_index("employee_id", unique=True, name="employee_id_1")
        print("✅ Created employees.employee_id unique index")
    else:
        print("ℹ️ employees.employee_id index already exists")

    if "email_1" not in emp_indexes:
        employees.create_index("email", name="email_1")
        print("✅ Created employees.email index")
    else:
        print("ℹ️ employees.email index already exists")

    # Attendance indexes
    att_indexes = attendance.index_information()

    if "employee_1_date_1" not in att_indexes:
        attendance.create_index(
            [("employee", 1), ("date", 1)],
            unique=True,
            name="employee_1_date_1"
        )
        print("✅ Created attendance (employee + date) unique index")
    else:
        print("ℹ️ attendance (employee + date) index already exists")

    if "date_1" not in att_indexes:
        attendance.create_index("date", name="date_1")
        print("✅ Created attendance.date index")
    else:
        print("ℹ️ attendance.date index already exists")

    if "status_1" not in att_indexes:
        attendance.create_index("status", name="status_1")
        print("✅ Created attendance.status index")
    else:
        print("ℹ️ attendance.status index already exists")

# ------------------------------------------------------------------
# Sample data insertion
# ------------------------------------------------------------------

def insert_sample_data(db):
    print("🧪 Inserting sample data (DEV ONLY)...")

    employees = db["employees"]
    attendance = db["attendance"]

    # Clear existing sample data
    employees.delete_many({})
    attendance.delete_many({})

    now = datetime.utcnow()

    sample_employees = [
        {
            "employee_id": "EMP001",
            "full_name": "John Doe",
            "email": "john.doe@company.com",
            "department": "Engineering",
            "created_at": now,
            "updated_at": now
        },
        {
            "employee_id": "EMP002",
            "full_name": "Jane Smith",
            "email": "jane.smith@company.com",
            "department": "HR",
            "created_at": now,
            "updated_at": now
        },
        {
            "employee_id": "EMP003",
            "full_name": "Mike Johnson",
            "email": "mike.johnson@company.com",
            "department": "Marketing",
            "created_at": now,
            "updated_at": now
        }
    ]

    result = employees.insert_many(sample_employees)
    print(f"✅ Inserted {len(result.inserted_ids)} employees")

    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    sample_attendance = []

    for i in range(5):
        for emp_id in result.inserted_ids:
            sample_attendance.append({
                "employee": emp_id,
                "date": today - timedelta(days=i),
                "status": "Present" if random.random() > 0.2 else "Absent",
                "created_at": now,
                "updated_at": now
            })

    attendance.insert_many(sample_attendance)
    print(f"✅ Inserted {len(sample_attendance)} attendance records")

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    print("🚀 HRMS Lite - MongoDB Atlas Setup")
    print("=" * 45)

    connected, client, mongodb_uri = check_mongodb_connection()
    if not connected:
        return False

    db_name = mongodb_uri.split("/")[-1]
    db = client[db_name]

    print(f"📁 Using database: {db_name}")

    create_indexes(db)

    create_data = input("\n🤔 Create sample data? (y/n): ").strip().lower()
    if create_data == "y":
        insert_sample_data(db)

    print("\n🎉 MongoDB setup completed successfully!")
    print(f"📊 Database: {db_name}")

    client.close()
    return True

# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
