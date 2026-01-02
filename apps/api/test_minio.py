"""Test script for MinIO connection"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

# Load environment variables
load_dotenv()

def test_minio_connection():
    """Test MinIO connection and basic operations"""
    
    print("=" * 60)
    print("MinIO Connection Test")
    print("=" * 60)
    
    # Get configuration from environment
    endpoint = os.getenv('S3_ENDPOINT')
    access_key = os.getenv('S3_ACCESS_KEY')
    secret_key = os.getenv('S3_SECRET_KEY')
    region = os.getenv('S3_REGION', 'us-east-1')
    bucket_docs = os.getenv('S3_BUCKET')
    bucket_images = os.getenv('S3_BUCKET_IMAGES')
    bucket_temp = os.getenv('S3_BUCKET_TEMP')
    
    print(f"\nConfiguration:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Region: {region}")
    print(f"  Documents Bucket: {bucket_docs}")
    print(f"  Images Bucket: {bucket_images}")
    print(f"  Temp Bucket: {bucket_temp}")
    print()
    
    # Initialize S3 client
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'}
            ),
            use_ssl=endpoint.startswith('https://') if endpoint else True,
        )
        print("✅ S3 Client initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize S3 client: {str(e)}")
        return False
    
    # Test 1: Test bucket access (skip ListBuckets if no admin permission)
    print("\n" + "=" * 60)
    print("Test 1: Check Bucket Access")
    print("=" * 60)
    
    # Try to list buckets (may fail if user doesn't have admin permissions)
    try:
        response = s3_client.list_buckets()
        print("✅ Successfully connected to MinIO with admin permissions!")
        print(f"\nAvailable Buckets ({len(response['Buckets'])}):")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
        
        # Check if required buckets exist
        bucket_names = [b['Name'] for b in response['Buckets']]
        required_buckets = [bucket_docs, bucket_images, bucket_temp]
        
        print("\nRequired Buckets Status:")
        for bucket in required_buckets:
            if bucket in bucket_names:
                print(f"  ✅ {bucket} - EXISTS")
            else:
                print(f"  ❌ {bucket} - MISSING (needs to be created)")
        
    except ClientError as e:
        if 'AccessDenied' in str(e):
            print("⚠️  ListBuckets permission denied (this is OK)")
            print("   Testing direct bucket access instead...")
            
            # Test direct bucket access
            required_buckets = [bucket_docs, bucket_images, bucket_temp]
            print("\nTesting Direct Bucket Access:")
            for bucket in required_buckets:
                try:
                    # Try to list objects in bucket (limited to 1)
                    s3_client.list_objects_v2(Bucket=bucket, MaxKeys=1)
                    print(f"  ✅ {bucket} - ACCESSIBLE")
                except ClientError as bucket_error:
                    if 'NoSuchBucket' in str(bucket_error):
                        print(f"  ❌ {bucket} - DOES NOT EXIST")
                    else:
                        print(f"  ❌ {bucket} - ERROR: {str(bucket_error)}")
        else:
            print(f"❌ Error connecting to MinIO: {str(e)}")
            return False
    
    # Test 2: Upload test file
    print("\n" + "=" * 60)
    print("Test 2: Upload Test File")
    print("=" * 60)
    
    test_bucket = bucket_docs
    test_key = 'test/connection_test.txt'
    test_content = b"MinIO connection test - " + str(os.urandom(16).hex()).encode()
    
    try:
        s3_client.put_object(
            Bucket=test_bucket,
            Key=test_key,
            Body=test_content,
            ContentType='text/plain',
            Metadata={
                'test': 'true',
                'uploaded_at': str(os.urandom(8).hex())
            }
        )
        print(f"✅ Test file uploaded successfully")
        print(f"   Bucket: {test_bucket}")
        print(f"   Key: {test_key}")
        print(f"   Size: {len(test_content)} bytes")
    except ClientError as e:
        print(f"❌ Error uploading file: {str(e)}")
        return False
    
    # Test 3: Generate presigned URL
    print("\n" + "=" * 60)
    print("Test 3: Generate Presigned URL")
    print("=" * 60)
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': test_bucket, 'Key': test_key},
            ExpiresIn=300
        )
        print(f"✅ Presigned URL generated successfully")
        print(f"   URL (first 100 chars): {url[:100]}...")
        print(f"   Expires in: 300 seconds (5 minutes)")
    except ClientError as e:
        print(f"❌ Error generating presigned URL: {str(e)}")
        return False
    
    # Test 4: Download file
    print("\n" + "=" * 60)
    print("Test 4: Download File")
    print("=" * 60)
    
    try:
        response = s3_client.get_object(Bucket=test_bucket, Key=test_key)
        downloaded_content = response['Body'].read()
        
        if downloaded_content == test_content:
            print(f"✅ File downloaded successfully")
            print(f"   Content matches: YES")
            print(f"   Size: {len(downloaded_content)} bytes")
        else:
            print(f"❌ Downloaded content doesn't match uploaded content")
            return False
    except ClientError as e:
        print(f"❌ Error downloading file: {str(e)}")
        return False
    
    # Test 5: Get file metadata
    print("\n" + "=" * 60)
    print("Test 5: Get File Metadata")
    print("=" * 60)
    
    try:
        response = s3_client.head_object(Bucket=test_bucket, Key=test_key)
        print(f"✅ File metadata retrieved successfully")
        print(f"   Content-Type: {response.get('ContentType')}")
        print(f"   Content-Length: {response.get('ContentLength')} bytes")
        print(f"   Last-Modified: {response.get('LastModified')}")
        print(f"   Metadata: {response.get('Metadata', {})}")
    except ClientError as e:
        print(f"❌ Error getting file metadata: {str(e)}")
        return False
    
    # Test 6: Delete test file (cleanup)
    print("\n" + "=" * 60)
    print("Test 6: Delete Test File (Cleanup)")
    print("=" * 60)
    
    try:
        s3_client.delete_object(Bucket=test_bucket, Key=test_key)
        print(f"✅ Test file deleted successfully")
        print(f"   Cleanup complete")
    except ClientError as e:
        print(f"❌ Error deleting file: {str(e)}")
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("✅ All tests passed successfully!")
    print("\nMinIO is properly configured and ready to use.")
    print("\nNext steps:")
    print("  1. Ensure all required buckets are created")
    print("  2. Configure bucket policies (public/private)")
    print("  3. Set up CORS if needed for browser uploads")
    print("  4. Implement storage service in your application")
    
    return True

if __name__ == "__main__":
    try:
        success = test_minio_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
