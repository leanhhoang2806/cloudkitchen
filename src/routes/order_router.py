from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.orders_manager import OrderManager
from src.managers.buyer_manager import BuyerManager
from src.models.data_model import (
    OrderCreate,
    OrderStatusUpdate,
    OrderInformationForExternal,
)
from src.models.postgres_model import DishPydantic, BuyerInfo, Order
from src.models.data_conversion import map_to_order_external
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
order_manager = OrderManager()
buyer_manager = BuyerManager()


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
    orders: List[Order] = order_manager.get_by_seller_id(seller_id)
    buyer_info: List[BuyerInfo] = [
        buyer_manager.get(order.buyer_id) for order in orders
    ]
    return [
        map_to_order_external(order, buyer.address)
        for order, buyer in zip(orders, buyer_info)
    ]


@router.get("/order/{order_id}", response_model=OrderInformationForExternal)
async def get_order(
    order_id: UUID,
    token=Depends(validate_token),
):
    order: Order = order_manager.get(order_id)
    buyer_info: BuyerInfo = buyer_manager.get(order.buyer_id)
    return map_to_order_external(order, buyer_info.address)


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
    buyer_info: BuyerInfo = buyer_manager.get(order_data.buyer_id)
    return [map_to_order_external(order, buyer_info.address) for order in orders]


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
