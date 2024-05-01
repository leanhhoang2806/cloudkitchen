from src.daos.BaseDAO import GenericDAO
from src.models.postgres_model import DiscountedDish
from typing import Optional
from uuid import UUID
from src.daos.database_session import provide_session
from sqlalchemy.orm import Session


class DiscountDishDAO(GenericDAO):
    def __init__(self):
        super().__init__(DiscountedDish)

    @provide_session
    def get_discounted_dish_by_dish_id(
        self, dish_id: UUID, session: Session
    ) -> Optional[DiscountedDish]:

        return (
            session.query(DiscountedDish)
            .filter(DiscountedDish.dish_id == str(dish_id))
            .order_by(DiscountedDish.updated_at.desc())
            .first()
        )

    @provide_session
    def delete_discounted_dish_by_dish_id(
        self, dish_id: UUID, session: Session
    ) -> Optional[int]:
        delete_count = (
            session.query(DiscountedDish)
            .filter(DiscountedDish.dish_id == str(dish_id))
            .delete()
        )

        session.commit()
        return delete_count
