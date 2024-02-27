from src.models.postgres_model import SellerInfo
from src.daos.BaseDAO import GenericDAO
from typing import Optional
from src.daos.database_session import session


class SellerInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(SellerInfo)

    def get_by_email(self, email: str) -> Optional[SellerInfo]:
        try:
            return (
                session.query(self.model).filter(self.model.email == str(email)).first()
            )
        finally:
            session.close()
