from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID


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


class SellerInfoUpdate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]


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


class OrderCreateWithBuyerId(BaseModel):
    buyer_id: UUID


class OrderUpdate(BaseModel):
    buyer_id: UUID
    total_amount: float


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
