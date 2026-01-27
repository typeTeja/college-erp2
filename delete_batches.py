#!/usr/bin/env python3
"""
Delete All Academic Batches Script

This script deletes all academic batches from the database via the API.
Use this to clean up old batches before recreating them with the new structure.

Usage:
    python delete_batches.py
"""

import requests
import sys

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
# You'll need to provide your authentication token
AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def list_batches():
    """List all academic batches"""
    response = requests.get(f"{API_BASE_URL}/batches/", headers=headers)
    
    if response.status_code == 200:
        batches = response.json()
        print(f"\n📋 Found {len(batches)} batch(es):\n")
        for batch in batches:
            print(f"  ID: {batch['id']}")
            print(f"  Code: {batch['batch_code']}")
            print(f"  Name: {batch['batch_name']}")
            print(f"  Joining Year: {batch['joining_year']}")
            print(f"  Status: {batch['status']}")
            print("-" * 50)
        return batches
    else:
        print(f"❌ Error listing batches: {response.status_code}")
        print(response.text)
        return []

def delete_batch(batch_id):
    """Delete a specific batch"""
    response = requests.delete(f"{API_BASE_URL}/batches/{batch_id}", headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Successfully deleted batch ID: {batch_id}")
        return True
    else:
        print(f"❌ Error deleting batch {batch_id}: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("🗑️  Academic Batch Deletion Script")
    print("=" * 60)
    
    # List all batches
    batches = list_batches()
    
    if not batches:
        print("\n✅ No batches to delete!")
        return
    
    # Confirm deletion
    print(f"\n⚠️  WARNING: This will delete ALL {len(batches)} batch(es)!")
    print("This action cannot be undone.")
    confirm = input("\nType 'DELETE ALL' to confirm: ")
    
    if confirm != "DELETE ALL":
        print("\n❌ Deletion cancelled.")
        return
    
    # Delete all batches
    print(f"\n🗑️  Deleting {len(batches)} batch(es)...\n")
    success_count = 0
    
    for batch in batches:
        if delete_batch(batch['id']):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Deleted {success_count}/{len(batches)} batches successfully!")
    print("=" * 60)

if __name__ == "__main__":
    # Check if token is set
    if AUTH_TOKEN == "YOUR_AUTH_TOKEN_HERE":
        print("❌ Error: Please set your AUTH_TOKEN in the script first!")
        print("\nTo get your token:")
        print("1. Log in to the web app")
        print("2. Open browser DevTools (F12)")
        print("3. Go to Application > Local Storage")
        print("4. Copy the 'token' value")
        print("5. Paste it in this script where it says 'YOUR_AUTH_TOKEN_HERE'")
        sys.exit(1)
    
    main()
