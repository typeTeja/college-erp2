
import asyncio
import os
import sys

# Add app to path
sys.path.append(os.getcwd())

from app.services.easebuzz_service import easebuzz_service
from app.config.settings import settings

async def debug_payment():
    print(f"DEBUG: Testing Payment Initiation")
    print(f"DEBUG: EASEBUZZ_ENV: {settings.EASEBUZZ_ENV}")
    print(f"DEBUG: BACKEND_BASE_URL: {settings.BACKEND_BASE_URL}")

    payment_data = {
        "txnid": "TEST_TXN_001",
        "amount": "1.00",
        "firstname": "Test User",
        "email": "test@example.com",
        "phone": "9999999999",
        "productinfo": "Debug Payment",
        "surl": "http://localhost:8000/api/v1/payment/response",
        "furl": "http://localhost:8000/api/v1/payment/response",
        "udf1": "1",
        "udf2": "APP123"
    }

    try:
        response = await easebuzz_service.initiate_payment(payment_data)
        print(f"DEBUG: Response: {response}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Error: {e}")

if __name__ == "__main__":
    asyncio.run(debug_payment())
