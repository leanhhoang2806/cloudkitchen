from src.daos.Orders_dish_DAO import OrdersDishDAO
from uuid import UUID
from typing import List
from src.models.postgres_model import Order


class OrderDishManager:
    def __init__(self) -> None:
        self.dao = OrdersDishDAO

    def get_order_for_seller(self, seller_id: UUID) -> List[Order]:
        return self.dao.get_order_for_seller(seller_id)
