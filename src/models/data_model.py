from pydantic import BaseModel, PositiveInt, Field
from typing import Optional, List, Dict
from uuid import UUID
import uuid
from datetime import datetime
from decimal import Decimal


class BuyerInfoCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]


class BuyerInfoUpdate(BaseModel):
    name: str
    phone: Optional[str]
    address: Optional[str]


class SellerInfoCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str]
    price: float
    seller_id: UUID
    s3_path: str
    quantities: PositiveInt


class DishUpdate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    seller_id: UUID


class OrderCreate(BaseModel):
    buyer_id: UUID
    dish_id: List[UUID]
    quantities: List[PositiveInt]


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    order_id: UUID
    dish_id: UUID
    quantity: int


class PurchaseUpdate(BaseModel):
    order_id: UUID
    dish_id: UUID
    quantity: int


class PaymentsCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    buyer_id: UUID
    dish_ids: List[UUID]


class StripeSubscriptionStatus(BaseModel):
    active_status: bool


class DiscountedDishCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    seller_id: UUID
    buyer_id: UUID
    messages: List[ChatMessage] = []


class ChatRoom(ChatRoomCreate):
    mongo_chat_room_id: str


class ChatInfoCreate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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
    image_data: str


class DishReviewCreateWithS3(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    dish_id: UUID
    buyer_id: UUID
    content: str
    rating: PositiveInt
    s3_path: str


class GenericPermission(BaseModel):
    accessible_uuids: List[UUID]


class UserPermission(BaseModel):
    user_email: str
    permissions: GenericPermission

    def dict(self, **kwargs) -> Dict[str, any]:
        data = super().dict(**kwargs)
        data["permissions"] = self.permissions.dict()
        return data


class UserPermissionUpdate(BaseModel):
    permissions: dict


class DishInformationForExternal(BaseModel):
    id: UUID
    name: str
    seller_name: Optional[str]
    description: Optional[str]
    price: Decimal
    s3_path: Optional[str]
    quantities: int
    is_featured: bool
    status: str
    created_at: datetime
    updated_at: datetime


class OrderInformationForExternal(BaseModel):
    id: UUID
    dish_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    address: Optional[str]
