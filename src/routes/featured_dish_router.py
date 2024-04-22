from fastapi import Depends, Query
from src.validations.validators import validate_token
from src.managers.featured_dish_manager import FeaturedDishManager
from src.managers.dish_manager import DishManager
from src.managers.payment_manager import PaymentManager
from src.models.postgres_model import FeatureDishPydantic, Dish
from src.errors.custom_exceptions import MaximumFeaturedLimit
from uuid import UUID
from src.routes.custom_api_router import CustomAPIRouter
from src.models.data_model import FeaturedDishCreate
from typing import Optional, List


router = CustomAPIRouter()
dish_manager = DishManager()
featured_dish_manager = FeaturedDishManager()
payment_manager = PaymentManager()


@router.get("/featured-dish/", response_model=Optional[List[FeatureDishPydantic]])
async def get_featured_dishes(
    skip: int = Query(0, description="Skip the first N featured dishes"),
    limit: int = Query(10, description="Limit the number of featured dishes returned"),
):
    featured_dishes = featured_dish_manager.get_featured_dish_paginated(
        skip=skip, limit=limit
    )
    return [
        FeatureDishPydantic.from_orm(featured_dish) for featured_dish in featured_dishes
    ]


@router.post("/featured-dish/", response_model=FeatureDishPydantic)
async def add_featured_dish(
    feature_dish: FeaturedDishCreate,
    token=Depends(validate_token),
):
    dish_info: Dish = dish_manager.get(feature_dish.dish_id)
    dish_by_seller: List[Dish] = dish_manager.get_by_seller_id(dish_info.seller_id)
    dish_ids = [dish.id for dish in dish_by_seller]
    featured_dish_count = featured_dish_manager.get_featured_dish_by_dish_id(dish_ids)

    payment_info = payment_manager.get_by_seller_id(dish_info.seller_id)
    # For ecommerce platform, removed len(featured_dish_count) out of the condition
    # "payment_info.dishes_to_feature_limit + len(featured_dish_count)"
    if len(featured_dish_count) > payment_info.dishes_to_feature_limit + len(
        featured_dish_count
    ):
        raise MaximumFeaturedLimit

    featured_dish = featured_dish_manager.create(feature_dish)
    dish_manager.update_dish_feature(feature_dish.dish_id, True)
    return FeatureDishPydantic.from_orm(featured_dish)


@router.delete("/featured-dish/{dish_id}")
async def remove_featured_dish(
    dish_id: UUID,
    token=Depends(validate_token),
):
    deleted_count = featured_dish_manager.delete_by_dish_id(dish_id)
    dish_manager.update_dish_feature(dish_id, False)
    return {"deleted_count": deleted_count}
