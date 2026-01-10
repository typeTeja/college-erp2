#!/usr/bin/env python3
"""
Seed initial institute information
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.institute import InstituteInfo

def seed_institute():
    """Create initial institute information"""
    print("=" * 60)
    print("Seeding Institute Information...")
    print("=" * 60)
    
    with Session(engine) as session:
        # Check if institute info already exists
        existing = session.exec(select(InstituteInfo)).first()
        
        if existing:
            print(f"\n✅ Institute info already exists: {existing.name}")
            print("Skipping seed.")
            return
        
        # Create initial institute info based on seed_settings.py
        institute = InstituteInfo(
            name="Regency College of Hotel Management",
            short_code="RCHM",
            address="Hyderabad, Telangana",
            contact_email="info@rchm.edu",
            contact_phone="+91-XXX-XXX-XXXX",
            logo_url=""
        )
        
        session.add(institute)
        session.commit()
        session.refresh(institute)
        
        print("\n✅ Institute information created successfully!")
        print(f"\nID: {institute.id}")
        print(f"Name: {institute.name}")
        print(f"Short Code: {institute.short_code}")
        print(f"Address: {institute.address}")
        print(f"Contact Email: {institute.contact_email}")
        print(f"Contact Phone: {institute.contact_phone}")
        print("\n⚠️  Please update the contact details through the Settings page.")

if __name__ == "__main__":
    seed_institute()
