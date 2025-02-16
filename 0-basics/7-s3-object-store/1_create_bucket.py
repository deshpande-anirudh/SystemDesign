import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # MinIO runs here
    aws_access_key_id="admin",
    aws_secret_access_key="admin123",
    region_name="us-east-1"
)

bucket_name = "my-bucket"

# Check if the bucket exists
def bucket_exists(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            raise  # Some other error occurred

# Create the bucket only if it doesn't exist
if not bucket_exists(bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"Bucket '{bucket_name}' created.")
else:
    print(f"Bucket '{bucket_name}' already exists.")

# Upload a file
s3_client.upload_file("test.txt", bucket_name, "test.txt")

print("File uploaded successfully!")
