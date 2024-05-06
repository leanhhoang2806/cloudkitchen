from src.daos.Seller_Application_DAO import SellerApplicationDAO
from src.managers.generic_manager import GenericManager
from src.models.postgres_model import SellerApplication
from typing import Optional


class SellerApplicationManager(GenericManager):
    def __init__(self):
        super().__init__(SellerApplicationDAO())

    def get_by_email(self, email: str) -> Optional[SellerApplication]:
        return self.dao.get_by_email(email)
