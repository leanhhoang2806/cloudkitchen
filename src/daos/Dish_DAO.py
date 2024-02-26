from src.models.postgres_model import Dish, SellerInfo
from src.daos.BaseDAO import GenericDAO
from typing import Optional, List
from src.daos.database_session import session
from sqlalchemy import or_


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

    def get_dishes_paginated(self, skip: int, limit: int) -> Optional[List[Dish]]:
        try:
            return session.query(self.model).offset(skip).limit(limit).all()
        finally:
            session.close()

    def search_by_name_and_zip(
        self, seller_name: str, zipcode: str
    ) -> Optional[List[Dish]]:
        try:
            dishes = (
                session.query(Dish)
                .join(SellerInfo)
                .filter(
                    or_(SellerInfo.name == seller_name, SellerInfo.address == zipcode)
                )
                .all()
            )
            return dishes

        finally:
            session.close()
