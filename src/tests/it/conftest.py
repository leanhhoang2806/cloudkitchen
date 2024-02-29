import pytest
from src.daos.Dish_DAO import DishDAO
from src.daos.Buyer_DAO import BuyerInfoDAO
from src.daos.Seller_DAO import SellerInfoDAO


@pytest.fixture(scope="module")
def dish_dao():
    return DishDAO()


@pytest.fixture(scope="module")
def buyer_dao():
    return BuyerInfoDAO()


@pytest.fixture(scope="module")
def seller_dao():
    return SellerInfoDAO()
