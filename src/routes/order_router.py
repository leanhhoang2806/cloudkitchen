from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.orders_manager import OrderManager
from src.models.data_model import OrderCreate, OrderUpdate
from src.models.postgres_model import OrderPydantic
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
order_manager = OrderManager()


@router.get("/order/seller/{seller_id}", response_model=Optional[List[OrderPydantic]])
async def get_order_by_seller_id(
    seller_id: UUID,
    token=Depends(validate_token),
):
    orders = order_manager.get_by_seller_id(seller_id)
    if not orders:
        return None
    return [OrderPydantic.from_orm(order) for order in orders]


@router.get("/order/{order_id}", response_model=OrderPydantic)
async def get_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    order = order_manager.get(order_id)
    return OrderPydantic.from_orm(order)


@router.post("/order/", response_model=OrderPydantic)
async def create_order(
    order_data: OrderCreate,
    token=Depends(validate_token),
):
    order = order_manager.create(order_data)
    return OrderPydantic.from_orm(order)


@router.put("/order/{order_id}", response_model=OrderPydantic)
async def update_order(
    order_id: UUID,
    order_data: OrderUpdate,
    token=Depends(validate_token),
):
    order = order_manager.update(order_id, order_data)
    return OrderPydantic.from_orm(order)


@router.delete("/order/{order_id}")
async def delete_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = order_manager.delete(order_id)
    return {"deleted_count": deleted_count}
