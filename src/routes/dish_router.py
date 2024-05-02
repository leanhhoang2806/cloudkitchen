from fastapi import Depends, Query
from src.validations.validators import validate_token
from src.managers.dish_manager import DishManager
from src.models.data_model import DishCreate, DishInformationForExternal
from src.models.postgres_model import Dish
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
dish_manager = DishManager()


def map_to_dish_external(dish_from_db: Dish) -> DishInformationForExternal:
    return DishInformationForExternal(
        id=dish_from_db.id,
        name=dish_from_db.name,
        description=dish_from_db.description,
        price=dish_from_db.price,
        s3_path=dish_from_db.s3_path,
        quantities=dish_from_db.quantities,
        is_featured=dish_from_db.is_featured,
        status=dish_from_db.status,
        created_at=dish_from_db.created_at,
        updated_at=dish_from_db.updated_at,
    )


@router.get(
    "/dish/seller/{seller_id}",
    response_model=Optional[List[DishInformationForExternal]],
)
async def get_dish_by_seller_id(
    seller_id: UUID,
    token=Depends(validate_token),
):
    dishes = dish_manager.get_by_seller_id(seller_id)
    return [map_to_dish_external(dish) for dish in dishes]


@router.get("/dish/{dish_id}", response_model=DishInformationForExternal)
async def get_dish(
    dish_id: UUID,
    token=Depends(validate_token),
):
    dish = dish_manager.get(dish_id)
    return map_to_dish_external(dish)


@router.get("/dish/featured/ids", response_model=List[DishInformationForExternal])
async def get_dishes(dish_ids: str = Query(...)):
    all_ids = dish_ids.split(",")
    dishes = [dish_manager.get(dish_id) for dish_id in all_ids]
    return [map_to_dish_external(dish) for dish in dishes]


@router.get("/dish/", response_model=Optional[List[DishInformationForExternal]])
async def get_dishes_paginated(
    skip: int = Query(0, description="Skip the first N dishes"),
    limit: int = Query(10, description="Limit the number of dishes returned"),
):
    dishes = dish_manager.get_dishes_paginated(skip=skip, limit=limit)
    return [map_to_dish_external(dish) for dish in dishes]


@router.post("/dish/", response_model=DishInformationForExternal)
async def create_dish(
    dish_data: DishCreate,
    token=Depends(validate_token),
):
    dish = dish_manager.create(dish_data)
    return map_to_dish_external(dish)


@router.delete("/dish/{dish_id}", response_model=Optional[DishInformationForExternal])
async def delete_dish(
    dish_id: UUID,
    token=Depends(validate_token),
):
    dish = dish_manager.soft_delete(dish_id)
    return map_to_dish_external(dish)
