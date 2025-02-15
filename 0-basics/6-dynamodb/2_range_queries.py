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
    user_uuid = str(uuid4())  # UUID for uniqueness
    # Append the UUID to the timestamp to ensure uniqueness
    timestamp_with_uuid = timestamp + '#' + user_uuid
    try:
        dynamodb_client.put_item(
            TableName='users',
            Item={
                'user-id': {'S': user_id},
                'timestamp': {'S': timestamp_with_uuid}  # Store timestamp with UUID
            }
        )
        print(f"Inserted user {user_id} with timestamp {timestamp_with_uuid}")
    except ClientError as e:
        print(f"Error inserting item: {e}")


# Example usage: insert a user with a timestamp
for _ in range(1000):
    user_id = f'user123'
    timestamp = datetime.now() + timedelta(minutes=random.randint(10, 50))
    timestamp = timestamp.isoformat()

    insert_user(user_id, timestamp)


def query_users_within_time_range(user_id):
    # Get current time and calculate time range (12 minutes ago to 10 minutes ago)
    current_time = datetime.now()
    twelve_minutes_ago = (current_time + timedelta(minutes=12)).isoformat()
    ten_minutes_ago = (current_time + timedelta(minutes=18)).isoformat()

    try:
        # Query for users with timestamp starting with the time range
        response = dynamodb_client.query(
            TableName='users',
            KeyConditionExpression="#user_id = :user_id AND begins_with(#timestamp, :start_time)",
            ExpressionAttributeNames={
                "#user_id": "user-id",
                "#timestamp": "timestamp"
            },
            ExpressionAttributeValues={
                ":user_id": {'S': user_id},
                ":start_time": {'S': twelve_minutes_ago.split('.')[0]}  # Remove milliseconds for begins_with
            }
        )

        # Filter items within the desired time range
        items_in_range = []
        if 'Items' in response:
            for item in response['Items']:
                timestamp_with_uuid = item['timestamp']['S']
                timestamp_part = timestamp_with_uuid.split('#')[0]  # Extract the timestamp part
                if twelve_minutes_ago <= timestamp_part <= ten_minutes_ago:
                    items_in_range.append(item)

        # Print the results
        if items_in_range:
            print("Found items:")
            for item in items_in_range:
                timestamp_with_uuid = item['timestamp']['S']
                timestamp_part, uuid = timestamp_with_uuid.split('#')  # Split timestamp and UUID
                print(f"User: {item['user-id']['S']}, Timestamp: {timestamp_part}, UUID: {uuid}")
        else:
            print("No items found in the specified time range.")

    except Exception as e:
        print(f"Error querying items: {e}")


query_users_within_time_range('user123')