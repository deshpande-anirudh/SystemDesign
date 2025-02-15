"""
Documentation: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html
Use: Download DynamoDB local 
"""

import boto3

# Create a DynamoDB client (instead of a resource)
dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # Local DynamoDB
    region_name='us-west-2',  # Any region name
    aws_access_key_id='fakeMyAccessKeyId',  # Dummy access key
    aws_secret_access_key='fakeSecretAccessKey'  # Dummy secret key
)

# List tables using the client
response = dynamodb_client.list_tables()
print("Tables:", response['TableNames'])
