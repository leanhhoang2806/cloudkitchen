from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

Base = declarative_base()
metadata = Base.metadata


class Profile(Base):
    __tablename__ = "profile"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    name = Column(String(100))
    address = Column(String(255))
    email = Column(String(100), nullable=False)
    contact = Column(String(20))
    profile_picture_s3_path = Column(String(255))


ProfilePydantic = sqlalchemy_to_pydantic(Profile)
