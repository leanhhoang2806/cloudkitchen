from src.daos.Seller_DAO import SellerInfoDAO
from src.managers.generic_manager import GenericManager


class SellerInfoManager(GenericManager):
    def __init__(self):
        super().__init__(SellerInfoDAO())
