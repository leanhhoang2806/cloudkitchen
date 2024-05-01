from src.models.postgres_model import BuyerInfo
from src.daos.BaseDAO import GenericDAO
from src.daos.database_session import provide_session
from sqlalchemy.orm import Session


class BuyerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(BuyerInfo)

    @provide_session
    def get_by_email(self, email: str, session: Session):
        return (
            session.query(self.model)
            .filter(self.model.email == str(email))
            .order_by(self.model.updated_at.desc())
            .first()
        )

    @provide_session
    def create_with_email_only(self, email: str, session: Session):
        buyer = BuyerInfo(email=email)
        session.add(buyer)
        session.commit()
        session.refresh(buyer)
        return buyer
