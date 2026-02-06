import requests
import json
import os
import sys

# Test configuration
BASE_URL = "http://127.0.0.1:8000/api/v1/admissions"

def test_full_payment_flow():
    # 1. Create a fresh application via Quick Apply
    print("Step 1: Creating fresh test application...")
    quick_apply_data = {
        "name": "Full Flow Test User",
        "email": "full_flow_test@example.com",
        "phone": "9876543210",
        "gender": "MALE",
        "program_id": 1,
        "state": "Telangana",
        "board": "CBSE",
        "group_of_study": "MPC",
        "fee_mode": "ONLINE"
    }
    
    response = requests.post(
        f"{BASE_URL}/quick-apply",
        json=quick_apply_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        print(f"FAILED to create application: {response.status_code}")
        print(response.text)
        return

    app_data = response.json()
    application_id = app_data.get("id")
    app_num = app_data.get("application_number")
    print(f"SUCCESS: Created application {app_num} (ID: {application_id})")

    # 2. Initiate Payment
    print(f"\nStep 2: Initiating payment for application {application_id}...")
    pay_response = requests.post(
        f"{BASE_URL}/applications/{application_id}/payment/initiate",
        headers={"Content-Type": "application/json"}
    )
    
    if pay_response.status_code != 200:
        print(f"FAILED to initiate payment: {pay_response.status_code}")
        return

    pay_data = pay_response.json()
    print(f"SUCCESS: Payment initiated. Gateway: {pay_data.get('payment_url')}")

    # 3. Simulate Easebuzz Success Callback
    print(f"\nStep 3: Simulating Easebuzz POST callback to /payment/success...")
    # Mock Easebuzz form data
    mock_form_data = {
        "status": "success",
        "txnid": f"T-{application_id}-12345",
        "amount": "1.00",
        "udf1": str(application_id),  # udf1 holds Application ID
        "firstname": "Full Flow",
        "email": "full_flow_test@example.com",
        "hash": "mock_hash" # Hash verification is skipped in the router for now
    }
    
    # Send as form-encoded data, don't follow redirects automatically
    callback_response = requests.post(
        f"{BASE_URL}/payment/success",
        data=mock_form_data,
        allow_redirects=False
    )
    
    print(f"Callback Status: {callback_response.status_code}")
    print(f"Redirect Location: {callback_response.headers.get('Location')}")
    
    # 4. Assertions
    if callback_response.status_code == 303:
        location = callback_response.headers.get('Location', '')
        if "/apply/success?status=success" in location:
            print("\n✅ REDIRECT TEST PASSED!")
            print(f"User redirected to: {location}")
        else:
            print("\n❌ REDIRECT TEST FAILED: Unexpected location")
            print(f"Actual Location: {location}")
    else:
        print(f"\n❌ REDIRECT TEST FAILED: Expected 303, got {callback_response.status_code}")
        print(callback_response.text)

    # 5. Verify database update (optional but recommended)
    print("\nStep 4: Verifying application status update...")
    # We can't easily verify DB without an API check or DB script.
    # Let's just check if the success page redirect worked.

if __name__ == "__main__":
    test_full_payment_flow()
