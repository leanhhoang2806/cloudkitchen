from src.daos.Featured_Dish_DAO import FeaturedDishDAO
from src.models.postgres_model import FeaturedDish
from src.managers.generic_manager import GenericManager
from typing import Optional, List


class FeaturedDishManager(GenericManager):
    def __init__(self):
        super().__init__(FeaturedDishDAO())

    def get_featured_dish_paginated(
        self, skip: int, limit: int
    ) -> Optional[List[FeaturedDish]]:
        return self.dao.get_featured_dish_paginated(skip, limit)
