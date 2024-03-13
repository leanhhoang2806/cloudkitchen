from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.orders_manager import OrderManager
from src.models.data_model import OrderCreate, OrderStatusUpdate
from src.models.postgres_model import OrderPydantic, DishPydantic
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
order_manager = OrderManager()


@router.get("/order/buyer/{buyer_id}", response_model=Optional[List[OrderPydantic]])
async def get_order_by_buyer_id(
    buyer_id: UUID,
    token=Depends(validate_token),
):
    orders = order_manager.get_by_buyer_id(buyer_id)
    return [OrderPydantic.from_orm(order) for order in orders]


@router.get("/order/{order_id}", response_model=OrderPydantic)
async def get_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    order = order_manager.get(order_id)
    return OrderPydantic.from_orm(order)


@router.get("/order/{order_id}/dish", response_model=Optional[List[DishPydantic]])
async def get_dish_by_order_id(
    order_id: UUID,
    token=Depends(validate_token),
):
    dishes = order_manager.get_dish_by_order_id(order_id)
    return [DishPydantic.from_orm(dish) for dish in dishes]


@router.post("/order/", response_model=List[OrderPydantic])
async def create_order(
    order_data: OrderCreate,
    token=Depends(validate_token),
):
    orders = order_manager.create(order_data)
    return [OrderPydantic.from_orm(order) for order in orders]


@router.put("/order/{order_id}/status", response_model=OrderPydantic)
async def update_order_status(
    order_id: UUID,
    order_data: OrderStatusUpdate,
    token=Depends(validate_token),
):
    order = order_manager.update_order_status(order_id, order_data.status)
    return OrderPydantic.from_orm(order)


@router.delete("/order/{order_id}")
async def delete_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = order_manager.delete(order_id)
    return {"deleted_count": deleted_count}
