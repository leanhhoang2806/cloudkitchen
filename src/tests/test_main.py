# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session


@pytest.fixture(autouse=True)
@patch.dict(
    "os.environ",
    {
        "AUTH0_ISSUER": "mocked_AUTH0_ISSUER",
        "API_IDENTIFIER": "mocked_API_IDENTIFIER",
        "POSTGRES_DATABASE_URL": "postgresql://your_user:your_password@postgres/your_dbname",
    },
)
@patch("src.managers.configuration_manager.ConfigurationManager", autospec=True)
@patch("src.daos.database_session.Database", autospec=True)
def mock_database_manager(mocked_configuration_manager, mocked_db):
    # mocked database session
    mocked_session = MagicMock(spec=Session)
    mocked_db.get_session.return_value = mocked_session

    # mocked configuration
    mocked_configuration_manager.return_value = MagicMock()

    yield mocked_configuration_manager.return_value, mocked_session


@pytest.fixture
def test_app():
    # Use the app instance from the main module
    from src.main import app

    client = TestClient(app)
    yield client


def test_read_health(test_app):
    response = test_app.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}
