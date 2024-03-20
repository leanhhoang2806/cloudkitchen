from src.daos.mongo_client import MONGO_DB
from src.models.data_model import ChatRoom, ChatMessage, ChatRoomCreate
from typing import Optional
from bson.objectid import ObjectId
from uuid import UUID
from pydantic import UUID4

COLLECTION_NAME = "seller_buyer_chat"


class ChatDAO:
    def insert_chat(self, conversation_id: str, new_message: ChatMessage) -> None:
        conversations_collection = MONGO_DB[COLLECTION_NAME]
        try:
            update_query = {"_id": conversation_id}

            update_statement = {"$push": {"messages": new_message.dict()}}

            conversations_collection.update_one(update_query, update_statement)

            inserted_doc = conversations_collection.find_one({"_id": conversation_id})
            return ChatRoom(**inserted_doc)
        except Exception as e:
            raise e

    def get_conversation_by_id(self, conversation_id: str) -> Optional[ChatRoom]:
        try:
            conversations_collection = MONGO_DB[COLLECTION_NAME]
            query = {"_id": ObjectId(conversation_id)}

            return conversations_collection.find_one(query)
        except Exception as e:
            raise e

    def create_chat_room(self, chat_room_create: ChatRoomCreate) -> ChatRoom:
        try:
            conversations_collection = MONGO_DB[COLLECTION_NAME]
            chat_room_dict = self._convert_uuids_to_strings(chat_room_create.dict())

            result = conversations_collection.insert_one(chat_room_dict)
            inserted_doc = conversations_collection.find_one(
                {"_id": result.inserted_id}
            )
            # Convert retrieved document into ChatRoom instance
            chat_room = ChatRoom(
                mongo_chat_room_id=str(inserted_doc["_id"]),
                seller_id=UUID4(inserted_doc["seller_id"]),
                buyer_id=UUID4(inserted_doc["buyer_id"]),
            )
            return chat_room
        except Exception as e:
            raise e

    def _convert_uuids_to_strings(self, data_dict):
        converted_data = {}
        for key, value in data_dict.items():
            if isinstance(value, UUID):
                converted_data[key] = str(value)
            else:
                converted_data[key] = value
        return converted_data
