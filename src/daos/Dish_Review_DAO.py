from src.models.postgres_model import DishReview
from src.models.data_model import DishReviewCreate
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session
from typing import List, Optional
from uuid import UUID
from sqlalchemy import func, desc, and_



class DishReviewDAO(GenericDAO):
    def __init__(self):
        super().__init__(DishReview)

    def create_if_not_exists(self, dish_review_create: DishReview) -> None:
        try:
            existing_instance = (
                session.query(DishReview).filter(and_(DishReview.buyer_id == dish_review_create.buyer_id, DishReview.dish_id == dish_review_create.dish_id)).first()
            )

            if existing_instance: return existing_instance
            data_dict = self._convert_uuids_to_strings(dish_review_create.dict())
            instance = DishReview(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get_by_dish_id(self, dish_id: UUID) -> Optional[List[DishReview]]:
        try:
            return (
                session.query(DishReview)
                .filter(DishReview.dish_id == str(dish_id))
                .order_by(desc(DishReview.created_at))
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
