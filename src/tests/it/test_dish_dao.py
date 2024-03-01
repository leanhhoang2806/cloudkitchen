# flake8: noqa
import pytest
from src.models.data_model import SellerInfoCreate
from src.models.data_model import DishCreate
from uuid import uuid4


def test_get_by_seller_id(seller_dao, dish_dao):
    sellerInfoCreate = SellerInfoCreate(name="test", email="test@gmail.com")
    seller = seller_dao.create(sellerInfoCreate)

    # Create some dummy dishes
    dummy_dishes = [
        DishCreate(
            name="Dish1",
            description="Description1",
            price=10.0,
            seller_id=seller.id,
            s3_path="test",
        ),
        DishCreate(
            name="Dish2",
            description="Description2",
            price=15.0,
            seller_id=seller.id,
            s3_path="test",
        ),
    ]
    for dish_create in dummy_dishes:
        dish_dao.create(dish_create)

    # Retrieve dishes by seller_id
    dishes = dish_dao.get_by_seller_id(seller.id)

    # Assert that the correct number of dishes is returned
    assert len(dishes) == 2


def test_get_dishes_paginated(seller_dao, dish_dao):
    sellerInfoCreate = SellerInfoCreate(name="test", email="test1@gmail.com")
    seller = seller_dao.create(sellerInfoCreate)

    # Create some dummy dishes
    dummy_dishes = [
        DishCreate(
            name=f"Dish{i}",
            description=f"Description{i}",
            price=10.0,
            seller_id=seller.id,
            s3_path="test",
        )
        for i in range(1, 11)
    ]
    for dish_create in dummy_dishes:
        dish_dao.create(dish_create)

    # Retrieve paginated dishes
    paginated_dishes = dish_dao.get_dishes_paginated(skip=0, limit=5)

    # Assert that the correct number of paginated dishes is returned
    assert len(paginated_dishes) == 5


# def test_update_when_feature():
#     # Instantiate the DishDAO
#     dish_dao = DishDAO()

#     # Create a dummy dish
#     dummy_dish = DishCreate(
#         name="Dummy Dish",
#         description="Dummy Description",
#         price=20.0,
#         seller_id=uuid4(),
#     )
#     created_dish = dish_dao.create(dummy_dish)

#     # Update dish to be featured
#     updated_dish = dish_dao.update_when_feature(created_dish.id)

#     # Assert that the dish is updated with the is_featured flag set to True
#     assert updated_dish.is_featured == True
