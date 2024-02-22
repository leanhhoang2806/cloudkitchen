from src.daos.Buyer_DAO import BuyerInfoDAO
from src.managers.generic_manager import GenericManager


class BuyerManager(GenericManager):
    def __init__(self):
        super().__init__(BuyerInfoDAO())
