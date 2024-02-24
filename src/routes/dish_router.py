from fastapi import Depends
from src.validations.validators import validate_token
from src.managers.dish_manager import DishManager
from src.models.data_model import DishCreate, DishUpdate
from src.models.postgres_model import DishPydantic
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
dish_manager = DishManager()


@router.get("/dish/seller/{seller_id}", response_model=Optional[List[DishPydantic]])
async def get_dish_by_seller_id(
    seller_id: UUID,
    token=Depends(validate_token),
):
    dishes = dish_manager.get_by_seller_id(seller_id)
    if not dishes:
        return None
    return [DishPydantic.from_orm(dish) for dish in dishes]


@router.get("/dish/{dish_id}", response_model=DishPydantic)
async def get_dish(
    dish_id: UUID,
    token=Depends(validate_token),
):
    dish = dish_manager.get(dish_id)
    return DishPydantic.from_orm(dish)


@router.post("/dish/", response_model=DishPydantic)
async def create_dish(
    dish_data: DishCreate,
    token=Depends(validate_token),
):
    dish = dish_manager.create(dish_data)
    return DishPydantic.from_orm(dish)


@router.put("/dish/{dish_id}", response_model=DishPydantic)
async def update_dish(
    dish_id: UUID,
    dish_data: DishUpdate,
    token=Depends(validate_token),
):
    dish = dish_manager.update(dish_id, dish_data)
    return DishPydantic.from_orm(dish)


@router.delete("/dish/{dish_id}")
async def delete_dish(
    dish_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = dish_manager.delete(dish_id)
    return {"deleted_count": deleted_count}
