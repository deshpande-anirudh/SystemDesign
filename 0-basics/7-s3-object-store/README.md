# Running S3 in local

Yes! You can run **S3 locally** using **MinIO** or **LocalStack**, which are great for learning and testing without an AWS account.  

---

## **1️⃣ Using MinIO (Best for Local S3-Compatible Storage)**
MinIO is an **S3-compatible** storage solution that runs locally.  

### **Steps to Set Up MinIO Locally**  
#### **Step 1: Install MinIO**  
- **Docker (Recommended)**
  ```sh
  docker run -p 9000:9000 -p 9001:9001 --name minio \
  -e "MINIO_ROOT_USER=admin" \
  -e "MINIO_ROOT_PASSWORD=admin123" \
  quay.io/minio/minio server /data --console-address ":9001"
  ```
- Alternatively, download MinIO from [min.io](https://min.io) and run it manually.

#### **Step 2: Access MinIO**
- MinIO **Web UI**: [http://localhost:9001](http://localhost:9001)  
- **Login with**:  
  - **User**: `admin`  
  - **Password**: `admin123`

#### **Step 3: Configure AWS SDK to Use MinIO**
- Install Boto3 if you haven't:
  ```sh
  pip install boto3
  ```
- Configure your script to point to MinIO instead of AWS S3:
  ```python
  import boto3

  s3_client = boto3.client(
      "s3",
      endpoint_url="http://localhost:9000",  # MinIO runs here
      aws_access_key_id="admin",
      aws_secret_access_key="admin123",
      region_name="us-east-1"
  )

  # Create a bucket
  s3_client.create_bucket(Bucket="my-bucket")

  # Upload a file
  s3_client.upload_file("test.txt", "my-bucket", "test.txt")

  print("File uploaded successfully!")
  ```
✅ **MinIO Pros:**  
- Runs **locally** without internet  
- Fully **S3 API compatible**  
- **Lightweight & fast**

---

## **2️⃣ Using LocalStack (Best for Full AWS Simulation)**
LocalStack emulates **AWS services**, including S3.

### **Steps to Set Up LocalStack**
#### **Step 1: Install LocalStack**
- **With Docker**:
  ```sh
  docker run --rm -p 4566:4566 localstack/localstack
  ```
- Or install via `pip`:
  ```sh
  pip install localstack
  ```

#### **Step 2: Configure AWS CLI**
```sh
aws --endpoint-url=http://localhost:4566 s3 mb s3://my-bucket
aws --endpoint-url=http://localhost:4566 s3 ls
```

#### **Step 3: Use in Python**
```python
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Create bucket and upload file
s3_client.create_bucket(Bucket="my-bucket")
s3_client.upload_file("test.txt", "my-bucket", "test.txt")

print("File uploaded to LocalStack S3!")
```

✅ **LocalStack Pros:**  
- Simulates **multiple AWS services**, not just S3  
- Supports **Lambda, DynamoDB, SQS, etc.**  
- Works well for **testing AWS integrations**  

---

### **Which One Should You Use?**
| Feature         | **MinIO** | **LocalStack** |
|----------------|----------|---------------|
| **S3 API Compatibility** | ✅ Full | ✅ Full |
| **Local-Only** | ✅ Yes | ✅ Yes |
| **Requires Internet?** | ❌ No | ❌ No |
| **Best for** | Storage & Uploads | Full AWS Testing |
| **Multi-Part Upload** | ✅ Yes | ✅ Yes |
| **Performance** | ⚡ Fast | ⚡ Slower |

👉 **Use MinIO if you just need local S3 storage.**  
👉 **Use LocalStack if you want a full AWS simulation.**  

Would you like help setting up multi-part uploads on MinIO? 🚀