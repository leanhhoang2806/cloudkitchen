from src.models.postgres_model import Dish
from src.daos.BaseDAO import GenericDAO

from src.daos.database_session import session


class DishDAO(GenericDAO):
    def __init__(self):
        super().__init__(Dish)

    def get_by_seller_id(self, seller_id):
        try:
            return (
                session.query(self.model)
                .filter(self.model.seller_id == str(seller_id))
                .all()
            )
        finally:
            session.close()
