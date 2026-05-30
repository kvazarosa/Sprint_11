import requests
from data import BASE_URL


def create_ad(token, title, description):
    url = f"{BASE_URL}api/create-listing"

    payload = {
        "name": title,
        "category": "Авто",
        "condition": "Новый",
        "city": "Москва",
        "description": description,
        "price": "1500"
    }

    files = []
    for key, value in payload.items():
        files.append((key, (None, str(value))))

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(
        url,
        files=files,
        headers=headers,
        verify=False
    )
    return response


def get_ad(token, ad_id):
    url = f"{BASE_URL}api/offers/{ad_id}"

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        url,
        headers=headers,
        verify=False
    )
    return response


def update_ad(token, ad_id, title=None, description=None, price=None, category="Авто", condition="Новый",
              city="Москва"):
    url = f"{BASE_URL}api/update-offer/{ad_id}"

    payload = {
        "name": title if title is not None else "",  # или можно получить текущее значение
        "category": category,
        "condition": condition,
        "city": city,
        "description": description if description is not None else "",
        "price": str(price) if price is not None else "0"
    }

    files = []
    for key, value in payload.items():
        files.append((key, (None, str(value))))

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.patch(
        url,
        files=files,
        headers=headers,
        verify=False
    )
    return response


def register(email, password, name="Test User"):
    url = f"{BASE_URL}api/auth/register"

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    response = requests.post(url, json=payload, verify=False)
    return response


def delete_ad(token, ad_id):
    url = f"{BASE_URL}api/listings/{ad_id}"

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.delete(
        url,
        headers=headers,
        verify=False
    )
    return response
