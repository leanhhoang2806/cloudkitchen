from sqlalchemy.orm import Session
from src.daos.BaseDAO import BaseDAO
from src.models.postgres_model import SellerInfo
from src.managers.base_manager import BaseManager


class SellerInfoManager(BaseManager):
    def __init__(self, db: Session):
        dao = BaseDAO(db, SellerInfo)
        super().__init__(db, dao)
