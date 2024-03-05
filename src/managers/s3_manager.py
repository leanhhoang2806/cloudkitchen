import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from typing import Optional
from uuid import uuid4
from botocore.exceptions import ClientError
from src.managers.payment_manager import PaymentManager
from src.managers.dish_manager import DishManager
from uuid import UUID
from src.errors.custom_exceptions import MediaUploadLimitException


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

        self.payment_manager = PaymentManager()
        self.dish_manager = DishManager()

    def create_bucket_if_not_exist(self, bucket_name):
        try:
            # Check if the bucket exists
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError:
            # If the bucket does not exist, create it
            self.s3_client.create_bucket(Bucket=bucket_name)

    def upload_to_s3(self, file: UploadFile, seller_id: UUID) -> Optional[str]:
        try:
            if not self._is_allowed_to_upload(seller_id):
                raise MediaUploadLimitException

            unique_filename = f"{file.filename.split('.')[0]}_{str(uuid4())}.{file.filename.split('.')[-1]}"
            self.s3_client.upload_fileobj(file.file, self.bucket_name, unique_filename)

            # Generate the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
            return s3_url
        except NoCredentialsError:
            # Handle credential errors
            return None

    def _is_allowed_to_upload(self, seller_id: UUID) -> bool:
        payment_info = self.payment_manager.get_by_seller_id(seller_id)
        dishes_owned_by_seller = self.dish_manager.get_by_seller_id(seller_id)
        return payment_info.picture_upload_limit > len(dishes_owned_by_seller)
