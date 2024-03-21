from src.daos.chat_info_SQL_DAO import ChatInfoDAO
from src.models.postgres_model import ChatInfo
from src.models.data_model import ChatInfoCreate
from src.managers.generic_manager import GenericManager
from uuid import UUID
from typing import Optional, List


class ChatInfoSQLManager(GenericManager):
    def __init__(self):
        super().__init__(ChatInfoDAO())

    def create_if_not_exists(self, chat_info_create: ChatInfoCreate) -> ChatInfoCreate:
        return self.dao.create_if_not_exists(chat_info_create)

    def get_chat_room_by_buyer_id(self, buyer_id: UUID) -> Optional[List[ChatInfo]]:
        return self.dao.get_chat_room_by_buyer_id(buyer_id)

    def get_chat_room_by_seller_id(self, seller_id: UUID) -> Optional[List[ChatInfo]]:
        return self.dao.get_chat_room_by_seller_id(seller_id)
