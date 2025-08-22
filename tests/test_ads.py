from methods.ads_methods import create_ad, update_ad, delete_ad
from data import AD_TITLE, AD_DESCRIPTION, AD_NEW_TITLE


class TestAds:
    def test_create_ad_success(self, auth_token):
        response = create_ad(auth_token, AD_TITLE, AD_DESCRIPTION)

        assert response.status_code in [200, 201]

        response_data = response.json()
        assert "id" in response_data
        assert response_data["name"] == AD_TITLE
        assert response_data["description"] == AD_DESCRIPTION
        assert response_data["price"] == 1500

        return response_data["id"]

    def test_update_ad_success(self, auth_token):
        create_response = create_ad(auth_token, AD_TITLE, AD_DESCRIPTION)
        assert create_response.status_code in [200, 201]
        ad_id = create_response.json()["id"]

        update_response = update_ad(
            auth_token,
            ad_id,
            title=AD_NEW_TITLE,
            price=100
        )

        assert update_response.status_code == 200
        response_data = update_response.json()
        assert response_data["name"] == AD_NEW_TITLE
        assert response_data["price"] == 100

    def test_update_other_user_ad_failure(self, auth_token):
        from helpers import generate_random_email
        from methods.auth_methods import register
        second_user_email = generate_random_email()
        second_user_password = "password123"

        register_response = register(second_user_email, second_user_password)
        assert register_response.status_code in [200, 201]

        from methods.auth_methods import login
        second_user_login = login(second_user_email, second_user_password)
        assert second_user_login.status_code in [200, 201]
        second_user_token = second_user_login.json()["token"]["access_token"]

        second_user_ad_response = create_ad(second_user_token, "Чужое объявление", "Описание чужого объявления")
        assert second_user_ad_response.status_code in [200, 201]
        other_user_ad_id = second_user_ad_response.json()["id"]

        update_response = update_ad(
            auth_token,
            other_user_ad_id,
            title="Попытка изменить чужое объявление",
            description="Не должно работать",
            price=999
        )

        assert update_response.status_code in [403, 401]

    def test_delete_ad_success(self, auth_token):
        create_response = create_ad(auth_token, AD_TITLE, AD_DESCRIPTION)
        assert create_response.status_code in [200, 201]
        ad_id = create_response.json()["id"]

        delete_response = delete_ad(auth_token, ad_id)

        assert delete_response.status_code == 200

        response_data = delete_response.json()
        assert "message" in response_data, "No message in delete response"
        assert "удалено" in response_data["message"].lower() or "success" in response_data["message"].lower()
