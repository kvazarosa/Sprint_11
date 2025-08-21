import requests
from data import BASE_URL


def create_ad(token, title, description):
    """Метод для создания объявления."""
    url = f"{BASE_URL}api/create-listing"

    # Используем разные значения как в успешном запросе
    data = {
        'name': title,  # Основное название
        'category': 'Хобби',  # Категория (работает)
        'condition': 'Б/У',  # Состояние (работает)
        'city': 'Екатеринбург',  # Город (работает)
        'description': description,
        'price': 2000  # Цена как число (работает)
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, data=data, headers=headers, verify=False)
    return response


def get_ad(token, ad_id):
    """Метод для получения информации об объявлении."""
    url = f"{BASE_URL}api/offers/{ad_id}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers, verify=False)
    return response


def update_ad(token, ad_id, title, description=None):
    """Метод для обновления объявления."""
    url = f"{BASE_URL}api/update-offer/{ad_id}"

    data = {'title': title}
    if description:
        data['description'] = description

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.patch(url, data=data, headers=headers, verify=False)
    return response


def delete_ad(token, ad_id):
    """Метод для удаления объявления."""
    url = f"{BASE_URL}api/listings/{ad_id}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(url, headers=headers, verify=False)
    return response