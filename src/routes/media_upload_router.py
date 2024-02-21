from fastapi import APIRouter, File, UploadFile, Depends
from src.managers.s3_manager import S3Uploader
from src.managers.configuration_manager import CONFIG
from src.validations.validators import validate_token

router = APIRouter()

bucket_name = "dish-popo24"
s3_uploader = S3Uploader(
    CONFIG.AWS_ACCESS_KEY_ID, CONFIG.AWS_SECRET_ACCESS_KEY, bucket_name
)

s3_uploader.create_bucket_if_not_exist(bucket_name)


@router.post("/s3/upload/")
async def upload_file(
    file: UploadFile = File(...),
    token=Depends(validate_token),
):
    s3_path = s3_uploader.upload_to_s3(file)

    if s3_path:
        return {"s3_path": s3_path}
    else:
        return {"message": "File upload failed"}
