import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # 1. Initialize S3 Client
    s3 = boto3.client('s3')
    
    # 2. List all buckets
    buckets = s3.list_buckets()['Buckets']
    unencrypted_buckets = []
    
    for b in buckets:
        name = b['Name']
        try:
            # 3. Check for encryption configuration
            s3.get_bucket_encryption(Bucket=name)
        except ClientError as e:
            # If configuration is missing, catch the error code
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                unencrypted_buckets.append(name)
                
    # 4. Print results for logging
    if unencrypted_buckets:
        print(" Unencrypted Buckets Found:")
        for bucket in unencrypted_buckets:
            print(f"- {bucket}")
    else:
        print("✅ All buckets are explicitly encrypted.")
        
    return {"statusCode": 200, "body": "Scan complete."}