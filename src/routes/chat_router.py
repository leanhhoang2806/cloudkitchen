from fastapi import Depends, Path
from src.validations.validators import validate_token
from src.routes.custom_api_router import CustomAPIRouter
from src.models.data_model import ChatRoomCreate, ChatMessage, ChatInfoCreate
from src.models.postgres_model import ChatInfoPydantic
from src.managers.chat_manager import ChatManager
from src.managers.chat_info_sql_manager import ChatInfoSQLManager
from typing import Optional, List

from uuid import UUID

router = CustomAPIRouter()
chat_manager = ChatManager()
chat_info_SQL_manager = ChatInfoSQLManager()


@router.post("/chat", response_model=ChatRoomCreate)
async def create_chat_room(
    payload: ChatRoomCreate,
    token=Depends(validate_token),
):
    result = chat_manager.create_chat_room(payload)
    chat_info_SQL_manager.create_if_not_exists(
        ChatInfoCreate(
            seller_id=payload.seller_id,
            buyer_id=payload.buyer_id,
            conversation_id=result.mongo_chat_room_id,
        )
    )
    return result


@router.get("/chat/{conversation_id}", response_model=ChatRoomCreate)
async def get_chat_room_by_id(
    conversation_id: str,
    token=Depends(validate_token),
):
    return chat_manager.get_conversation_by_id(conversation_id)


@router.get("/chat/buyer/{buyer_id}", response_model=Optional[List[ChatInfoPydantic]])
async def get_chat_room_by_buyer_id(
    buyer_id: UUID,
    token=Depends(validate_token),
):

    chat_info = chat_info_SQL_manager.get_chat_room_by_buyer_id(buyer_id)
    return [ChatInfoPydantic.from_orm(chat) for chat in chat_info]


@router.get("/chat/seller/{seller_id}", response_model=Optional[List[ChatInfoPydantic]])
async def get_chat_room_by_seller_id(
    seller_id: UUID,
    token=Depends(validate_token),
):
    chat_info = chat_info_SQL_manager.get_chat_room_by_seller_id(seller_id)
    return [ChatInfoPydantic.from_orm(chat) for chat in chat_info]


@router.post("/chat/{chat_id}")
async def post_message(
    payload: ChatMessage,
    chat_id: str = Path(...),
    token=Depends(validate_token),
):
    return chat_manager.insert_chat(chat_id, payload)
