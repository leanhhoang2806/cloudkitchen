from src.models.postgres_model import Payment
from src.models.data_model import PaymentUpdate
from src.daos.BaseDAO import GenericDAO
from uuid import UUID
from typing import Optional
from src.daos.database_session import session


class PaymentDAO(GenericDAO):
    def __init__(self) -> None:
        super().__init__(Payment)

    def get_by_seller_id(self, seller_id: UUID) -> Optional[Payment]:
        try:
            return (
                session.query(Payment)
                .filter(Payment.seller_id == str(seller_id))
                .first()
            )
        finally:
            session.close()

    def update_by_email(self, payment_update: PaymentUpdate) -> Optional[Payment]:
        try:
            session.query(Payment).filter(Payment.email == payment_update.email).update(
                payment_update.dict()
            )
            session.commit()
            return (
                session.query(Payment)
                .filter(Payment.email == payment_update.email)
                .first()
            )
        finally:
            session.close()
