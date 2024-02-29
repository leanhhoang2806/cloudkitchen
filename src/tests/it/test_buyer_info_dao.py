# flake8: noqa
import pytest
from src.daos.Buyer_DAO import BuyerInfoDAO


def test_get_by_email(buyer_dao):

    # Create a buyer
    email = "test@example.com"
    buyer_dao.create_with_email_only(email)

    # Retrieve the buyer by email
    retrieved_buyer = buyer_dao.get_by_email(email)

    # Assert that the retrieved buyer's email matches the expected email
    assert retrieved_buyer.email == email


def test_create_with_email_only(buyer_dao):

    # Create a buyer with email
    email = "test@example.com"
    buyer = buyer_dao.create_with_email_only(email)

    # Assert that the buyer is created with the correct email
    assert buyer.email == email
