import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.data_model import DishCreate, SellerInfoCreate
from src.models.postgres_model import Dish, SellerInfo
from uuid import UUID
from faker import Faker
from typing import Generator
import requests

BASE_URL = "http://localhost:8000/api/v1"
FIXED_ZIPCODE = "75025"
fake = Faker()


def _convert_uuids_to_strings(data_dict: dict) -> dict:
    converted_data = {}
    for key, value in data_dict.items():
        if isinstance(value, UUID):
            converted_data[key] = str(value)
        else:
            converted_data[key] = value
    return converted_data


@pytest.fixture(scope="session")
def session() -> Generator[Session, None, None]:
    # Define the connection string
    connection_string = "postgresql://your_user:your_password@localhost:5432/popo_24"

    # Create the SQLAlchemy engine
    engine = create_engine(connection_string)

    # Create a sessionmaker bound to the engine
    Session = sessionmaker(bind=engine)

    # Create a session
    session = Session()

    # Yield the session to the test function
    yield session

    # Close the session after the test function finishes
    session.close()


def generate_random_dish(seller_id: UUID) -> DishCreate:
    return DishCreate(
        name=fake.word(),
        description=(
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        price=fake.random_number(digits=1),
        seller_id=seller_id,
        s3_path=fake.uri_path(),
    )


@pytest.fixture(scope="session")
def generate_random_seller_info() -> SellerInfoCreate:
    return SellerInfoCreate(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number() if fake.boolean(chance_of_getting_true=50) else None,
        address=fake.address() if fake.boolean(chance_of_getting_true=50) else None,
        zipcode=FIXED_ZIPCODE,
    )


@pytest.fixture(scope="session")
def seller(session: Session, generate_random_seller_info) -> SellerInfo:
    seller_info: SellerInfo = generate_random_seller_info

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    return seller


# @pytest.fixture(scope="session")
# def buyer(session: Session, generate_random_buyer_info) -> BuyerInfo:
#     buyer_info = generate_random_buyer_info
#     buyer = BuyerInfo(**_convert_uuids_to_strings(buyer_info.dict()))
#     session.add(buyer)
#     session.commit()
#     return buyer


def test_search_should_only_return_active_dish(
    session: Generator[Session, None, None], seller: SellerInfo
) -> None:
    url = f"{BASE_URL}/search"
    dish_create = generate_random_dish(seller.id)
    dish_instance = Dish(**_convert_uuids_to_strings(dish_create.dict()))
    session.add(dish_instance)
    session.commit()
    session.close()

    params = {"zip_code": FIXED_ZIPCODE, "seller_name": ""}
    response = requests.get(url, params=params)
    json_response = response.json()
    for item in json_response:
        assert item["status"] == "ACTIVE"

    # Remove the dish with delete
    dish_instance.status = "SOFT_DELETE"
    session.commit()
