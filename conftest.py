import pytest
from methods.auth_methods import login
from data import VALID_EMAIL, VALID_PASSWORD


@pytest.fixture
def auth_token():
    response = login(VALID_EMAIL, VALID_PASSWORD)
    assert response.status_code in [200, 201]
    response_data = response.json()
    token = response_data["token"]["access_token"]
    assert token is not None, "Token not found in login response"
    return token
