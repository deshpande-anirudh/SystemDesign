import boto3

# Initialize DynamoDB client
dynamodb = boto3.client(
    "dynamodb",
    endpoint_url='http://localhost:8000',  # Local DynamoDB
    region_name="us-west-2",
    aws_access_key_id='fakeMyAccessKeyId',  # Dummy access key
    aws_secret_access_key='fakeSecretAccessKey'  # Dummy secret key
)

# Table name
table_name = "JobScheduling2"

# Create table
response = dynamodb.create_table(
    TableName=table_name,
    AttributeDefinitions=[
        {"AttributeName": "job_id", "AttributeType": "S"},
        {"AttributeName": "execution_start_time", "AttributeType": "N"},
        {"AttributeName": "execution_date", "AttributeType": "S"},  # Added for time-based partitioning (optional)
    ],
    KeySchema=[
        {"AttributeName": "job_id", "KeyType": "HASH"},
        {"AttributeName": "execution_start_time", "KeyType": "RANGE"},
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "ExecutionStartTimeIndex",
            "KeySchema": [
                {"AttributeName": "execution_start_time", "KeyType": "HASH"},
                {"AttributeName": "job_id", "KeyType": "RANGE"},  # Sort key for GSI
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        }
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)

print(f"Creating table {table_name}...")
