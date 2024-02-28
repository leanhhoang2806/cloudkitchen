from uuid import UUID
from src.models.postgres_model import OrdersDish, Dish, SellerInfo
from typing import List
from src.daos.database_session import session


class OrdersDishDAO:
    def get_order_for_seller(seller_id: UUID) -> List[Dish]:
        try:
            return (
                # use this query if needed multiple data from different tables
                # session.query(OrdersDish, SellerInfo, Dish)
                #     .join(OrdersDish, Dish.id == OrdersDish.order_id)
                #     .join(SellerInfo, SellerInfo.id == Dish.seller_id)
                #     .filter(Dish.seller_id == seller_id)
                #     .all()
                # Use this query to return a specific data
                session.query(Dish)
                .join(OrdersDish, OrdersDish.dish_id == Dish.id)
                .join(SellerInfo, SellerInfo.id == Dish.seller_id)
                .filter(SellerInfo.id == str(seller_id))
                .all()
            )
        finally:
            session.close()
