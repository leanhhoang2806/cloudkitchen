from src.models.postgres_model import SellerInfo
from src.models.postgres_model import Dish
from src.daos.BaseDAO import GenericDAO
from typing import Optional
from src.daos.database_session import session
from uuid import UUID


class SellerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(SellerInfo)

    def get_by_email(self, email: str) -> Optional[SellerInfo]:
        try:
            return (
                session.query(self.model).filter(self.model.email == str(email)).first()
            )
        finally:
            session.close()

    def get_seller_name_by_dish_id(self, dish_id: UUID) -> Optional[SellerInfo]:
        try:
            return (
                session.query(SellerInfo).join(Dish).filter(Dish.id == dish_id).first()
            )

        finally:
            session.close()
