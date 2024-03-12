from src.models.postgres_model import Order, OrdersDish, Dish
from src.models.data_model import OrderCreate, OrderCreateWithBuyerId
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session
from uuid import UUID
from typing import Optional, List
import logging


logging.basicConfig(level=logging.INFO)


class OrderDAO(GenericDAO):
    def __init__(self):
        super().__init__(Order)

    def create_then_add_to_order_dish(self, data: OrderCreate):
        try:
            instance = self.create(OrderCreateWithBuyerId(buyer_id=data.buyer_id))
            [
                session.add(OrdersDish(order_id=instance.id, dish_id=str(dish_id)))
                for dish_id in data.dish_id
            ]
            session.commit()
            return instance
        finally:
            session.close()

    def get_by_seller_id(self, seller_id: UUID) -> Optional[Order]:
        try:
            return (
                session.query(self.model)
                .filter(self.model.seller_id == str(seller_id))
                .all()
            )
        finally:
            session.close()

    def get_by_buyer_id(self, buyer_id: UUID) -> Optional[Order]:
        try:
            return (
                session.query(self.model)
                .filter(self.model.buyer_id == str(buyer_id))
                .all()
            )
        finally:
            session.close()

    def get_order_detail_by_order_id(
        self, order_ids: List[UUID]
    ) -> Optional[List[Dish]]:
        try:
            return (
                session.query(Dish)
                .join(OrdersDish)
                .filter(
                    OrdersDish.order_id.in_([str(order_id) for order_id in order_ids])
                )
                .all()
            )
        finally:
            session.close()

    def update_order_status(self, order_id: UUID, status: str) -> Optional[Order]:
        try:
            session.query(Order).filter(Order.id == str(order_id)).update(
                {"status": status}
            )
            session.commit()
            return session.query(Order).filter(Order.id == str(order_id)).first()
        finally:
            session.close()
