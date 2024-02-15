from sqlalchemy.orm import Session
from src.models.postgres_model import Profile
from src.models.data_model import ProfileCreate
from uuid import UUID


class ProfileDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, profile_data: ProfileCreate) -> ProfileCreate:
        profile = Profile(**profile_data.dict())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile(self, profile_id: UUID) -> ProfileCreate:
        return self.db.query(Profile).filter(Profile.id == profile_id).first()

    def update_profile(self, profile_id: UUID, profile_data: ProfileCreate):
        profile = Profile(**profile_data.dict(), id=profile_id)
        self.db.merge(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete_profile(self, profile_id: UUID):
        deleted_count = self.db.query(Profile).filter(Profile.id == profile_id).delete()
        self.db.commit()
        return deleted_count
