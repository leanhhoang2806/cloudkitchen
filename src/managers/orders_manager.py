from src.daos.Order_DAO import OrderDAO
from src.managers.generic_manager import GenericManager


class OrderManager(GenericManager):
    def __init__(self):
        super().__init__(OrderDAO())

    def get_by_seller_id(self, seller_id):
        return self.dao.get_by_seller_id(seller_id)
