from src.models.postgres_model import BuyerInfo
from src.daos.BaseDAO import GenericDAO


class BuyerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(BuyerInfo)
