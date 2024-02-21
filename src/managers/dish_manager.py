from src.daos.Dish_DAO import DishDAO
from src.managers.generic_manager import GenericManager


class DishManager(GenericManager):
    def __init__(self):
        super().__init__(DishDAO())
