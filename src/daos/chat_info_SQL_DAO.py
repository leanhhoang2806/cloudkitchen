from src.models.postgres_model import ChatInfo
from src.models.data_model import ChatInfoCreate
from src.daos.BaseDAO import GenericDAO
from uuid import UUID
from typing import List, Optional

from src.daos.database_session import session


class ChatInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(ChatInfo)

    def create_if_not_exists(self, chat_info_create: ChatInfoCreate) -> None:
        try:
            existing_instance = (
                session.query(ChatInfo)
                .filter(ChatInfo.conversation_id == chat_info_create.conversation_id)
                .first()
            )
            if existing_instance:
                return existing_instance
            data_dict = self._convert_uuids_to_strings(chat_info_create.dict())
            instance = ChatInfo(**data_dict)
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
        finally:
            session.close()

    def get_chat_room_by_buyer_id(self, buyer_id: UUID) -> Optional[List[ChatInfo]]:
        try:
            return (
                session.query(ChatInfo).filter(ChatInfo.buyer_id == str(buyer_id)).all()
            )

        finally:
            session.close()

    def get_chat_room_by_seller_id(self, seller_id: UUID) -> Optional[List[ChatInfo]]:
        try:
            return (
                session.query(ChatInfo)
                .filter(ChatInfo.seller_id == str(seller_id))
                .all()
            )

        finally:
            session.close()
