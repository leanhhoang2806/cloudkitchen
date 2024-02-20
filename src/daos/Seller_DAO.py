from src.models.postgres_model import SellerInfo
from src.daos.BaseDAO import GenericDAO


class SellerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(SellerInfo)
