from src.daos.Discount_Dish_DAO import DiscountDishDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import DiscountedDish
from uuid import UUID
from typing import Optional


class DiscountedDishManager(GenericManager):
    def __init__(self) -> None:
        super().__init__(DiscountDishDAO())

    def get_discounted_dish_by_dish_id(self, dish_id: UUID) -> Optional[DiscountedDish]:
        return self.dao.get_discounted_dish_by_dish_id(dish_id)

    def delete_discounted_dish_by_dish_id(self, dish_id: UUID) -> Optional[int]:
        return self.dao.delete_discounted_dish_by_dish_id(dish_id)
