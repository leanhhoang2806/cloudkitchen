from src.models.postgres_model import ChatInfo
from src.daos.BaseDAO import GenericDAO
from uuid import UUID
from typing import List, Optional

from src.daos.database_session import session


class ChatInfoDAO(GenericDAO):
    def __init__(self):
        super().__init__(ChatInfo)

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
