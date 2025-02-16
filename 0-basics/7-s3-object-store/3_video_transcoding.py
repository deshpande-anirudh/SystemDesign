import os
import ffmpeg
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize boto3 client for S3-compatible MinIO
s3_client = boto3.client(
    's3',
    endpoint_url="http://localhost:9000",  # MinIO server endpoint
    aws_access_key_id="admin",
    aws_secret_access_key="admin123",
    region_name="us-east-1",  # You can change the region if necessary
    use_ssl=False  # Set to True for HTTPS
)

# Specify the S3 bucket name
bucket_name = "my-videos"

# Ensure the bucket exists
try:
    s3_client.head_bucket(Bucket=bucket_name)
except ClientError as e:
    if e.response['Error']['Code'] == 'NoSuchBucket':
        s3_client.create_bucket(Bucket=bucket_name)
    else:
        print(f"Error checking bucket: {e}")


# Function to transcode video to HLS format (segments and playlist)
def transcode_to_hls(input_file, output_folder, resolution):
    try:
        # Define output filenames for HLS segments and playlist
        # Define input file and output folder

        segment_pattern = f'{output_folder}/video_1920x1080_%03d.ts'
        playlist_file = f'{output_folder}/playlist.m3u8'

        # Use ffmpeg to transcode the video to HLS format
        ffmpeg.input(input_file).output(
            playlist_file,  # Output playlist file
            vcodec='libx264', acodec='aac',
            vf=f"scale={resolution[0]}:{resolution[1]}",
            hls_time=10,  # Set segment duration to 10 seconds
            hls_list_size=0,  # Include all segments in the playlist
            hls_segment_filename=segment_pattern,  # Segment filename pattern
            f='hls'  # Explicitly specify HLS format
        ).run()

        print(f"Video transcoded to HLS format with resolution {resolution[0]}x{resolution[1]}")
        print(f"Playlist file: {playlist_file}")
    except ffmpeg.Error as e:
        print(f"Error during transcoding: {e}")


# Function to upload HLS segments and playlist to S3 (MinIO)
def upload_to_s3(local_folder, bucket_name, object_prefix):
    try:
        for file_name in os.listdir(local_folder):
            local_file = os.path.join(local_folder, file_name)
            if os.path.isfile(local_file):
                object_name = f"{object_prefix}/{file_name}"
                s3_client.upload_file(local_file, bucket_name, object_name)
                print(f"Successfully uploaded {object_name} to S3 bucket {bucket_name}")
    except (NoCredentialsError, ClientError) as e:
        print(f"Error uploading files: {e}")


# List of resolutions to transcode the video
resolutions = [(1920, 1080), (1280, 720), (640, 360)]  # Full HD, HD, and SD

# Input video file
input_video = "srinath.mp4"

# Output folder for HLS segments
output_folder = "hls_output"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Transcode and upload for each resolution
for resolution in resolutions:
    # Transcode video to HLS format for the specific resolution
    transcode_to_hls(input_video, output_folder, resolution)

    # Upload HLS segments and playlist to MinIO (via boto3)
    upload_to_s3(output_folder, bucket_name, f"videos/{resolution[0]}x{resolution[1]}")

    # Optional: Clean up local files after upload
    for file_name in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, file_name))
