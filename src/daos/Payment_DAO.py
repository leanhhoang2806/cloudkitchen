from src.models.postgres_model import Payment
from src.models.data_model import PaymentUpdate
from src.daos.BaseDAO import GenericDAO
from uuid import UUID
from typing import Optional
from src.daos.database_session import provide_session
from sqlalchemy.orm import Session


class PaymentDAO(GenericDAO):
    def __init__(self) -> None:
        super().__init__(Payment)

    @provide_session
    def get_by_seller_id(self, seller_id: UUID, session: Session) -> Optional[Payment]:
        return (
            session.query(Payment).filter(Payment.seller_id == str(seller_id)).first()
        )

    @provide_session
    def update_by_email(
        self, payment_update: PaymentUpdate, session: Session
    ) -> Optional[Payment]:
        session.query(Payment).filter(Payment.email == payment_update.email).update(
            payment_update.dict()
        )
        session.commit()
        return (
            session.query(Payment).filter(Payment.email == payment_update.email).first()
        )
