from src.models.postgres_model import Dish, SellerInfo
from src.daos.BaseDAO import GenericDAO
from typing import Optional, List
from src.daos.database_session import session
from sqlalchemy import or_, and_
from uuid import UUID
from sqlalchemy import update
from src.enums.status import Status


class DishDAO(GenericDAO):
    def __init__(self):
        super().__init__(Dish)

    def get_by_seller_id(self, seller_id):
        try:
            return (
                session.query(Dish).filter(and_(Dish.seller_id == str(seller_id), Dish.status == Status.ACTIVE)).all()
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

    def update_dish_feature(self, dish_id: UUID, is_featured: bool) -> Dish:
        try:
            session.execute(
                update(Dish)
                .where(Dish.id == str(dish_id))
                .values(is_featured=is_featured)
            )
            # Commit the transaction
            session.commit()

            # Retrieve and return the updated Dish object
            return session.query(Dish).filter(Dish.id == str(dish_id)).first()
        finally:
            session.close()

    def get_dishes_by_ids(self, dish_ids: List[UUID]) -> Optional[List[Dish]]:
        try:
            # Query dishes based on the provided list of dish IDs
            dishes = (
                session.query(self.model)
                .filter(self.model.id.in_([str(dish_id) for dish_id in dish_ids]))
                .all()
            )
            return dishes
        finally:
            session.close()

    def search_by_seller_zipcodes(self, zipcodes: List[int]) -> Optional[List[Dish]]:
        try:
            zipcodeds_str = [str(zipcode) for zipcode in zipcodes]
            dishes = (
                session.query(Dish)
                .join(SellerInfo)
                .filter(SellerInfo.zipcode.in_(zipcodeds_str))
                .all()
            )
            return dishes
        finally:
            session.close()

    def soft_delete(self, dish_id: UUID) -> Optional[Dish]:
        try:
            session.execute(
                update(Dish)
                .where(Dish.id == str(dish_id))
                .values(status=Status.SOFT_DELETE)
            )
            session.commit()
            return session.query(Dish).filter(Dish.id == str(dish_id)).first()
        finally:
            session.close()
