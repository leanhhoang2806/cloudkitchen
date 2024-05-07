from src.daos.Ops_DAO import OpsDAO
from src.models.postgres_model import SellerApplication
from uuid import UUID
from typing import List


class OpsManager:
    def __init__(self):
        self.dao = OpsDAO()

    def get_all_seller_application(self) -> List[SellerApplication]:
        return self.dao.get_all_seller_application()

    def update_seller_application(
        self, application_id: UUID, status: str
    ) -> SellerApplication:
        return self.dao.update_seller_application(application_id, status)
