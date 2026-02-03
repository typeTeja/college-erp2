"""
Generate OpenAPI Specification

This script generates the OpenAPI spec from the FastAPI app and saves it
as a versioned JSON file for frontend integration.
"""
import sys
import os
import json
from datetime import datetime

# Ensure apps/api is in python path
api_path = os.path.join(os.getcwd(), "apps/api")
if api_path not in sys.path:
    sys.path.append(api_path)

# Mock required env vars
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "mock_secret_for_openapi_generation")
os.environ.setdefault("BACKEND_BASE_URL", "http://localhost:8000")
os.environ.setdefault("PORTAL_BASE_URL", "http://localhost:3000")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

# S3 Storage mocks
os.environ.setdefault("AWS_ACCESS_KEY_ID", "mock_access_key")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "mock_secret_key")
os.environ.setdefault("AWS_REGION", "us-east-1")
os.environ.setdefault("S3_BUCKET_NAME", "mock-bucket")
os.environ.setdefault("S3_ENDPOINT", "https://s3.amazonaws.com")

def generate_openapi_spec():
    """Generate and save OpenAPI specification"""
    print("Generating OpenAPI specification...")
    
    try:
        from app.main import app
        
        # Get OpenAPI schema
        openapi_schema = app.openapi()
        
        # Add metadata
        openapi_schema["info"]["version"] = "1.0.0"
        openapi_schema["info"]["description"] = """
College ERP System API

**Generated:** {timestamp}

**Locked Domains:**
- Admission (v1.0.0) - Contracts locked with strict validation

**Status:**
- ✅ Admission: Ready for frontend integration
- ⏳ Finance: In progress
- ⏳ Academic: In progress
- ⏳ Student: In progress

**Breaking Changes Policy:**
- Enum additions: Safe (backward compatible)
- New optional fields: Safe
- Required field changes: Requires migration + deprecation notice
- Enum removals: 6-month deprecation period
- Field type changes: Major version bump
        """.format(timestamp=datetime.utcnow().isoformat())
        
        # Save to versioned file
        output_dir = "apps/api/docs"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save versioned spec
        version = "v1.0.0"
        versioned_file = os.path.join(output_dir, f"openapi_{version}.json")
        with open(versioned_file, "w") as f:
            json.dump(openapi_schema, f, indent=2)
        
        # Save latest (symlink alternative)
        latest_file = os.path.join(output_dir, "openapi_latest.json")
        with open(latest_file, "w") as f:
            json.dump(openapi_schema, f, indent=2)
        
        print(f"✅ OpenAPI spec generated successfully!")
        print(f"   Versioned: {versioned_file}")
        print(f"   Latest: {latest_file}")
        print(f"\n📋 Spec Summary:")
        print(f"   Title: {openapi_schema['info']['title']}")
        print(f"   Version: {openapi_schema['info']['version']}")
        print(f"   Paths: {len(openapi_schema.get('paths', {}))}")
        print(f"   Schemas: {len(openapi_schema.get('components', {}).get('schemas', {}))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate OpenAPI spec: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if generate_openapi_spec():
        sys.exit(0)
    else:
        sys.exit(1)
