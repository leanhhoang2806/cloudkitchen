from fastapi import APIRouter, Depends
from src.validations.validators import validate_token
from src.errors.handle_exceptions import handle_exceptions
from sqlalchemy.orm import Session
from src.daos.database_session import session
from src.managers.profile_manager import ProfileManager
from src.models.data_model import ProfileCreate
from src.models.postgres_model import ProfilePydantic
from uuid import UUID


class CustomAPIRouter(APIRouter):
    def add_api_route(self, path: str, endpoint, **kwargs):
        super().add_api_route(path, handle_exceptions(endpoint), **kwargs)


router = CustomAPIRouter()


def get_profile_manager(db: Session = Depends(session)) -> ProfileManager:
    return ProfileManager(db)


@router.get("/profiles/{profile_id}", response_model=ProfilePydantic)
async def get_profile(
    profile_id: UUID,
    manager: ProfileManager = Depends(get_profile_manager),
    token=Depends(validate_token),
):
    profile = manager.get_profile(profile_id)
    return ProfilePydantic.from_orm(profile)


@router.post("/profiles/", response_model=ProfilePydantic)
async def create_profile(
    profile_data: ProfileCreate,
    manager: ProfileManager = Depends(get_profile_manager),
    token=Depends(validate_token),
):
    profile = manager.create_profile(profile_data)
    return ProfilePydantic.from_orm(profile)


@router.put("/profiles/{profile_id}", response_model=ProfilePydantic)
async def update_profile(
    profile_id: UUID,
    profile_data: ProfileCreate,
    manager: ProfileManager = Depends(get_profile_manager),
    token=Depends(validate_token),
):
    profile = manager.update_profile(profile_id, profile_data)
    return ProfilePydantic.from_orm(profile)


@router.delete("/profiles/{profile_id}")
async def delete_profile(
    profile_id: UUID,
    manager: ProfileManager = Depends(get_profile_manager),
    token=Depends(validate_token),
):
    deleted_count = manager.delete_profile(profile_id)
    return {"deleted_count": deleted_count}
