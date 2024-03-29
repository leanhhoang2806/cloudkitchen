from src.daos.Seller_DAO import SellerInfoDAO
from src.managers.generic_manager import GenericManager
from typing import Optional
from src.models.postgres_model import SellerInfo
from src.models.data_model import SellerInfoCreate
from src.managers.payment_manager import PaymentManager
from src.models.data_model import PaymentCreate
from uuid import UUID


class SellerInfoManager(GenericManager):
    def __init__(self):
        super().__init__(SellerInfoDAO())
        self.payment_manager = PaymentManager()

    def get_by_email(self, seller_email: str) -> Optional[SellerInfo]:
        return self.dao.get_by_email(seller_email)

    def create_with_payment_limit(
        self, seller_info_data: SellerInfoCreate
    ) -> SellerInfo:
        seller = self.create(seller_info_data)
        paymentCreate = PaymentCreate(
            email=seller_info_data.email,
            picture_upload_limit=1,
            dishes_to_feature_limit=1,
            seller_id=seller.id,
        )
        self.payment_manager.create(paymentCreate)
        return seller

    def get_seller_name_by_dish_id(self, dish_id: UUID) -> Optional[SellerInfo]:
        return self.dao.get_seller_name_by_dish_id(dish_id)
