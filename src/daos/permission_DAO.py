from src.daos.database_session import session
from src.models.postgres_model import Permission
from src.models.data_model import UserPermission
from uuid import UUID
from typing import Optional


class PermissionDAO:
    def get_permission(self, user_email: str) -> Optional[Permission]:
        try:
            return (
                session.query(Permission)
                .filter(Permission.user_email == user_email)
                .first()
            )

        finally:
            session.close()

    def create_permission(self, permission_create: UserPermission) -> Permission:
        try:
            permission_create.permissions.accessible_uuids = [
                str(item) for item in permission_create.permissions.accessible_uuids
            ]
            instance = Permission(**permission_create.dict())
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return (
                session.query(Permission)
                .filter(Permission.user_email == permission_create.user_email)
                .first()
            )

        finally:
            session.close()

    def delete_permission(self, instance_id: UUID) -> Optional[int]:
        try:
            deleted_count = (
                session.query(Permission)
                .filter(Permission.id == str(instance_id))
                .delete()
            )

            session.commit()
            return deleted_count
        finally:
            session.close()

    def remove_permission(self, instance_id: UUID, uuid_to_remove: UUID) -> Permission:
        try:
            instance: Permission = (
                session.query(Permission)
                .filter(Permission.id == str(instance_id))
                .first()
            )
            if instance:
                instance.permissions.accessible_uuids.remove(str(uuid_to_remove))
                session.commit()
                session.refresh(instance)
            return instance
        finally:
            session.close()

    def add_permission(self, email: str, new_accessible_uuid: UUID) -> Permission:
        try:
            instance: Permission = (
                session.query(Permission).filter(Permission.user_email == email).first()
            )
            if instance:
                instance.permissions["accessible_uuids"].append(
                    str(new_accessible_uuid)
                )
                session.commit()
                session.refresh(instance)
            return instance
        finally:
            session.close()
