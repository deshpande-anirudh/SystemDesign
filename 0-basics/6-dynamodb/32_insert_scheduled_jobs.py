import boto3
import random
from datetime import datetime, timedelta

# Table name
table_name = "JobScheduling"

# Get the current time and 1 hour later
current_time = int(datetime.utcnow().timestamp())  # Current time in UNIX timestamp
one_hour_later = current_time + 3600  # 1 hour later

# Initialize table resource
table = boto3.resource(
    'dynamodb',
    region_name="us-west-2",
    aws_access_key_id='fakeMyAccessKeyId',  # Dummy access key
    aws_secret_access_key='fakeSecretAccessKey',  # Dummy secret key
    endpoint_url='http://localhost:8000').Table(table_name)

# Function to generate a random job_id
def generate_job_id():
    return f"job_{random.randint(1000, 9999)}"

# Insert 1000 jobs with random execution_start_time within the next 1 hour
for _ in range(1000):
    execution_start_time = random.randint(current_time, one_hour_later)  # Random time within the next 1 hour
    job_id = generate_job_id()  # Random job_id

    # Insert the job into DynamoDB
    table.put_item(
        Item={
            "job_id": job_id,
            "execution_start_time": execution_start_time,
        }
    )

print("1000 jobs added to the JobScheduling table.")
