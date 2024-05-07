from fastapi import HTTPException, status
from src.daos.Seller_DAO import SellerInfoDAO
from src.managers.permission_manager import PermissionManager
from src.managers.generic_manager import GenericManager
from src.managers.seller_application_manager import SellerApplicationManager
from typing import Optional
from src.models.postgres_model import SellerInfo
from src.models.data_model import SellerInfoCreate
from src.managers.payment_manager import PaymentManager
from src.models.data_model import PaymentCreate
from src.errors.custom_exceptions import SellerApplicationHasNotApproved
from uuid import UUID


permission_manager = PermissionManager()
seller_application_manager = SellerApplicationManager()


class SellerInfoManager(GenericManager):
    def __init__(self):
        super().__init__(SellerInfoDAO())
        self.payment_manager = PaymentManager()

    def get_with_permission(
        self, token_email: str, seller_id: UUID
    ) -> Optional[SellerInfo]:
        if not permission_manager.is_authorized_to_access(token_email, seller_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )
        return self.dao.get(seller_id)

    def get_by_email(self, seller_email: str) -> Optional[SellerInfo]:
        return self.dao.get_by_email(seller_email)

    def create_with_payment_limit(
        self, seller_info_data: SellerInfoCreate
    ) -> SellerInfo:
        if not self.does_seller_application_approved(seller_info_data.email):
            raise SellerApplicationHasNotApproved

        seller = self.create(seller_info_data)
        paymentCreate = PaymentCreate(
            email=seller_info_data.email,
            picture_upload_limit=1,
            dishes_to_feature_limit=1,
            seller_id=seller.id,
        )
        self.payment_manager.create(paymentCreate)
        permission_manager.add_permission(seller_info_data.email, seller.id)
        return seller

    def get_seller_name_by_dish_id(self, dish_id: UUID) -> Optional[SellerInfo]:
        return self.dao.get_seller_name_by_dish_id(dish_id)

    def does_seller_application_approved(self, email: str) -> bool:
        application = seller_application_manager.get_by_email(email)
        return application.status == "approved" if application else False
