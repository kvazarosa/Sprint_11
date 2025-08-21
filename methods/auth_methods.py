import requests
from data import BASE_URL


def register(email, password):
    url = f"{BASE_URL}api/signup"
    payload = {
        "email": email,
        "password": password,
        "submitPassword": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response


def login(email, password):
    url = f"{BASE_URL}api/signin"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    return response
