import boto3
from PIL import Image
from io import BytesIO
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
from typing import Optional
from uuid import uuid4
from botocore.exceptions import ClientError
from src.managers.payment_manager import PaymentManager
from src.managers.dish_manager import DishManager
from src.managers.stripe_manager import StripeManager
from src.managers.seller_manager import SellerInfoManager
from src.models.data_model import PaymentUpdate
from src.logger.logger import initialize_logger
from uuid import UUID
from src.errors.custom_exceptions import (
    MediaUploadLimitException,
    NotAllowedToUploadThisImage,
)

from src.managers.configuration_manager import CONFIG

logger = initialize_logger()

stripe_manager = StripeManager()
payment_manager = PaymentManager()
seller_info_manager = SellerInfoManager()
MAX_IMAGE_SIZE_MB = 5


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

    def _is_image_valid(self, file: UploadFile) -> bool:
        try:
            read_image = file.file.read()
            file_size_mb = len(read_image) / (1024 * 1024)
            if file_size_mb > MAX_IMAGE_SIZE_MB:
                return False
            img = Image.open(BytesIO(read_image))
            img.verify()
            return True
        except (IOError, SyntaxError) as e:
            logger.error(e)
            return False

    def upload_to_s3(self, file: UploadFile, seller_id: UUID) -> Optional[str]:
        try:
            if not self._is_allowed_to_upload(seller_id):
                raise MediaUploadLimitException
            if not self._is_image_valid(file):
                raise NotAllowedToUploadThisImage

            file.file.seek(0)  # reset after any image process
            unique_filename = f"{file.filename.split('.')[0]}_{str(uuid4())}.{file.filename.split('.')[-1]}"
            self.s3_client.upload_fileobj(file.file, self.bucket_name, unique_filename)

            # Generate the S3 URL
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{unique_filename}"
            return s3_url
        except NoCredentialsError:
            # Handle credential errors
            return None

    def delete_from_s3(self, object_path: str) -> bool:
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_path)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def _is_allowed_to_upload(self, seller_id: UUID) -> bool:
        payment_info = self.payment_manager.get_by_seller_id(seller_id)
        dishes_owned_by_seller = self.dish_manager.get_by_seller_id(seller_id)
        if len(dishes_owned_by_seller) > payment_info.picture_upload_limit:
            if stripe_manager.is_seller_subsciption_active:
                seller_info = seller_info_manager.get(seller_id)
                payment_manager.payment_update_by_email(
                    PaymentUpdate(
                        email=seller_info.email,
                        picture_upload_limit=10,
                        dishes_to_feature_limit=5,
                    )
                )
        return payment_info.picture_upload_limit > len(dishes_owned_by_seller)


BUCKET_NAME = "popo24-public-read-images"
S3_UPLOADER = S3Uploader(
    CONFIG.S3_ONLY_AWS_ACCESS_KEY_ID, CONFIG.S3_ONLY_AWS_SECRET_ACCESS_KEY, BUCKET_NAME
)
