from src.managers.dish_manager import DishManager
from typing import Optional, List
from src.models.postgres_model import Dish


class SearchManager:
    def __init__(self, dish_manager: DishManager) -> None:
        self.dish_manager = dish_manager

    def search_by_name_and_zip(self, name: str, zipcode: str) -> Optional[List[Dish]]:
        return self.dish_manager.search_by_name_and_zip(name, zipcode)
