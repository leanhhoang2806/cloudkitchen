from src.models.postgres_model import FeaturedDish
from src.daos.BaseDAO import GenericDAO
from typing import Optional, List
from src.daos.database_session import session


class FeaturedDishDAO(GenericDAO):
    def __init__(self):
        super().__init__(FeaturedDish)

    def get_featured_dish_paginated(
        self, skip: int, limit: int
    ) -> Optional[List[FeaturedDish]]:
        try:
            return session.query(self.model).offset(skip).limit(limit).all()
        finally:
            session.close()
