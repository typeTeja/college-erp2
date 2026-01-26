import sys
import os

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.db.session import engine
from app.models.admissions import Application

def check_status(app_number):
    with Session(engine) as session:
        statement = select(Application).where(Application.application_number == app_number)
        app = session.exec(statement).first()
        
        if not app:
            print(f"Application {app_number} NOT FOUND.")
            return

        print(f"--- Status for {app_number} ---")
        print(f"ID: {app.id}")
        print(f"Name: {app.name}")
        print(f"Status: {app.status}")
        print(f"Payment Status: {app.payment_status}")
        print(f"Fee Mode: {app.fee_mode}")
        print(f"Offline Verified: {app.offline_payment_verified}")
        print(f"Application Fee: {app.application_fee}")
        
        if app.payments:
            print("\nPayments:")
            for p in app.payments:
                print(f" - Transaction: {p.transaction_id}, Status: {p.status}, Amount: {p.amount}")
        else:
            print("\nNo payment records found.")

if __name__ == "__main__":
    check_status("APP202600034")
