from minio import Minio
from minio.error import S3Error
import os
import time

# MinIO connection details
MINIO_ENDPOINT = "minio:9000"
ROOT_USER = "myaccesskey"
ROOT_PASSWORD = "mysecretkey"

# Bucket name in MinIO
BUCKET_NAME = "mybucket"

# Path to the input files directory
INPUT_DIR = "/app/input_files"

def connect_to_minio():
    """Connect to MinIO server and return the client info"""
    client = Minio(
        MINIO_ENDPOINT,
        access_key = ROOT_USER,
        secret_key = ROOT_PASSWORD,
        secure=False
    )
    return client

def create_bucket(client, bucket_name):
    """Create a bucket in MinIO if it doesn't already exist."""
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
           
        # Giving time to let the user set the quota.
        # If you wish to set the quota, remove the comment sign for time.sleep
        # time.sleep(45)
    else:
        print(f"Bucket '{bucket_name}' already exists.")

def upload_files_to_minio(client, bucket_name, input_dir):
    """Upload all files from the input directory to the MinIO bucket."""
    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        return

    files = os.listdir(input_dir)
    if not files:
        print(f"No files found in '{input_dir}' to upload.")
        return

    print(f"Found {len(files)} files in '{input_dir}'. Uploading to MinIO...")

    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        if os.path.isfile(file_path):
        # Sending files to MinIO Bucket
            client.fput_object(
            bucket_name,
            file_name, 
            file_path)
            print(f"Uploaded '{file_name}' to bucket '{bucket_name}'.")
    
        else:
            print(f"'{file_name}' is not a file, skipping...")


if __name__ == "__main__":
    # Connecting to MinIO
    minio_client = connect_to_minio()
    # Waiting for launch.sh to execute

    if minio_client:
        create_bucket(minio_client, BUCKET_NAME)
        time.sleep(5)
        print("Waiting for all settings to set up...")
        upload_files_to_minio(minio_client, BUCKET_NAME, INPUT_DIR)
