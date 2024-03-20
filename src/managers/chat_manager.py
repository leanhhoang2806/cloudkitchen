from src.models.data_model import ChatMessage, ChatRoom, ChatRoomCreate
from src.daos.chat_DAO import ChatDAO
from typing import Optional


class ChatManager:
    def __init__(self) -> None:
        self.dao = ChatDAO()

    def insert_chat(self, conversation_id: str, new_message: ChatMessage) -> None:
        return self.dao.insert_chat(conversation_id, new_message)

    def get_conversation_by_id(self, conversation_id: str) -> Optional[ChatRoom]:
        return self.dao.get_conversation_by_id(conversation_id)

    def create_chat_room(self, chat_room_create: ChatRoomCreate) -> ChatRoom:
        return self.dao.create_chat_room(chat_room_create)
