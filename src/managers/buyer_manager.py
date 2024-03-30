from src.daos.Buyer_DAO import BuyerInfoDAO
from src.models.data_model import UserPermission, GenericPermission
from src.managers.generic_manager import GenericManager
from src.managers.permission_manager import PermissionManager
from uuid import UUID


permission_manager = PermissionManager()


class BuyerManager(GenericManager):
    def __init__(self):
        super().__init__(BuyerInfoDAO())

    def get_by_email(self, email):
        buyer = self.dao.get_by_email(email)
        if not buyer:
            buyer = self.dao.create_with_email_only(email)
            permission_manager.create(
                UserPermission(
                    user_email=email,
                    permissions=GenericPermission(accessible_uuids=[buyer.id]),
                )
            )
        return buyer

    def is_address_exist(self, buyer_id: UUID) -> bool:
        buyer = self.dao.get(buyer_id)
        return True if buyer.address else False
