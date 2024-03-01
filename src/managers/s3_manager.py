import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from typing import Optional
from uuid import uuid4
from botocore.exceptions import ClientError


class S3Uploader:
    def __init__(
        self, aws_access_key_id: str, aws_secret_access_key: str, bucket_name: str
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def create_bucket_if_not_exist(self, bucket_name):
        try:
            # Check if the bucket exists
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            # If the bucket does not exist, create it
            self.s3_client.create_bucket(Bucket=bucket_name)

    def upload_to_s3(self, file: UploadFile) -> Optional[str]:
        try:
            unique_filename = f"{file.filename.split('.')[0]}_{str(uuid4())}.{file.filename.split('.')[-1]}"
            self.s3_client.upload_fileobj(file.file, self.bucket_name, unique_filename)

            # Generate the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
            return s3_url
        except NoCredentialsError:
            # Handle credential errors
            return None
