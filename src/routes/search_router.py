from fastapi import Query
from src.managers.dish_manager import DishManager
from src.managers.search_manager import SearchManager
from src.models.postgres_model import DishPydantic
from src.routes.custom_api_router import CustomAPIRouter
from typing import Optional, List

router = CustomAPIRouter()
search_manager = SearchManager(DishManager())


@router.get("/search/", response_model=Optional[List[DishPydantic]])
async def search_dishes(
    seller_name: Optional[str] = Query(..., description="Name of the seller"),
    zip_code: Optional[str] = Query(..., description="Zip code"),
):
    dishes = search_manager.search_by_name_and_zip(seller_name, zip_code)
    return [DishPydantic.from_orm(dish) for dish in dishes]
