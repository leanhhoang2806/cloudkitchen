# tests/test_integration.py
import requests
import pytest


@pytest.fixture
def api_url():
    return "http://localhost:8000/api/v1"  # Update with your FastAPI server URL


def test_read_root(api_url):
    response = requests.get(f"{api_url}/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}
