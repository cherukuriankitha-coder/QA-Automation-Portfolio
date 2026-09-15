"""Simple REST API test examples for a QA automation portfolio."""

import requests

BASE_URL = "https://reqres.in/api"


def test_get_user():
    response = requests.get(f"{BASE_URL}/users/2", timeout=10)
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["id"] == 2
    assert "email" in payload["data"]


def test_create_user():
    body = {"name": "Ankitha", "job": "Data QA Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=body, timeout=10)
    assert response.status_code in (200, 201)
    payload = response.json()
    assert payload["name"] == body["name"]
    assert payload["job"] == body["job"]
    assert "id" in payload


def test_update_user():
    body = {"name": "Ankitha", "job": "QA Automation Engineer"}
    response = requests.put(f"{BASE_URL}/users/2", json=body, timeout=10)
    assert response.status_code == 200
    payload = response.json()
    assert payload["job"] == body["job"]


def test_missing_user_returns_404():
    response = requests.get(f"{BASE_URL}/users/23", timeout=10)
    assert response.status_code == 404
