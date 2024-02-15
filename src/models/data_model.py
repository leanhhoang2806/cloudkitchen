from pydantic import BaseModel


class ProfileCreate(BaseModel):
    name: str
    address: str
    email: str
    contact: str
    profile_picture_s3_path: str
