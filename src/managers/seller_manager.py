from src.daos.Seller_DAO import SellerInfoDAO
from src.managers.generic_manager import GenericManager
from typing import Optional
from src.models.postgres_model import SellerInfo


class SellerInfoManager(GenericManager):
    def __init__(self):
        super().__init__(SellerInfoDAO())

    def get_by_email(self, seller_email: str) -> Optional[SellerInfo]:
        return self.dao.get_by_email(seller_email)
