from src.models.postgres_model import SellerApplication
from src.daos.database_session import provide_session
from sqlalchemy.orm import Session
from uuid import UUID


class OpsDAO:

    @provide_session
    def get_all_seller_application(self, session: Session):
        return (
            session.query(SellerApplication)
            .order_by(SellerApplication.updated_at.desc())
            .all()
        )

    @provide_session
    def update_seller_application(
        self, application_id: UUID, status: str, session: Session
    ) -> SellerApplication:
        session.query(SellerApplication).filter(
            SellerApplication.id == str(application_id)
        ).update({"status": status})

        session.commit()

        return (
            session.query(SellerApplication)
            .filter(SellerApplication.id == str(application_id))
            .first()
        )
