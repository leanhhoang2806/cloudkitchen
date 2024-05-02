from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import Order, Dish
from uuid import UUID
from typing import Optional, List
from src.models.data_model import OrderCreate, SingleOrderCreate
from src.managers.all_managers import ALL_MANAGER
from src.errors.custom_exceptions import (
    BuyerMustUpdateAddressBeforeOrderError,
    DishDoesNotHaveEnoughToSell,
)
import logging

dish_manager = ALL_MANAGER.dish_manager
buyer_manager = ALL_MANAGER.buyer_manager


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def create(self, order_create: OrderCreate) -> List[Order]:
        if not (buyer_manager.is_address_exist(order_create.buyer_id)):
            raise BuyerMustUpdateAddressBeforeOrderError
        seller_id_by_dish: List[Dish] = [
            dish_manager.get(dish_id) for dish_id in order_create.dish_id
        ]
        requested_dish_quantities_map = {
            str(dish_id): count
            for dish_id, count in zip(order_create.dish_id, order_create.quantities)
        }
        for dish in seller_id_by_dish:
            if dish.quantities < requested_dish_quantities_map[str(dish.id)]:
                raise DishDoesNotHaveEnoughToSell
        result = [
            self.dao.create(
                SingleOrderCreate(
                    dish_id=order_create.dish_id[index],
                    buyer_id=order_create.buyer_id,
                    seller_id=seller_id_by_dish[index].seller_id,
                ),
            )
            for index in range(len(order_create.dish_id))
        ]
        logging.error("result")
        logging.error(result)

        # Reduce quantities
        for dish_id, requested_quantities in requested_dish_quantities_map.items():
            dish_manager.update_dish_quantities(dish_id, requested_quantities)
        return result

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
