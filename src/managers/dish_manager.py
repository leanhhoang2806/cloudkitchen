from src.daos.Dish_DAO import DishDAO
from src.managers.generic_manager import GenericManager
from typing import Optional, List
from src.models.postgres_model import Dish


class DishManager(GenericManager):
    def __init__(self):
        super().__init__(DishDAO())

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)

    def get_dishes_paginated(self, skip: int, limit: int) -> Optional[List[Dish]]:
        return self.dao.get_dishes_paginated(skip, limit)

    def search_by_name_and_zip(self, name: str, zipcode: str) -> Optional[List[Dish]]:
        return self.dao.search_by_name_and_zip(name, zipcode)