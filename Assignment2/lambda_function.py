import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # 1. Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Replace with your actual bucket name
    BUCKET_NAME = 'my-lambda-cleanup-bucket-2026' 
    
    # Calculate the cutoff date (30 days ago from right now)
    # Note: We use timezone.utc because S3 timestamps are always in UTC
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
    
    print(f"Starting cleanup. Looking for files modified before: {cutoff_date}")
    
    # 2. List objects inside the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    
    # Check if the bucket is completely empty first
    if 'Contents' not in response:
        print("The bucket is already empty.")
        return {
            'statusCode': 200,
            'body': 'No files to clean up.'
        }
        
    deleted_count = 0
    
    # 3. Loop through and evaluate each object
    for obj in response['Contents']:
        file_name = obj['Key']
        file_modified_time = obj['LastModified']
        
        # Compare dates
        if file_modified_time < cutoff_date:
            # 4. Delete the object if it's older than 30 days
            s3_client.delete_object(Bucket=BUCKET_NAME, Key=file_name)
            
            # 5. Print out the name for CloudWatch logging
            print(f"DELETED: {file_name} (Modified: {file_modified_time})")
            deleted_count += 1
        else:
            print(f"KEPT: {file_name} (Only {datetime.now(timezone.utc) - file_modified_time} old)")

    return {
        'statusCode': 200,
        'body': f"Cleanup complete. Successfully deleted {deleted_count} old file(s)."
    }