from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import Order, Dish
from uuid import UUID
from typing import Optional, List
from src.models.data_model import OrderCreate, SingleOrderCreate


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def create(self, data: OrderCreate) -> List[Order]:
        return [
            self.dao.create(SingleOrderCreate(dish_id=dish_id, buyer_id=data.buyer_id))
            for dish_id in data.dish_id
        ]

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)

    def get_by_buyer_id(self, buyer_id: UUID) -> Optional[Order]:
        return self.dao.get_by_buyer_id(buyer_id)

    def get_order_detail_by_order_id(
        self, order_ids: List[UUID]
    ) -> Optional[List[Dish]]:
        return self.dao.get_order_detail_by_order_id(order_ids)

    def update_order_status(self, order_id: UUID, status: str) -> Optional[Order]:
        return self.dao.update_order_status(order_id, status)

    def get_dish_by_order_id(self, order_id: UUID) -> Optional[List[Dish]]:
        return self.dao.get_dish_by_order_id(order_id)
