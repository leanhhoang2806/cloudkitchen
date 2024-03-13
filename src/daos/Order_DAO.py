from src.models.postgres_model import Order
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session
from uuid import UUID
from typing import Optional
import logging


logging.basicConfig(level=logging.INFO)


class OrderDAO(GenericDAO):
    def __init__(self):
        super().__init__(Order)

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

    def update_order_status(self, order_id: UUID, status: str) -> Optional[Order]:
        try:
            session.query(Order).filter(Order.id == str(order_id)).update(
                {"status": status}
            )
            session.commit()
            return session.query(Order).filter(Order.id == str(order_id)).first()
        finally:
            session.close()
