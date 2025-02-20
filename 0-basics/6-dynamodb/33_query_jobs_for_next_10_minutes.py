import boto3
from datetime import datetime, timedelta

# Table name
table_name = "JobScheduling"

# Initialize the DynamoDB resource
table = boto3.resource(
    'dynamodb',
    region_name="us-west-2",
    aws_access_key_id='fakeMyAccessKeyId',  # Dummy access key
    aws_secret_access_key='fakeSecretAccessKey',  # Dummy secret key
    endpoint_url='http://localhost:8000').Table(table_name)

# Get current time and 15 minutes later
current_time = int(datetime.utcnow().timestamp())  # Current time in UNIX timestamp
fifteen_minutes_later = current_time + 900  # 15 minutes later in UNIX timestamp

# Query to fetch jobs scheduled between now and the next 15 minutes
response = table.query(
    IndexName="ExecutionStartTimeIndex",  # Querying the GSI
    KeyConditionExpression="execution_start_time BETWEEN :start AND :end",
    ExpressionAttributeValues={
        ":start": current_time,
        ":end": fifteen_minutes_later,
    }
)

# Print the results
if "Items" in response:
    for job in response["Items"]:
        print(f"Job ID: {job['job_id']}, Execution Start Time: {job['execution_start_time']}")
else:
    print("No jobs found in the next 15 minutes.")
