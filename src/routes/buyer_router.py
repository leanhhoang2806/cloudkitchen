from fastapi import Depends, Query
from src.validations.validators import validate_token
from src.managers.buyer_manager import BuyerManager
from src.models.data_model import BuyerInfoUpdate  # , BuyerInfoCreate
from src.models.postgres_model import BuyerPydantic
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter


router = CustomAPIRouter()
buyer_manager = BuyerManager()


@router.get("/buyer/", response_model=BuyerPydantic)
async def get_buyer_by_email(
    email: str = Query(...),
    token=Depends(validate_token),
):
    buyer = buyer_manager.get_by_email(email)
    return BuyerPydantic.from_orm(buyer)


@router.get("/buyer/no-validation/{buyer_id}")
async def get_buyer_name_by_id_no_validation(buyer_id: UUID):
    buyer = buyer_manager.get(buyer_id)
    return {"name": buyer.email}


@router.get("/buyer/{buyer_id}", response_model=BuyerPydantic)
async def get_buyer(
    buyer_id: UUID,
    token=Depends(validate_token),
):
    buyer = buyer_manager.get(buyer_id)
    return BuyerPydantic.from_orm(buyer)


# @router.post("/buyer/", response_model=BuyerPydantic)
# async def create_buyer(
#     buyer_data: BuyerInfoCreate,
#     token=Depends(validate_token),
# ):
#     buyer = buyer_manager.create(buyer_data)
#     return BuyerPydantic.from_orm(buyer)


@router.put("/buyer/{buyer_id}", response_model=BuyerPydantic)
async def update_buyer(
    buyer_id: UUID,
    buyer_data: BuyerInfoUpdate,
    token=Depends(validate_token),
):
    buyer = buyer_manager.update(buyer_id, buyer_data)
    return BuyerPydantic.from_orm(buyer)


@router.delete("/buyer/{buyer_id}")
async def delete_buyer(
    buyer_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = buyer_manager.delete(buyer_id)
    return {"deleted_count": deleted_count}
