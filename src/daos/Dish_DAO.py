from src.models.postgres_model import Dish
from src.daos.BaseDAO import GenericDAO


class DishDAO(GenericDAO):
    def __init__(self):
        super().__init__(Dish)
