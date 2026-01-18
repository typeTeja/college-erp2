"""Fix NULL discount_value in scholarship_slab table"""
from sqlmodel import Session, select
from app.db.session import engine
from app.models.master_data import ScholarshipSlab
from decimal import Decimal

def fix_null_discount_values():
    with Session(engine) as session:
        # Get all scholarship slabs with NULL discount_value
        stmt = select(ScholarshipSlab)
        slabs = session.exec(stmt).all()
        
        updated_count = 0
        for slab in slabs:
            if slab.discount_value is None:
                print(f"Updating slab: {slab.name} (ID: {slab.id})")
                slab.discount_value = Decimal("0.00")
                session.add(slab)
                updated_count += 1
        
        if updated_count > 0:
            session.commit()
            print(f"\n✅ Updated {updated_count} scholarship slabs with NULL discount_value")
        else:
            print("✅ No scholarship slabs with NULL discount_value found")
        
        # Verify the fix
        print("\nCurrent scholarship slabs:")
        slabs = session.exec(select(ScholarshipSlab)).all()
        for slab in slabs:
            print(f"  - {slab.name}: discount_value = {slab.discount_value}")

if __name__ == "__main__":
    fix_null_discount_values()
