from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.seller_application_manager import SellerApplicationManager
from src.routes.custom_api_router import CustomAPIRouter
from src.models.postgres_model import SellerApplicationPydantic
from src.models.data_model import SellerApplicationCreate
from uuid import UUID

router = CustomAPIRouter()
seller_application_manager = SellerApplicationManager()


@router.post(
    "/seller-application/",
    response_model=SellerApplicationPydantic,
)
async def post_seller_application(
    seller_application: SellerApplicationCreate,
    token=Depends(validate_token),
):
    return SellerApplicationPydantic.from_orm(
        seller_application_manager.create(seller_application)
    )


@router.get(
    "/seller-application/{application_id}",
    response_model=SellerApplicationPydantic,
)
async def get_seller_application_by_id(
    application_id: UUID,
    token=Depends(validate_token),
):
    return SellerApplicationPydantic.from_orm(
        seller_application_manager.get(application_id)
    )


@router.get(
    "/seller-application/seller/{application_email}",
    response_model=SellerApplicationPydantic,
)
async def get_seller_application_by_email(
    application_email: str,
    token=Depends(validate_token),
):
    return SellerApplicationPydantic.from_orm(
        seller_application_manager.get_by_email(application_email)
    )
