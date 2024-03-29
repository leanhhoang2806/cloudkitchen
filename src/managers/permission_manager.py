from src.daos.permission_DAO import PermissionDAO
from src.models.data_model import UserPermission
from src.models.postgres_model import Permission
from uuid import UUID
from typing import Optional


class PermissionManager:
    def __init__(self) -> None:
        self.dao = PermissionDAO()

    def is_authorized_to_access(self, user_email: str, target_uuid: UUID) -> bool:
        permission = self.dao.get_permission(user_email)
        is_found = False
        for item in permission:
            if item == str(target_uuid):
                is_found = True
        return is_found

    def create(self, user_permission_create: UserPermission) -> Permission:
        return self.dao.create_permission(user_permission_create)

    def delete(self, instance_id: UUID) -> int:
        return self.dao.delete_permission(instance_id)

    def add_permission(self, email: str, new_uuid: UUID) -> Permission:
        return self.dao.add_permission(email, new_uuid)

    def remove_permission(self, instance_id: UUID, uuid_to_remove: UUID) -> Permission:
        return self.dao.remove_permission(instance_id, uuid_to_remove)

    def get_by_email(self, email: str) -> Optional[Permission]:
        return self.dao.get_permission(email)
