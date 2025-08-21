# check_token.py
from methods.auth_methods import login
from data import VALID_EMAIL, VALID_PASSWORD

response = login(VALID_EMAIL, VALID_PASSWORD)
print(f"Login status: {response.status_code}")
print(f"Token: {response.json()['token']['access_token'][:50]}...")