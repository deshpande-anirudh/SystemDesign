import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import random
from uuid import uuid4

# Initialize the DynamoDB client
dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # Local DynamoDB
    region_name='us-west-2',  # Any region name
    aws_access_key_id='fakeMyAccessKeyId',  # Dummy access key
    aws_secret_access_key='fakeSecretAccessKey'  # Dummy secret key
)

# Create the table if it doesn't exist
try:
    # Check if the table exists
    response = dynamodb_client.list_tables()
    if 'users' not in response['TableNames']:
        # Create the table if it doesn't exist
        dynamodb_client.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'user-id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'user-id',
                    'AttributeType': 'S'  # String type for user-id
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'  # String type for timestamp
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table 'users' created successfully.")
    else:
        print("Table 'users' already exists.")
except ClientError as e:
    print(f"Error checking or creating table: {e}")


# Insert an entry into the 'users' table
def insert_user(user_id, timestamp):
    uuid = str(uuid4())
    timestamp = timestamp + '#' + uuid
    try:
        dynamodb_client.put_item(
            TableName='users',
            Item={
                'user-id': {'S': user_id},
                'timestamp': {'S': timestamp}
            }
        )
        print(f"Inserted user {user_id} with timestamp {timestamp}")
    except ClientError as e:
        print(f"Error inserting item: {e}")


# Example usage: insert a user with a timestamp
for _ in range(1000):
    user_id = f'user{random.randint(100, 100000)}'
    timestamp = datetime.now() + timedelta(minutes=random.randint(10, 50))
    timestamp = timestamp.isoformat()

    insert_user(user_id, timestamp)



