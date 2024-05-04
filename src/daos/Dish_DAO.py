from src.models.postgres_model import Dish, SellerInfo
from src.daos.BaseDAO import GenericDAO
from typing import Optional, List
from src.daos.database_session import provide_session
from sqlalchemy import or_, and_
from uuid import UUID
from sqlalchemy import update
from src.enums.status import Status
from sqlalchemy.orm import Session


class DishDAO(GenericDAO):
    def __init__(self):
        super().__init__(Dish)

    @provide_session
    def update_dish_quantities(
        self, dish_id: UUID, quantities: int, session: Session
    ) -> Dish:

        session.query(Dish).filter(Dish.id == str(dish_id)).update(
            {Dish.quantities: Dish.quantities - quantities}
        )
        session.commit()
        return session.query(Dish).filter(Dish.id == str(dish_id)).first()

    @provide_session
    def get_by_seller_id(self, seller_id: UUID, session: Session):
        return (
            session.query(Dish)
            .filter(
                and_(Dish.seller_id == str(seller_id), Dish.status == Status.ACTIVE)
            )
            .all()
        )

    @provide_session
    def get_dishes_paginated(
        self, skip: int, limit: int, session: Session
    ) -> Optional[List[Dish]]:
        return (
            session.query(Dish)
            .filter(Dish.status == Status.ACTIVE)
            .offset(skip)
            .limit(limit)
            .order_by(Dish.updated_at.desc())
            .all()
        )

    @provide_session
    def search_by_name_and_zip(
        self, seller_name: str, zipcode: str, session: Session
    ) -> Optional[List[Dish]]:
        return (
            session.query(Dish)
            .join(SellerInfo)
            .filter(or_(SellerInfo.name == seller_name, SellerInfo.address == zipcode))
            .order_by(Dish.updated_at.desc())
            .all()
        )

    @provide_session
    def update_dish_feature(
        self, dish_id: UUID, is_featured: bool, session: Session
    ) -> Dish:
        session.execute(
            update(Dish).where(Dish.id == str(dish_id)).values(is_featured=is_featured)
        )
        # Commit the transaction
        session.commit()

        # Retrieve and return the updated Dish object
        return session.query(Dish).filter(Dish.id == str(dish_id)).first()

    @provide_session
    def get_dishes_by_ids(
        self, dish_ids: List[UUID], session: Session
    ) -> Optional[List[Dish]]:
        return (
            session.query(self.model)
            .filter(self.model.id.in_([str(dish_id) for dish_id in dish_ids]))
            .order_by(self.model.updated_at.desc())
            .all()
        )

    @provide_session
    def search_by_seller_zipcodes(
        self, zipcodes: List[int], session: Session
    ) -> Optional[List[Dish]]:
        zipcodeds_str = [str(zipcode) for zipcode in zipcodes]
        dishes = (
            session.query(Dish, SellerInfo)
            .join(SellerInfo)
            .filter(SellerInfo.zipcode.in_(zipcodeds_str), Dish.status == Status.ACTIVE)
            .order_by(Dish.updated_at.desc())
            .all()
        )
        return dishes

    @provide_session
    def soft_delete(self, dish_id: UUID, session: Session) -> Optional[Dish]:
        session.execute(
            update(Dish)
            .where(Dish.id == str(dish_id))
            .values(status=Status.SOFT_DELETE)
        )
        session.commit()
        return session.query(Dish).filter(Dish.id == str(dish_id)).first()
