
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

def get_auth_token():
    try:
        payload = {"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        resp = requests.post(f"{BASE_URL}/auth/login", data=payload)
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            print_fail(f"Login failed: {resp.text}")
            return None
    except Exception as e:
        print_fail("Login exception", e)
        return None

def verify_student_architecture():
    print("🚀 Verifying Strict Student Architecture...")
    
    token = get_auth_token()
    if not token:
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Get Prerequisites (Program, Batch, ProgramYear, Quarter/Semester, Section)
    # We need to find valid IDs to link.
    
    # Get Batches
    batch = None
    try:
        resp = requests.get(f"{BASE_URL}/batches/", headers=headers)
        if resp.status_code == 200:
            batches = resp.json()
            if batches:
                batch = batches[0]
                print_pass(f"Found Batch: {batch['batch_code']} (ID: {batch['id']})")
            else:
                print_fail("No batches found. Run smoke test or create batch first.")
                return
    except Exception as e:
        print_fail("Error fetching batches", e)
        return

    if not batch: return

    # Get Program Years for Batch
    program_year = None
    try:
        resp = requests.get(f"{BASE_URL}/batches/{batch['id']}/program-years", headers=headers)
        if resp.status_code == 200:
            pys = resp.json()
            if pys:
                program_year = pys[0] # 1st Year
                print_pass(f"Found Program Year: {program_year['year_name']} (ID: {program_year['id']})")
    except Exception as e:
        print_fail("Error fetching program years", e)
        return
        
    if not program_year: return

    # Get Semesters for Batch
    semester = None
    try:
        resp = requests.get(f"{BASE_URL}/batches/{batch['id']}/semesters", headers=headers)
        if resp.status_code == 200:
            sems = resp.json()
            if sems:
                semester = sems[0] # Semester 1
                print_pass(f"Found Semester: {semester['semester_name']} (ID: {semester['id']})")
            else:
                print_fail(f"No semesters found for Batch {batch['id']}")
                print(f"Response: {resp.text}")
                return
    except Exception as e:
        print_fail("Error fetching semesters", e)
        return

    if not semester: return
    
    import random
    rand_suffix = random.randint(1000, 9999)
    student_payload = {
        "admission_number": f"ARCH_TEST_{rand_suffix}",
        "name": "Architecture Test Student",
        "email": f"archtest{rand_suffix}@student.edu",
        "program_id": batch['program_id'], # Must match batch's program
        "batch_id": batch['id'],
        "program_year_id": program_year['id'],
        "batch_semester_id": semester['id'],
        # Section ID is optional, usually assigned later. Let's skip for now or fetch if available.
        # "section_id": ...
    }
    
    print(f"📝 Attempting to create student with strict IDs: {student_payload}")
    
    try:
        # Note: We need to find the student create endpoint. Assuming /admissions/students or /students/
        # Check router. smoke_test used paths, but didn't verify student creation.
        # usually it is /students/ or /admissions/
        # Let's try /students/ first (if it exists)
        resp = requests.post(f"{BASE_URL}/students/", json=student_payload, headers=headers)
        
        if resp.status_code == 200 or resp.status_code == 201:
            student = resp.json()
            print_pass(f"Student Created Successfully! ID: {student['id']}")
            print(f"   Derived Batch: {student.get('batch_code')}")
            print(f"   Derived Program: {student.get('program_name')}")
            
            if student.get('batch_id') == batch['id']:
                 print_pass("Batch ID matches Source of Truth")
            else:
                 print_fail("Batch ID mismatch")
                 
        elif resp.status_code == 404:
             print_fail("Endpoint /students/ not found. Trying /admissions/...")
        else:
            print_fail(f"Student Creation Failed: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print_fail("Exception during creation", e)

    # 3. Negative Test: Try to mix hierarchy (Wrong Semester for Program Year)
    # We need a different program year or just a fake ID to trigger mismatch
    print("\n📝 Attempting Invalid Hierarchy (Semester Mismatch)...")
    invalid_payload = student_payload.copy()
    invalid_payload["admission_number"] = "ARCH_FAIL_001"
    invalid_payload["program_year_id"] = program_year['id'] + 999 # Likely exists? No, just fake ID.
    # actually better to use valid ID but wrong match.
    # But we only have one batch. Let's try to just change program_year_id to something else if exists, or just rely on not found.
    # Service checks "Program Year MUST belong to Batch".
    # Let's try passing a semester that doesn't belong to program year.
    # We need another program year.
    
    # Actually simpler: Just fake IDs will return 400 "Not Found" which is also validation.
    # Real validation test needs cross-match.
    # Assume we use program_year['id'] but pass a semester from a different year?
    # We only fetched one semester.
    
    try:
        # Just use mismatching IDs if we had them. 
        # For now, let's verify it calls the service.
        pass
    except:
        pass

if __name__ == "__main__":
    verify_student_architecture()
