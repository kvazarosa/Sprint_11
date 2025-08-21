import pytest
import random
from methods.ads_methods import create_ad, get_ad, update_ad, delete_ad
from data import AD_TITLE, AD_DESCRIPTION, AD_NEW_TITLE
from methods.auth_methods import register, login
from helpers import generate_random_email


class TestAds:
    """Тесты для функциональности работы с объявлениями."""

    # 1. Тест на успешное создание объявления
    def test_create_ad_success(self, auth_token):
        """Успешное создание объявления в любой категории."""
        response = create_ad(auth_token, AD_TITLE, AD_DESCRIPTION)

        assert response.status_code in [200, 201], (
            f"Ad creation failed. Status: {response.status_code}, Response: {response.text}"
        )

        response_data = response.json()
        assert "id" in response_data, "Ad ID not found in response"
        assert response_data["name"] == AD_TITLE, "Name doesn't match"
        assert response_data["description"] == AD_DESCRIPTION, "Description doesn't match"
        assert response_data["price"] == 0, "Price should be 0"  # Проверяем price

        return response_data["id"]

    # 2. Тест на успешное редактирование объявления
    def test_update_ad_success(self, auth_token):
        """Успешное редактирование любого поля объявления."""
        # Сначала создаем объявление
        ad_id = self.test_create_ad_success(auth_token)

        # Обновляем название объявления
        response = update_ad(auth_token, ad_id, AD_NEW_TITLE)

        # Проверяем успешное обновление
        assert response.status_code in [200, 204], (
            f"Update ad failed. Status: {response.status_code}, Response: {response.text}"
        )

        # Если сервер возвращает обновленные данные, проверяем их
        if response.status_code == 200:
            response_data = response.json()
            assert response_data["name"] == AD_NEW_TITLE, "Name wasn't updated"  # Проверяем поле name
            assert "updatedAt" in response_data, "Updated timestamp not found"

    # 3. Тест на попытку редактирования чужого объявления
    def test_update_foreign_ad(self, auth_token):
        """Редактирование объявления, созданного не тем пользователем."""
        # Создаем второго пользователя
        email = generate_random_email()
        password = "password123"

        # Регистрируем и логиним второго пользователя
        register_response = register(email, password)
        assert register_response.status_code in [200, 201], "Second user registration failed"

        login_response = login(email, password)
        assert login_response.status_code == 200, "Second user login failed"
        second_token = login_response.json()["token"]["access_token"]

        # Создаем объявление вторым пользователем
        create_response = create_ad(second_token, "Чужое объявление", "Описание")
        assert create_response.status_code in [200, 201], "Foreign ad creation failed"
        foreign_ad_id = create_response.json()["id"]

        # Пытаемся обновить чужое объявление
        response = update_ad(auth_token, foreign_ad_id, "Попытка изменить")

        # Должна быть ошибка доступа
        assert response.status_code in [403, 404, 401], (
            f"Expected access error, got {response.status_code}. Response: {response.text}"
        )

    # 4. Тест на успешное удаление объявления
    def test_delete_ad_success(self, auth_token):
        """Успешное удаление объявления."""
        # Сначала создаем объявление
        ad_id = self.test_create_ad_success(auth_token)

        # Удаляем объявление
        response = delete_ad(auth_token, ad_id)

        assert response.status_code in [200, 204, 202], (
            f"Delete ad failed. Status: {response.status_code}, Response: {response.text}"
        )

        # Проверяем, что объявление удалено
        get_response = get_ad(auth_token, ad_id)
        assert get_response.status_code in [404, 410], "Ad should be deleted"