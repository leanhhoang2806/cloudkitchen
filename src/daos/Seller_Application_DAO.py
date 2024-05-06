from src.models.postgres_model import SellerApplication
from src.daos.BaseDAO import GenericDAO
from typing import Optional
from src.daos.database_session import provide_session
from sqlalchemy.orm import Session


class SellerApplicationDAO(GenericDAO):
    def __init__(self) -> None:
        super().__init__(SellerApplication)

    @provide_session
    def get_by_email(self, email: str, session: Session) -> Optional[SellerApplication]:
        return (
            session.query(SellerApplication)
            .filter(SellerApplication.email == email)
            .first()
        )
