from fastapi import Depends
from src.validations.validators import validate_token
from src.routes.custom_api_router import CustomAPIRouter
from src.models.data_model import ChatRoomCreate, ChatRoom, ChatMessage, ChatInfoCreate
from src.managers.chat_manager import ChatManager
from src.managers.chat_info_sql_manager import ChatInfoSQLManager

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
    chat_info_SQL_manager.create(
        ChatInfoCreate(
            seller_id=payload.seller_id,
            buyer_id=payload.buyer_id,
            conversation_id=result.mongo_chat_room_id,
        )
    )
    return result


@router.get("/chat/{chat_id}", response_model=ChatRoom)
async def get_chat_room_by_id(
    chat_id: UUID,
    token=Depends(validate_token),
):
    return chat_manager.get_conversation_by_id(chat_id)


@router.post(
    "/chat/{chat_id}",
    response_model=ChatRoom,
)
async def post_message(
    chat_id: UUID,
    payload: ChatMessage,
    token=Depends(validate_token),
):
    return chat_manager.insert_chat(str(chat_id), payload)
