from pydantic import BaseModel, PositiveInt
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class BuyerInfoCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    request_email: str


class BuyerInfoUpdate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]


class SellerInfoCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    zipcode: str


class SellerInfoUpdate(BaseModel):
    name: str
    phone: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]


class DishCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    seller_id: UUID
    s3_path: str


class DishUpdate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    seller_id: UUID


class OrderCreate(BaseModel):
    buyer_id: UUID
    dish_id: List[UUID]


class SingleOrderCreate(BaseModel):
    buyer_id: UUID
    dish_id: UUID
    seller_id: UUID


class OrderCreateWithBuyerId(BaseModel):
    buyer_id: UUID


class OrderUpdate(BaseModel):
    buyer_id: UUID
    total_amount: float


class OrderStatusUpdate(BaseModel):
    status: str
    buyer_id: UUID


class PurchaseCreate(BaseModel):
    order_id: UUID
    dish_id: UUID
    quantity: int


class PurchaseUpdate(BaseModel):
    order_id: UUID
    dish_id: UUID
    quantity: int


class PaymentsCreate(BaseModel):
    email: str
    picture_upload_limit: int
    dishes_to_feature_limit: int


class PaymentsUpdate(BaseModel):
    picture_upload_limit: Optional[int]
    dishes_to_feature_limit: Optional[int]


class Payments(BaseModel):
    id: UUID
    email: str
    picture_upload_limit: int
    dishes_to_feature_limit: int


class FeaturedDishCreate(BaseModel):
    dish_id: UUID


class PaymentCreate(BaseModel):
    email: str
    picture_upload_limit: int
    dishes_to_feature_limit: int
    seller_id: UUID


class PaymentUpdate(BaseModel):
    email: Optional[str]
    picture_upload_limit: Optional[int]
    dishes_to_feature_limit: Optional[int]


class StripeClientSecret(BaseModel):
    client_secret: str


class StripePaymentInfo(BaseModel):
    dish_ids: List[UUID]


class StripeSubscriptionStatus(BaseModel):
    active_status: bool


class DiscountedDishCreate(BaseModel):
    dish_id: UUID
    discounted_percentage: int


class DiscountedDishUpdate(BaseModel):
    id: UUID
    discounted_percentage: int


class EmailOnlyPayload(BaseModel):
    email: str


class ChatMessage(BaseModel):
    sender: str
    receiver: str
    content: str
    created_at: datetime = datetime.now()


class ChatRoomCreate(BaseModel):
    seller_id: UUID
    buyer_id: UUID
    messages: List[ChatMessage] = []


class ChatRoom(ChatRoomCreate):
    mongo_chat_room_id: str


class ChatInfoCreate(BaseModel):
    seller_id: UUID
    buyer_id: UUID
    conversation_id: str


class GenericResponsePayload(StripeSubscriptionStatus):
    # combined order classes if needed

    pass


class DishReviewCreate(BaseModel):
    dish_id: UUID
    buyer_id: UUID
    content: str
    rating: PositiveInt
