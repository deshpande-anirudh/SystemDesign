import boto3
from botocore.exceptions import ClientError


with open("input/1mb_file.txt", "w") as f:
    f.write("A" * 500 * 1024 * 1024)  # 1024 bytes = 1 KB

print("1 MB text file created: 1mb_file.txt")

s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",  # MinIO
    aws_access_key_id="admin",
    aws_secret_access_key="admin123",
    region_name="us-east-1"
)

bucket_name = "my-bucket"
object_key = "1mb_file.txt"
file_path = "input/1mb_file.txt"
part_size = 5 * 1024 * 1024  # 5MB per part (MinIO supports smaller parts)


def multipart_upload():
    # Step 1: Initiate the multipart upload
    try:
        response = s3_client.create_multipart_upload(Bucket=bucket_name, Key=object_key)
        upload_id = response["UploadId"]
        print(f"Upload initiated with ID: {upload_id}")
    except ClientError as e:
        print(f"Failed to initiate upload: {e}")
        return

    parts = []
    try:
        # Step 2: Upload file parts
        with open(file_path, "rb") as file:
            part_number = 1
            while chunk := file.read(part_size):
                response = s3_client.upload_part(
                    Bucket=bucket_name,
                    Key=object_key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=chunk
                )
                parts.append({"PartNumber": part_number, "ETag": response["ETag"]})
                print(f"Uploaded part {part_number}")
                part_number += 1

        # Step 3: Complete the multipart upload
        response = s3_client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=object_key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts}
        )
        print(f"Multipart upload completed successfully!, {response}")

    except ClientError as e:
        print(f"Error during upload: {e}")
        # Optional: Abort the multipart upload if there's an error
        s3_client.abort_multipart_upload(Bucket=bucket_name, Key=object_key, UploadId=upload_id)
        print("Multipart upload aborted.")

multipart_upload()
