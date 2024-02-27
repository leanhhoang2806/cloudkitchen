from src.models.postgres_model import Order
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session
from uuid import UUID
from typing import Optional


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
