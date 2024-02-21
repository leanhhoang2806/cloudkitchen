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
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BuyerInfo(Base):
    __tablename__ = "buyer_info"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class SellerInfo(Base):
    __tablename__ = "seller_info"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class Dish(Base):
    __tablename__ = "dish"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    seller_id = Column(ForeignKey("seller_info.id"), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    seller = relationship("SellerInfo")


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    buyer_id = Column(ForeignKey("buyer_info.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship("BuyerInfo")


class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    order_id = Column(ForeignKey("orders.id"), nullable=False)
    dish_id = Column(ForeignKey("dish.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    dish = relationship("Dish")
    order = relationship("Order")


SellerInfoPydantic = sqlalchemy_to_pydantic(SellerInfo)
DishPydantic = sqlalchemy_to_pydantic(Dish)
