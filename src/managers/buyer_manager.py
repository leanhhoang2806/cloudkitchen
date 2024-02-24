from src.daos.Buyer_DAO import BuyerInfoDAO
from src.managers.generic_manager import GenericManager


class BuyerManager(GenericManager):
    def __init__(self):
        super().__init__(BuyerInfoDAO())

    def get_by_email(self, email):
        buyer = self.dao.get_by_email(email)
        if not buyer:
            self.dao.create_with_email_only(email)
        return self.dao.get_by_email(email)
