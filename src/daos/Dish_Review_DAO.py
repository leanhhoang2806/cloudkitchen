from src.models.postgres_model import DishReview
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func


class DishReviewDAO(GenericDAO):
    def __init__(self):
        super().__init__(DishReview)

    def get_by_dish_id(self, dish_id: UUID) -> Optional[List[DishReview]]:
        try:
            return (
                session.query(DishReview)
                .filter(DishReview.dish_id == str(dish_id))
                .all()
            )
        finally:
            session.close()

    def get_dish_review_rating_summary(self, dish_id: UUID) -> Optional[float]:
        try:
            return (
                session.query(func.avg(DishReview.rating))
                .filter(DishReview.dish_id == str(dish_id))
                .scalar()
            )
        finally:
            session.close()
