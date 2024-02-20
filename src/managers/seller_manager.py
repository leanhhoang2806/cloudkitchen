from src.daos.Seller_DAO import SellerInfoDAO


class SellerInfoManager:
    def __init__(self):
        self.dao = SellerInfoDAO()

    def create_seller_info(self, data):
        return self.dao.create(data)

    def get_seller_info(self, seller_info_id):
        return self.dao.get(seller_info_id)

    def update_seller_info(self, seller_info_id, data):
        return self.dao.update(seller_info_id, data)

    def delete_seller_info(self, seller_info_id):
        return self.dao.delete(seller_info_id)
