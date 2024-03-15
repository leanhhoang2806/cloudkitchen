from fastapi import Depends, Response, status
from uuid import UUID
from src.validations.validators import validate_token
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional
from src.managers.discounted_dish_manager import DiscountedDishManager
from src.models.postgres_model import DiscountedDishPydantic
from src.models.data_model import DiscountedDishCreate, DiscountedDishUpdate


router = CustomAPIRouter()
discounted_dish_manager = DiscountedDishManager()


@router.get(
    "/discounted-dish/dish/{dish_id}",
    response_model=Optional[DiscountedDishPydantic],
)
async def get_discounted_dish_by_dish_id(dish_id: UUID):
    discounted_dish = discounted_dish_manager.get_discounted_dish_by_dish_id(dish_id)
    return (
        DiscountedDishPydantic.from_orm(discounted_dish)
        if discounted_dish
        else Response(status_code=status.HTTP_204_NO_CONTENT)
    )


@router.get(
    "/discounted-dish/{discounted_dish_id}",
    response_model=Optional[DiscountedDishPydantic],
)
async def get_discounted_dish(
    discounted_dish_id: UUID,
    token=Depends(validate_token),
):
    discounted_dish = discounted_dish_manager.get(discounted_dish_id)
    return DiscountedDishPydantic.from_orm(discounted_dish)


@router.post("/discounted-dish/", response_model=DiscountedDishPydantic)
async def create_discounted_dish(
    discounted_dish_data: DiscountedDishCreate,
    token=Depends(validate_token),
):
    discounted_dish = discounted_dish_manager.create(discounted_dish_data)
    return DiscountedDishPydantic.from_orm(discounted_dish)


@router.put(
    "/discounted-dish/{discounted_dish_id}", response_model=DiscountedDishPydantic
)
async def update_discounted_dish(
    discounted_dish_id: UUID,
    discounted_dish_data: DiscountedDishUpdate,
    token=Depends(validate_token),
):
    discounted_dish = discounted_dish_manager.update(
        discounted_dish_id, discounted_dish_data
    )
    return DiscountedDishPydantic.from_orm(discounted_dish)


@router.delete("/discounted-dish/{discounted_dish_id}")
async def delete_discounted_dish(
    discounted_dish_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = discounted_dish_manager.delete(discounted_dish_id)
    return {"deleted_count": deleted_count}


@router.delete("/discounted-dish/dish/{dish_id}")
async def delete_discounted_dish_by_dish_id(
    dish_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = discounted_dish_manager.delete_discounted_dish_by_dish_id(dish_id)
    return {"deleted_count": deleted_count}
