from fastapi import File, UploadFile, Depends
from src.managers.s3_manager import S3_UPLOADER, BUCKET_NAME
from src.validations.validators import validate_token
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter


router = CustomAPIRouter()


S3_UPLOADER.create_bucket_if_not_exist(BUCKET_NAME)


@router.post("/s3/upload/{seller_id}")
async def upload_file(
    seller_id: UUID,
    file: UploadFile = File(...),
    token=Depends(validate_token),
):
    s3_path = S3_UPLOADER.upload_to_s3(file, seller_id)

    if s3_path:
        return {"s3_path": s3_path}
    else:
        return {"message": "File upload failed"}
