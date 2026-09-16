"""Example API contract tests using a public test endpoint."""
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_user_contract():
    response = requests.get(f"{BASE_URL}/users/1", timeout=10)
    assert response.status_code == 200
    payload = response.json()
    assert {"id", "name", "email"}.issubset(payload)
    assert payload["id"] == 1


def test_missing_resource_returns_404():
    response = requests.get(f"{BASE_URL}/users/999999", timeout=10)
    assert response.status_code == 404
