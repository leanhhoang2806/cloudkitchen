from sqlalchemy.orm import Session
from src.daos.profile_DAO import ProfileDAO
from src.models.data_model import ProfileCreate
from src.models.postgres_model import Profile
from uuid import UUID


class ProfileManager:
    def __init__(self, db: Session):
        self.dao = ProfileDAO(db)

    def create_profile(self, profile_data: ProfileCreate) -> Profile:
        return self.dao.create_profile(profile_data)

    def get_profile(self, profile_id: UUID) -> Profile:
        return self.dao.get_profile(profile_id)

    def update_profile(self, profile_id: UUID, profile_data: ProfileCreate) -> Profile:
        return self.dao.update_profile(profile_id, profile_data)

    def delete_profile(self, profile_id: UUID) -> int:
        return self.dao.delete_profile(profile_id)
