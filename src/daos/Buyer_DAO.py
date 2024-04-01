from src.models.postgres_model import BuyerInfo
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import session


class BuyerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(BuyerInfo)

    def get_by_email(self, email: str):
        try:
            return (
                session.query(self.model)
                .filter(self.model.email == str(email))
                .order_by(self.model.updated_at.desc())
                .first()
            )
        finally:
            session.close()

    def create_with_email_only(self, email: str):
        try:
            buyer = BuyerInfo(email=email)
            session.add(buyer)
            session.commit()
            session.refresh(buyer)
            return buyer
        finally:
            session.close()
