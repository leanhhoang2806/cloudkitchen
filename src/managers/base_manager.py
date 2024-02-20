from sqlalchemy.orm import Session
from src.daos.BaseDAO import BaseDAO


class BaseManager:
    def __init__(self, db: Session, dao: BaseDAO):
        self.dao = dao(db)

    def create(self, data):
        return self.dao.create(data)

    def get(self, item_id):
        return self.dao.get(item_id)

    def update(self, item_id, data):
        return self.dao.update(item_id, data)

    def delete(self, item_id):
        return self.dao.delete(item_id)
