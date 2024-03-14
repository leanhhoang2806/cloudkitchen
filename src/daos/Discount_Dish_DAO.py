from src.daos.BaseDAO import GenericDAO
from src.models.postgres_model import DiscountedDish
from typing import Optional
from uuid import UUID
from src.daos.database_session import session


class DiscountDishDAO(GenericDAO):
    def __init__(self):
        super().__init__(DiscountedDish)

    def get_discounted_dish_by_dish_id(self, dish_id: UUID) -> Optional[DiscountedDish]:
        try:
            return (
                session.query(DiscountedDish)
                .filter(DiscountedDish.dish_id == str(dish_id))
                .first()
            )

        finally:
            session.close()

    def delete_discounted_dish_by_dish_id(self, dish_id: UUID) -> Optional[int]:
        try:
            delete_count = (
                session.query(DiscountedDish)
                .filter(DiscountedDish.dish_id == str(dish_id))
                .delete()
            )

            session.commit()
            return delete_count
        finally:
            session.close()
