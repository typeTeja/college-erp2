#!/usr/bin/env python3
"""
Check PostgreSQL database for institute_info table
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.institute import InstituteInfo

def check_institute_info():
    """Check institute_info table"""
    print("=" * 60)
    print("Checking institute_info table in PostgreSQL...")
    print("=" * 60)
    
    with Session(engine) as session:
        # Check if any records exist
        institutes = session.exec(select(InstituteInfo)).all()
        
        if not institutes:
            print("\n❌ No institute records found in database")
            print("\nThe table exists but is EMPTY.")
            return False
        else:
            print(f"\n✅ Found {len(institutes)} institute record(s)")
            print("\nInstitute Information:")
            print("-" * 60)
            for inst in institutes:
                print(f"ID: {inst.id}")
                print(f"Name: {inst.name}")
                print(f"Short Code: {inst.short_code}")
                print(f"Address: {inst.address}")
                print(f"Contact Email: {inst.contact_email}")
                print(f"Contact Phone: {inst.contact_phone}")
                print(f"Logo URL: {inst.logo_url}")
                print("-" * 60)
            return True

if __name__ == "__main__":
    check_institute_info()
