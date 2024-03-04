from src.daos.Seller_DAO import SellerInfoDAO
from src.managers.generic_manager import GenericManager
from typing import Optional
from src.models.postgres_model import SellerInfo
from src.models.data_model import SellerInfoCreate
from src.managers.payment_manager import PaymentManager
from src.models.data_model import PaymentCreate


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
            picture_upload_limit=3,
            dishes_to_feature_limit=3,
            seller_id=seller.id,
        )
        self.payment_manager.create(paymentCreate)
        return seller
