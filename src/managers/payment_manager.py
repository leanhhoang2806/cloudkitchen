from src.daos.Payment_DAO import PaymentDAO
from src.managers.generic_manager import GenericManager
from uuid import UUID
from typing import Optional
from src.models.postgres_model import Payment


class PaymentManager(GenericManager):
    def __init__(self) -> None:
        super().__init__(PaymentDAO())

    def get_by_seller_id(self, seller_id: UUID) -> Optional[Payment]:
        return self.dao.get_by_seller_id(seller_id)
