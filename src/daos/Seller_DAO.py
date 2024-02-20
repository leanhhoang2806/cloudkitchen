from src.daos.database_session import session
from src.models.postgres_model import SellerInfo


class SellerInfoDAO:
    def create(self, data):
        try:
            instance = SellerInfo(**data.dict())
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get(self, seller_info_id):
        try:
            return (
                session.query(SellerInfo)
                .filter(SellerInfo.id == seller_info_id)
                .first()
            )
        finally:
            session.close()

    def update(self, seller_info_id, data):
        try:
            instance = (
                session.query(SellerInfo)
                .filter(SellerInfo.id == seller_info_id)
                .first()
            )
            if instance:
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                session.commit()
                session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, seller_info_id):
        try:
            deleted_count = (
                session.query(SellerInfo)
                .filter(SellerInfo.id == seller_info_id)
                .delete()
            )
            session.commit()
            return deleted_count
        finally:
            session.close()
