from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import Order
from uuid import UUID
from typing import Optional


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)

    def get_by_buyer_id(self, buyer_id: UUID) -> Optional[Order]:
        return self.dao.get_by_buyer_id(buyer_id)
