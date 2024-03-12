from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import Order, Dish
from uuid import UUID
from typing import Optional, List


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def create(self, data):
        return self.dao.create_then_add_to_order_dish(data)

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)

    def get_by_buyer_id(self, buyer_id: UUID) -> Optional[Order]:
        return self.dao.get_by_buyer_id(buyer_id)

    def get_order_detail_by_order_id(self, order_id: UUID) -> Optional[List[Dish]]:
        return self.dao.get_order_detail_by_order_id(order_id)
