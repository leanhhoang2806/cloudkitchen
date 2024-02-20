from typing import TypeVar, Generic, Type
from src.models.postgres_model import Base
from src.daos.database_session import session

ModelType = TypeVar("ModelType", bound=Base)


class BaseDAO(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, data):
        try:
            instance = self.model(**data.dict())
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get(self, item_id):
        try:
            return session.query(self.model).filter(self.model.id == item_id).first()
        finally:
            session.close()

    def update(self, item_id, data):
        try:
            instance = (
                session.query(self.model).filter(self.model.id == item_id).first()
            )
            if instance:
                for key, value in data.dict().items():
                    setattr(instance, key, value)
                session.commit()
                session.refresh(instance)
            return instance
        finally:
            session.close()

    def delete(self, item_id):
        try:
            deleted_count = (
                session.query(self.model).filter(self.model.id == item_id).delete()
            )
            session.commit()
            return deleted_count
        finally:
            session.close()
