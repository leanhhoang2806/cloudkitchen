from src.models.postgres_model import FeaturedDish
from src.daos.BaseDAO import GenericDAO
from typing import Optional, List
from src.daos.database_session import session
from uuid import UUID


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

    def delete_by_dish_id(self, dish_id: UUID) -> int:
        try:
            # Perform the delete operation
            deleted_count = (
                session.query(FeaturedDish)
                .filter(FeaturedDish.dish_id == str(dish_id))
                .delete()
            )
            session.commit()  # Commit the transaction
            return deleted_count  # Return the number of deleted records
        finally:
            session.close()  # Close the session
            return 0
