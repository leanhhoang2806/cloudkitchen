from src.daos.Dish_DAO import DishDAO
from src.managers.generic_manager import GenericManager
from typing import Optional, List
from src.models.postgres_model import Dish
from uuid import UUID


class DishManager(GenericManager):
    def __init__(self):
        super().__init__(DishDAO())

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)

    def get_dishes_paginated(self, skip: int, limit: int) -> Optional[List[Dish]]:
        return self.dao.get_dishes_paginated(skip, limit)

    def search_by_name(self, name: str) -> Optional[List[Dish]]:
        return self.dao.search_by_name(name)

    def search_by_seller_zipcodes(self, zipcodes: List[int]) -> Optional[List[Dish]]:
        return self.dao.search_by_seller_zipcodes(zipcodes)

    def search_by_name_and_zipcode(self, name: str, zipcode: str):
        return self.search_by_zipcode(zipcode)  # make this a placeholder for now

    def update_dish_feature(self, dish_id: UUID, is_featured: bool) -> Dish:
        return self.dao.update_dish_feature(dish_id=dish_id, is_featured=is_featured)

    def get_dishes_by_ids(self, dish_ids: List[UUID]) -> Optional[List[Dish]]:
        return self.dao.get_dishes_by_ids(dish_ids)

    def soft_delete(self, dish_id: UUID) -> Optional[Dish]:
        return self.dao.soft_delete(dish_id)

    def update_dish_quantities(self, dish_id: UUID, quantities: int) -> Dish:
        return self.dao.update_dish_quantities(dish_id, quantities)
