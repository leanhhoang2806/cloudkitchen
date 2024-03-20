from src.models.postgres_model import ChatInfo
from src.daos.BaseDAO import GenericDAO


class ChatInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(ChatInfo)
