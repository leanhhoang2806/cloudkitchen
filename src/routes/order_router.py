from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.orders_manager import OrderManager
from src.models.data_model import (
    OrderCreate,
    OrderStatusUpdate,
    OrderInformationForExternal,
)
from src.models.postgres_model import DishPydantic, Order
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
order_manager = OrderManager()


def map_to_order_external(order_from_db: Order) -> OrderInformationForExternal:
    return OrderInformationForExternal(
        id=order_from_db.id,
        dish_id=order_from_db.dish_id,
        status=order_from_db.status,
        created_at=order_from_db.created_at,
        updated_at=order_from_db.updated_at,
    )


@router.get(
    "/order/buyer/{buyer_id}",
    response_model=Optional[List[OrderInformationForExternal]],
)
async def get_order_by_buyer_id(
    buyer_id: UUID,
    token=Depends(validate_token),
):
    orders = order_manager.get_by_buyer_id(buyer_id)
    return [map_to_order_external(order) for order in orders]


@router.get(
    "/order/seller/{seller_id}",
    response_model=Optional[List[OrderInformationForExternal]],
)
async def get_order_by_seller_id(
    seller_id: UUID,
    token=Depends(validate_token),
):
    orders = order_manager.get_by_seller_id(seller_id)
    return [map_to_order_external(order) for order in orders]


@router.get("/order/{order_id}", response_model=OrderInformationForExternal)
async def get_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    order = order_manager.get(order_id)
    return map_to_order_external(order)


@router.get("/order/{order_id}/dish", response_model=Optional[List[DishPydantic]])
async def get_dish_by_order_id(
    order_id: UUID,
    token=Depends(validate_token),
):
    dishes = order_manager.get_dish_by_order_id(order_id)
    return [map_to_order_external(dish) for dish in dishes]


@router.post("/order/", response_model=List[OrderInformationForExternal])
async def create_order(
    order_data: OrderCreate,
    token=Depends(validate_token),
):
    orders = order_manager.create(order_data)
    return [map_to_order_external(order) for order in orders]


@router.put("/order/{order_id}/status", response_model=OrderInformationForExternal)
async def update_order_status(
    order_id: UUID,
    order_data: OrderStatusUpdate,
    token=Depends(validate_token),
):
    order = order_manager.update_order_status(order_id, order_data.status)
    return map_to_order_external(order)


@router.delete("/order/{order_id}")
async def delete_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = order_manager.delete(order_id)
    return {"deleted_count": deleted_count}
