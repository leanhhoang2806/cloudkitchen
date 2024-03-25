from src.managers.generic_manager import GenericManager
from src.daos.Dish_Review_DAO import DishReviewDAO
from src.models.postgres_model import DishReview
from uuid import UUID
from typing import List, Optional


class DishReviewManager(GenericManager):
    def __init__(self):
        super().__init__(DishReviewDAO())

    def get_by_dish_id(self, dish_id: UUID) -> Optional[List[DishReview]]:
        return self.dao.get_by_dish_id(dish_id)

    def get_dish_review_rating_summary(self, dish_id: UUID) -> Optional[float]:
        rating = self.dao.get_dish_review_rating_summary(dish_id)
        return round(rating, 1) if rating else 0
