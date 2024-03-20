from src.daos.chat_info_SQL_DAO import ChatInfoDAO

from src.managers.generic_manager import GenericManager


class ChatInfoSQLManager(GenericManager):
    def __init__(self):
        super().__init__(ChatInfoDAO())
