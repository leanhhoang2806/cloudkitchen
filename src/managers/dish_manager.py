from src.daos.Dish_DAO import DishDAO
from src.managers.generic_manager import GenericManager


class DishManager(GenericManager):
    def __init__(self):
        super().__init__(DishDAO())

    def get_by_seller_id(self, seller_id):
        self.dao.get_by_seller_id(seller_id)
        return self.dao.get_by_seller_id(seller_id)
