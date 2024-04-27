from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BuyerInfo(Base):
    __tablename__ = "Buyer_Info"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    seller_id = Column(UUID)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Permission(Base):
    __tablename__ = "Permission"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    user_email = Column(String(100), nullable=False, unique=True)
    permissions = Column(JSON)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class SellerInfo(Base):
    __tablename__ = "Seller_Info"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    address = Column(String(255))
    zipcode = Column(String(15), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class ChatInfo(Base):
    __tablename__ = "Chat_Info"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    seller_id = Column(ForeignKey("Seller_Info.id"), nullable=False)
    buyer_id = Column(ForeignKey("Buyer_Info.id"), nullable=False)
    conversation_id = Column(String(24), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship("BuyerInfo")
    seller = relationship("SellerInfo")


class Dish(Base):
    __tablename__ = "Dish"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    s3_path = Column(String(255))
    seller_id = Column(ForeignKey("Seller_Info.id"), nullable=False)
    is_featured = Column(Boolean, server_default=text("false"))
    status = Column(String(50), server_default=text("'ACTIVE'::character varying"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    seller = relationship("SellerInfo")


class Payment(Base):
    __tablename__ = "Payments"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    email = Column(String(255), nullable=False)
    picture_upload_limit = Column(Integer, nullable=False)
    dishes_to_feature_limit = Column(Integer, nullable=False)
    seller_id = Column(ForeignKey("Seller_Info.id"), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    seller = relationship("SellerInfo")


class DiscountedDish(Base):
    __tablename__ = "Discounted_Dish"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    dish_id = Column(ForeignKey("Dish.id"), nullable=False)
    discounted_percentage = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    dish = relationship("Dish")


class DishReview(Base):
    __tablename__ = "Dish_Review"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    dish_id = Column(ForeignKey("Dish.id"), nullable=False)
    buyer_id = Column(ForeignKey("Buyer_Info.id"), nullable=False)
    content = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    s3_path = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship("BuyerInfo")
    dish = relationship("Dish")


class FeaturedDish(Base):
    __tablename__ = "Featured_dish"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    dish_id = Column(ForeignKey("Dish.id"), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    dish = relationship("Dish")


class Order(Base):
    __tablename__ = "Orders"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    buyer_id = Column(ForeignKey("Buyer_Info.id"), nullable=False)
    dish_id = Column(ForeignKey("Dish.id"), nullable=False)
    seller_id = Column(UUID, nullable=False)
    status = Column(
        String(50),
        server_default=text("'WAITING_FOR_SELLER_CONFIRM'::character varying"),
    )
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship("BuyerInfo")
    dish = relationship("Dish")


class Purchase(Base):
    __tablename__ = "Purchases"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    order_id = Column(ForeignKey("Orders.id"), nullable=False)
    dish_id = Column(ForeignKey("Dish.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    dish = relationship("Dish")
    order = relationship("Order")


SellerInfoPydantic = sqlalchemy_to_pydantic(SellerInfo)
DishPydantic = sqlalchemy_to_pydantic(Dish)
BuyerPydantic = sqlalchemy_to_pydantic(BuyerInfo)
OrderPydantic = sqlalchemy_to_pydantic(Order)
FeatureDishPydantic = sqlalchemy_to_pydantic(FeaturedDish)
PaymentPydantic = sqlalchemy_to_pydantic(Payment)
DiscountedDishPydantic = sqlalchemy_to_pydantic(DiscountedDish)
ChatInfoPydantic = sqlalchemy_to_pydantic(ChatInfo)
DishReviewPydantic = sqlalchemy_to_pydantic(DishReview)
PermissionPydantic = sqlalchemy_to_pydantic(Permission)
