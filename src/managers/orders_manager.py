from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import Order, Dish
from uuid import UUID
from typing import Optional, List
from src.models.data_model import OrderCreate, SingleOrderCreate
from src.managers.dish_manager import DishManager

dish_manager = DishManager()


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def create(self, order_create: OrderCreate) -> List[Order]:
        seller_id_by_dish: List[Dish] = [
            dish_manager.get(dish_id) for dish_id in order_create.dish_id
        ]
        return [
            self.dao.create(
                SingleOrderCreate(
                    dish_id=order_create.dish_id[index],
                    buyer_id=order_create.buyer_id,
                    seller_id=seller_id_by_dish[index].seller_id,
                ),
            )
            for index in range(len(order_create.dish_id))
        ]

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

    def get_by_seller_id(self, seller_id: UUID) -> Optional[Order]:
        return self.dao.get_by_seller_id(seller_id)
