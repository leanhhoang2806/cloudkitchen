from src.daos.Payment_DAO import PaymentDAO
from src.managers.generic_manager import GenericManager
from uuid import UUID
from typing import Optional
from src.models.postgres_model import Payment
from src.models.data_model import PaymentUpdate


class PaymentManager(GenericManager):
    def __init__(self) -> None:
        super().__init__(PaymentDAO())

    def get_by_seller_id(self, seller_id: UUID) -> Optional[Payment]:
        return self.dao.get_by_seller_id(seller_id)

    def payment_update_by_email(
        self, payment_update: PaymentUpdate
    ) -> Optional[Payment]:
        return self.dao.update_by_email(payment_update)
