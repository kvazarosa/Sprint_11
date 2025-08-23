from methods.auth_methods import register, login
from helpers import generate_random_email
from data import VALID_EMAIL, VALID_PASSWORD


class TestAuth:
    def test_successful_registration(self):
        email = generate_random_email()
        password = "1234567890poiuyt"
        response = register(email, password)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data is not None
        assert "user" in response_data or "access_token" in response_data

    def test_registration_with_existing_email(self):
        response = register(VALID_EMAIL, VALID_PASSWORD)
        response_data = response.json()
        assert response_data["statusCode"] == 400
        assert response_data["message"] == "Почта уже используется"

    def test_successful_login(self):
        response = login(VALID_EMAIL, VALID_PASSWORD)

        assert response.status_code == 201
        response_data = response.json()
        user_data = response_data["user"]
        assert user_data["email"] == VALID_EMAIL
        assert "id" in user_data
        assert "name" in user_data
        access_token = response_data["token"]["access_token"]
        assert len(access_token) > 0, "Access token should not be empty"
