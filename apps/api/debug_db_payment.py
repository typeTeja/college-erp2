
import asyncio
import os
import sys
from sqlmodel import Session, select

# Add app to path
sys.path.append(os.getcwd())

from app.db.session import engine
from app.models.admissions import Application
from app.services.easebuzz_service import easebuzz_service
from app.schemas.easebuzz import PaymentInitiateRequest
from app.api.v1.easebuzz import initiate_payment as api_initiate_payment

async def debug_real_payment():
    print(f"DEBUG: Testing Payment with Application 19")
    
    with Session(engine) as session:
        app_id = 19
        application = session.get(Application, app_id)
        
        if not application:
            print(f"ERROR: Application {app_id} not found")
            return

        print(f"DEBUG: Found Application: {application.name}, {application.email}, {application.phone}")
        print(f"DEBUG: App Fee: {application.application_fee}")

        # Construct payload like the Frontend would
        # The frontend sends: application_id, amount
        request = PaymentInitiateRequest(
            application_id=app_id,
            amount=application.application_fee
        )
        
        try:
            # We can't easily call the API function directly because it relies on Depends()
            # So we mimic the logic inside initiate_payment
            
            # 1. Prepare data
            payment_data = {
                "txnid": "DEBUG_TXN_" + str(app_id),
                "amount": request.amount,
                "firstname": application.name,
                "email": application.email,
                "phone": application.phone,
                "productinfo": f"Application Fee for {application.application_number}",
                "udf1": str(application.id),
                "udf2": application.application_number,
                "surl": None,
                "furl": None
            }
            
            print(f"DEBUG: Calling easebuzz_service.initiate_payment with: {payment_data}")
            
            response = await easebuzz_service.initiate_payment(payment_data)
            print(f"DEBUG: Service Response: {response}")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(debug_real_payment())
