import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models.data_model import DishCreate, SellerInfoCreate, BuyerInfoCreate
from src.models.postgres_model import Dish, SellerInfo, BuyerInfo, SellerApplication
from uuid import UUID
from faker import Faker
from typing import Generator
import requests
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

BASE_URL = "http://localhost:8000/api/v1"
FIXED_ZIPCODE = "75025"
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjE2TDJHLTkyWmFJN3pzbjFGTlZhWCJ9.eyJodHRwczovL215YXBwLmV4YW1wbGUuY29tL2VtYWlsIjoiaG9hbmd0ZWNoYWNvdW50QGdtYWlsLmNvbSIsImh0dHBzOi8vbXlhcHAuZXhhbXBsZS5jb20vbmFtZSI6IkhvYW5nIExlIiwiaXNzIjoiaHR0cHM6Ly9kZXYtMXdlY3ZqeW56cXl3NzhnMC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkyNDkxNzY5MDc4NjYxNDExODkiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtMXdlY3ZqeW56cXl3NzhnMC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZGV2LTF3ZWN2anluenF5dzc4ZzAudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcxNTEwNTA5NCwiZXhwIjoxNzE1MTkxNDk0LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoiUE0zRzlZQXZxWXZNRUtHT1A1aHRDcFpkNWlHOFZJeHoifQ.S2lvpk6T7zINjfCPiTl_Rgcqcm4sFWRFoVQimdgaw09_zGIsUV7EFKorSnHK8xcaLD6rm78IqPkhXEFfNMvIXy9k9pVWEjGmhYKQ07O0AWXCOzzrxObCm2EXT5tuTE1Tr_e1p1f8ecrlradfeDR4Mg4JYoUFkoI10XTR1gHFLNrIOoQTDuPF2-cI2WjPM2SUbUf5au7VDvj2bgnO3vlPsg-DWNIyV5LadiDoPjILGoPJtNrcuv9tQqDTuDeW4uYmk4NCYylCt5jQlXOVjKagUSEli-cUbXwKo9O9CopwkL20-Yyqz8IqL8RylkZ5DxEtQPQ4wWJUAHDMq-9iXYaQKA"
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
        address=(
            fake.address()[:10] if fake.boolean(chance_of_getting_true=50) else None
        ),
        zipcode=FIXED_ZIPCODE,
    )


def generate_random_buyer_info() -> BuyerInfoCreate:
    return BuyerInfoCreate(
        name=fake.name(),
        email=fake.email(),
        phone=(
            fake.phone_number()[:5] if fake.boolean(chance_of_getting_true=50) else None
        ),
        address=fake.address()[:10],
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
        "quantities": fake.random_number(digits=1) + 1,
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

    get_response = requests.get(f"{order_url}/{order_response[0]['id']}")
    get_json_response = get_response.json()
    assert "seller_id" not in get_json_response
    assert "buyer_id" not in get_json_response


def test_seller_application_endpoint(session: Session):
    # create payload
    url = f"{BASE_URL}/seller-application"
    email = fake.email()
    payload = {
        "email": email,
        "address": fake.address() if fake.boolean(chance_of_getting_true=50) else None,
        "s3_path": "test",
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200

    get_response = requests.get(f"{url}/seller/{email}", headers=headers)
    get_response_json = get_response.json()

    assert get_response_json["email"] == email


def test_create_seller_only_application_approved(session: Session):
    seller_url = f"{BASE_URL}/seller_info"
    email = "hoangtechacount@gmail.com"
    seller_payload = {
        "name": fake.name(),
        "email": email,
        "phone": fake.phone_number(),
        "address": fake.address()[:5],
        "zipcode": FIXED_ZIPCODE,
    }

    seller_response = requests.post(seller_url, json=seller_payload, headers=headers)
    assert seller_response.status_code == 400

    # create an application
    application_url = f"{BASE_URL}/seller-application"
    application_payload = {
        "email": email,
        "address": (
            fake.address()[:5] if fake.boolean(chance_of_getting_true=50) else None
        ),
        "s3_path": "test",
    }

    requests.post(application_url, json=application_payload, headers=headers)
    assert (
        session.query(SellerApplication)
        .filter(SellerApplication.email == email)
        .count()
        == 1
    )

    # Update email manually, do the same in prod
    session.query(SellerApplication).filter(SellerApplication.email == email).update(
        {"status": "approved"}
    )
    session.commit()

    # post the request againt
    seller_response = requests.post(seller_url, json=seller_payload, headers=headers)
    assert seller_response.status_code == 200


def test_ops_router(session: Session):
    ops_applications = f"{BASE_URL}/ops/seller-application/all"
    ops_token = "SPECIAL_OPS_KEY"

    request = requests.get(
        ops_applications, headers={"Authorization": f"Bearer {ops_token}"}
    )

    assert request.status_code == 200

    first_application = request.json()[0]

    put_application_url = f"{BASE_URL}/ops/seller-application"
    update_request = requests.put(
        put_application_url,
        json={"application_id": first_application["id"], "status": "denied"},
        headers={"Authorization": f"Bearer {ops_token}"},
    )

    update_request_json = update_request.json()

    application: SellerApplication = (
        session.query(SellerApplication)
        .filter(SellerApplication.id == str(update_request_json["id"]))
        .first()
    )

    assert application.status == "denied"
