
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api/v1"
ADMIN_EMAIL = "admin@college.edu"
ADMIN_PASSWORD = "password123"

def print_pass(message):
    print(f"✅ PASS: {message}")

def print_fail(message, error=None):
    print(f"❌ FAIL: {message}")
    if error:
        print(f"   Error: {error}")

def run_smoke_test():
    print("🚀 Starting Backend Smoke Test...")
    
    # 1. Test Health/Root
    try:
        resp = requests.get("http://localhost:8000/")
        if resp.status_code == 200:
            print_pass("Root endpoint reachable")
        else:
            print_fail(f"Root endpoint returned {resp.status_code}")
    except Exception as e:
        print_fail("Root endpoint unreachable", e)
        return

    # 2. Test Login
    token = None
    try:
        payload = {
            "username": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        # Login is usually form-urlencoded or json. Let's try form-data first as it is OAuth2 standard often used in FastAPI
        resp = requests.post(f"{BASE_URL}/auth/login", data=payload)
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            if token:
                print_pass("Admin Login successful")
            else:
                print_fail("Login successful but no token returned")
        else:
            # Try JSON if form failed (though requests.post with data= does form)
            print_fail(f"Login failed with {resp.status_code}: {resp.text}")
            return
    except Exception as e:
        print_fail("Login exception", e)
        return

    if not token:
        print("🛑  Aborting tests due to login failure")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Test Dashboard Stats
    try:
        resp = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
        if resp.status_code == 200:
            print_pass("Dashboard Stats fetched")
        else:
            print_fail(f"Dashboard Stats failed {resp.status_code}")
    except Exception as e:
        print_fail("Dashboard Stats exception", e)

    # 4. Test Master Data (Programs)
    try:
        resp = requests.get(f"{BASE_URL}/master/programs-list", headers=headers)
        if resp.status_code == 200:
            programs = resp.json()
            print_pass(f"Programs List fetched ({len(programs)} items)")
        else:
            print_fail(f"Programs List failed {resp.status_code}")
    except Exception as e:
        print_fail("Programs List exception", e)

    # 5. Test Regulations
    try:
        resp = requests.get(f"{BASE_URL}/regulations/", headers=headers)
        if resp.status_code == 200:
            regulations = resp.json()
            print_pass(f"Regulations fetched ({len(regulations)} items)")
        else:
            print_fail(f"Regulations failed {resp.status_code}")
    except Exception as e:
        print_fail("Regulations exception", e)

    # 6. Test Batches
    try:
        resp = requests.get(f"{BASE_URL}/batches/", headers=headers)
        if resp.status_code == 200:
            batches = resp.json()
            print_pass(f"Batches fetched ({len(batches)} items)")
        else:
            print_fail(f"Batches failed {resp.status_code}")
            print(resp.text)
    except Exception as e:
        print_fail("Batches exception", e)
    
    print("\n🏁 Smoke Test Complete")

if __name__ == "__main__":
    run_smoke_test()
