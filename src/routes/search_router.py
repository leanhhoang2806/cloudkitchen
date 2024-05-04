from fastapi import Query
from src.managers.dish_manager import DishManager
from src.managers.search_manager import SearchManager
from src.managers.seller_manager import SellerInfoManager
from src.models.data_model import DishInformationForExternal
from src.routes.custom_api_router import CustomAPIRouter
from src.models.data_conversion import map_to_dish_external
from typing import Optional, List

router = CustomAPIRouter()
search_manager = SearchManager(DishManager())
seller_manager = SellerInfoManager()


@router.get("/search/", response_model=Optional[List[DishInformationForExternal]])
async def search_dishes(
    seller_name: Optional[str] = Query(..., description="Name of the seller"),
    zip_code: Optional[str] = Query(..., description="Zip code"),
):

    dishes_and_seller = search_manager.search_by_name_and_zip(seller_name, zip_code)

    return [
        map_to_dish_external(dish, seller.name) for dish, seller in dishes_and_seller
    ]
