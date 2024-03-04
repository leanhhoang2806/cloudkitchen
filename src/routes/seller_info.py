from fastapi import Depends, Query
from src.validations.validators import validate_token
from src.managers.seller_manager import SellerInfoManager
from src.models.data_model import SellerInfoCreate, SellerInfoUpdate
from src.models.postgres_model import SellerInfoPydantic
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional

router = CustomAPIRouter()
seller_info_manager = SellerInfoManager()


@router.get("/seller_info/", response_model=Optional[SellerInfoPydantic])
async def get_seller_by_email(
    email: str = Query(...),
    token=Depends(validate_token),
):
    seller_info = seller_info_manager.get_by_email(email)
    return SellerInfoPydantic.from_orm(seller_info) if seller_info else None


@router.get("/seller_info/{seller_info_id}", response_model=SellerInfoPydantic)
async def get_seller_info(
    seller_info_id: UUID,
    token=Depends(validate_token),
):
    seller_info = seller_info_manager.get(seller_info_id)
    return SellerInfoPydantic.from_orm(seller_info)


@router.post("/seller_info/", response_model=SellerInfoPydantic)
async def create_seller_info(
    seller_info_data: SellerInfoCreate,
    token=Depends(validate_token),
):
    seller_info = seller_info_manager.create_with_payment_limit(seller_info_data)
    return SellerInfoPydantic.from_orm(seller_info)


@router.put("/seller_info/{seller_info_id}", response_model=SellerInfoPydantic)
async def update_seller_info(
    seller_info_id: UUID,
    seller_info_data: SellerInfoUpdate,
    token=Depends(validate_token),
):
    seller_info = seller_info_manager.update(seller_info_id, seller_info_data)
    return SellerInfoPydantic.from_orm(seller_info)


@router.delete("/seller_info/{seller_info_id}")
async def delete_seller_info(
    seller_info_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = seller_info_manager.delete(seller_info_id)
    return {"deleted_count": deleted_count}
