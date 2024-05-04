import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.data_model import DishCreate, SellerInfoCreate, BuyerInfoCreate
from src.models.postgres_model import Dish, SellerInfo, BuyerInfo
from uuid import UUID
from faker import Faker
from typing import Generator
import requests
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

BASE_URL = "http://localhost:8000/api/v1"
FIXED_ZIPCODE = "75025"
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjE2TDJHLTkyWmFJN3pzbjFGTlZhWCJ9.eyJodHRwczovL215YXBwLmV4YW1wbGUuY29tL2VtYWlsIjoiaG9hbmd0ZWNoYWNvdW50QGdtYWlsLmNvbSIsImh0dHBzOi8vbXlhcHAuZXhhbXBsZS5jb20vbmFtZSI6IkhvYW5nIExlIiwiaXNzIjoiaHR0cHM6Ly9kZXYtMXdlY3ZqeW56cXl3NzhnMC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkyNDkxNzY5MDc4NjYxNDExODkiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtMXdlY3ZqeW56cXl3NzhnMC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZGV2LTF3ZWN2anluenF5dzc4ZzAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcxNDY0MTYxMSwiZXhwIjoxNzE0NzI4MDExLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiUE0zRzlZQXZxWXZNRUtHT1A1aHRDcFpkNWlHOFZJeHoifQ.cmvf-fbe25hXWs1YeK-ACaD8igBxxRe_9lBaHg86r6R_xSHZZp4tVSrjfFuI36dBQh8Z5qZ_kb6UKdmWvkMMUfdDrx3yszL_aPLcBMToQbGjHrbhE3iEhwN-Ozt45XrRzLg1Hx9g62XTmohgHB3JJFuN_WhmGDGDz7YIn2ERCnw5KDyDKkF0c2A48vwnKI7Qk10qit7bsm3LXeEaBvBTuh7CHSg9jx36mpDWAEp75Retg929VelAZqmNk2vOh0T4CAj8AWY2Cz82QiNuYHFnfdZZqCcaE4-SwJjeHI4X-GOmlvMt8GWBQt5O-pHLw2_KSQIq85NPf7bdM9W_kCVCSw"
headers = {"Authorization": f"Bearer {TOKEN}"}
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

    for table in Base.metadata.tables.values():
        # Create a delete statement for the current table
        delete_stmt = table.delete()

        # Execute the delete statement using the session
        session.execute(delete_stmt)

    # Commit the transaction
    session.commit()

    # Close the session after the test function finishes
    session.close()


def generate_random_dish(seller_id: UUID) -> DishCreate:
    return DishCreate(
        name=fake.word(),
        description=(
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        price=fake.random_number(digits=1),
        seller_id=str(seller_id),
        s3_path=fake.uri_path(),
        quantities=fake.random_number(digits=1) + 1,
    )


def generate_random_seller_info() -> SellerInfoCreate:
    return SellerInfoCreate(
        name=fake.name(),
        email=fake.email(),
        phone=(
            fake.phone_number()[:5] if fake.boolean(chance_of_getting_true=50) else None
        ),
        address=fake.address() if fake.boolean(chance_of_getting_true=50) else None,
        zipcode=FIXED_ZIPCODE,
    )


def generate_random_buyer_info() -> BuyerInfoCreate:
    return BuyerInfoCreate(
        name=fake.name(),
        email=fake.email(),
        phone=(
            fake.phone_number()[:5] if fake.boolean(chance_of_getting_true=50) else None
        ),
        address=fake.address(),
    )


def test_search_should_only_return_active_dish(session: Session) -> None:
    url = f"{BASE_URL}/search"
    seller_info: SellerInfo = generate_random_seller_info()

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    session.refresh(seller)
    dish_create = generate_random_dish(seller.id)
    dish_instance = Dish(**_convert_uuids_to_strings(dish_create.dict()))
    session.add(dish_instance)
    session.commit()
    session.refresh(dish_instance)

    params = {"zip_code": FIXED_ZIPCODE, "seller_name": ""}
    response = requests.get(url, params=params)
    json_response = response.json()
    for item in json_response:
        assert item["status"] == "ACTIVE"

    # Remove the dish with delete
    session.query(Dish).filter(Dish.id == str(dish_instance.id)).update(
        {Dish.status: "SOFT_DELETE"}
    )
    session.commit()

    response = requests.get(url, params=params)
    json_response = response.json()
    for item in json_response:
        assert item["status"] == "ACTIVE"


def test_dish_create_route(session: Session):
    url = f"{BASE_URL}/dish"
    seller_info: SellerInfoCreate = generate_random_seller_info()

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    session.refresh(seller)
    payload = {
        "name": fake.word(),
        "description": (
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        "price": fake.random_number(digits=1) / 10,
        "seller_id": str(seller.id),
        "s3_path": fake.uri_path(),
        "quantities": fake.random_number(digits=1),
    }

    response = requests.post(url, json=payload, headers=headers)
    assert "quantities" in response.json()


def test_dish_quantities_should_reduce_after_ordering(session: Session):
    dish_url = f"{BASE_URL}/dish"
    order_url = f"{BASE_URL}/order"
    dish_quantities = fake.random_number(digits=1) + 1
    seller_info: SellerInfo = generate_random_seller_info()

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    session.refresh(seller)
    payload = {
        "name": fake.word(),
        "description": (
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        "price": fake.random_number(digits=1) / 10,
        "seller_id": str(seller.id),
        "s3_path": fake.uri_path(),
        "quantities": dish_quantities,
    }

    response = requests.post(dish_url, json=payload, headers=headers)
    post_dish_response = response.json()

    assert response.status_code == 200

    # create a buyer
    buyer_create = generate_random_buyer_info()
    buyer_inserted = BuyerInfo(**_convert_uuids_to_strings(buyer_create.dict()))
    session.add(buyer_inserted)
    session.commit()
    session.refresh(buyer_inserted)

    # create an order
    order_payload = {
        "buyer_id": buyer_inserted.id,
        "dish_id": [post_dish_response["id"]],
        "quantities": [1],
    }

    response = requests.post(order_url, json=order_payload, headers=headers)

    get_dish: Dish = (
        session.query(Dish).filter(Dish.id == post_dish_response["id"]).first()
    )

    assert dish_quantities - get_dish.quantities == 1


def test_make_sure_no_seller_id_return_on_GET_dish(session: Session):
    dish_url = f"{BASE_URL}/dish"
    dish_quantities = fake.random_number(digits=1) + 1
    seller_info: SellerInfo = generate_random_seller_info()

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    session.refresh(seller)
    payload = {
        "name": fake.word(),
        "description": (
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        "price": fake.random_number(digits=1) / 10,
        "seller_id": str(seller.id),
        "s3_path": fake.uri_path(),
        "quantities": dish_quantities,
    }

    response = requests.post(dish_url, json=payload, headers=headers)
    post_dish_response = response.json()

    assert "seller_id" not in post_dish_response


def test_no_seller_id_or_buyer_id_in_GET_order(session: Session):
    dish_url = f"{BASE_URL}/dish"
    order_url = f"{BASE_URL}/order"
    dish_quantities = fake.random_number(digits=1) + 1
    seller_info: SellerInfo = generate_random_seller_info()

    seller = SellerInfo(**_convert_uuids_to_strings(seller_info.dict()))
    session.add(seller)
    session.commit()
    session.refresh(seller)
    payload = {
        "name": fake.word(),
        "description": (
            fake.sentence() if fake.boolean(chance_of_getting_true=50) else None
        ),
        "price": fake.random_number(digits=1) / 10,
        "seller_id": str(seller.id),
        "s3_path": fake.uri_path(),
        "quantities": dish_quantities,
    }

    response = requests.post(dish_url, json=payload, headers=headers)
    post_dish_response = response.json()

    assert response.status_code == 200

    # create a buyer
    buyer_create = generate_random_buyer_info()
    buyer_inserted = BuyerInfo(**_convert_uuids_to_strings(buyer_create.dict()))
    session.add(buyer_inserted)
    session.commit()
    session.refresh(buyer_inserted)

    # create an order
    order_payload = {
        "buyer_id": buyer_inserted.id,
        "dish_id": [post_dish_response["id"]],
        "quantities": [1],
    }

    response = requests.post(order_url, json=order_payload, headers=headers)
    order_response = response.json()

    print(order_response)

    get_response = requests.get(f"{order_url}/{order_response[0]['id']}")
    get_json_response = get_response.json()
    assert "seller_id" not in get_json_response
    assert "buyer_id" not in get_json_response
