# Running SQS in local

### **Steps to Run SQS Locally Using LocalStack**
#### **1. Install LocalStack**
```sh
pip install localstack
```
Or using Docker:
```sh
docker pull localstack/localstack
```

#### **2. Start LocalStack**
```sh
localstack start
```
Or with Docker:
```sh
docker run -it -p 4566:4566 -e SERVICES=sqs localstack/localstack
```
LocalStack will now be running on `http://localhost:4566`.

#### **3. Configure AWS CLI for LocalStack**
```sh
aws configure set aws_access_key_id test
aws configure set aws_secret_access_key test
aws configure set region us-east-1
```

#### **4. Create an SQS Queue Locally**
```sh
aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name my-local-queue
```

#### **5. Send a Message to the Queue**
```sh
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/my-local-queue --message-body "Hello from Local SQS!"
```

#### **6. Receive Messages**
```sh
aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url http://localhost:4566/000000000000/my-local-queue
```

### **Using boto3 in Python**
```python
import boto3

# Connect to LocalStack
sqs = boto3.client("sqs", endpoint_url="http://localhost:4566")

# Create Queue
response = sqs.create_queue(QueueName="my-local-queue")
queue_url = response["QueueUrl"]

# Send Message
sqs.send_message(QueueUrl=queue_url, MessageBody="Hello from Local SQS!")

# Receive Message
messages = sqs.receive_message(QueueUrl=queue_url)
print(messages)
```
