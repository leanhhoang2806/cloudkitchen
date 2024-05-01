from src.models.postgres_model import SellerInfo
from src.models.postgres_model import Dish
from src.daos.BaseDAO import GenericDAO
from typing import Optional
from src.daos.database_session import provide_session
from uuid import UUID
from sqlalchemy.orm import Session


class SellerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(SellerInfo)

    @provide_session
    def get_by_email(self, email: str, session: Session) -> Optional[SellerInfo]:
        return session.query(self.model).filter(self.model.email == str(email)).first()

    @provide_session
    def get_seller_name_by_dish_id(
        self, dish_id: UUID, session: Session
    ) -> Optional[SellerInfo]:
        return session.query(SellerInfo).join(Dish).filter(Dish.id == dish_id).first()
