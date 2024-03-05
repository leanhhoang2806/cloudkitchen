from fastapi import APIRouter, File, UploadFile, Depends
from src.managers.s3_manager import S3Uploader
from src.managers.configuration_manager import CONFIG
from src.validations.validators import validate_token
from uuid import UUID

router = APIRouter()


bucket_name = "popo24-public-read-images"
s3_uploader = S3Uploader(
    CONFIG.AWS_ACCESS_KEY_ID, CONFIG.AWS_SECRET_ACCESS_KEY, bucket_name
)

s3_uploader.create_bucket_if_not_exist(bucket_name)


@router.post("/s3/upload/{seller_id}")
async def upload_file(
    seller_id: UUID,
    file: UploadFile = File(...),
    token=Depends(validate_token),
):
    s3_path = s3_uploader.upload_to_s3(file, seller_id)

    if s3_path:
        return {"s3_path": s3_path}
    else:
        return {"message": "File upload failed"}
