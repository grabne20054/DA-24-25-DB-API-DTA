import json
from api.model import UserDB

import pytest # noqa

from crud import crud


def test_create_user(test_app, monkeypatch):
    test_request_payload = {
        "name": "MyUser",
        "password": "MyPassword",}
    test_response_payload = {
        "id": 1,
        "name": "MyUser",
        "password": "MyPassword",}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post_user", mock_post)

    response = test_app.post(
        "/users/",
        content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_user_invalid_json(test_app):
    response = test_app.post(
        "/users/",
        content=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_update_user_invalid_json(test_app):
    response = test_app.put("/users/1", content=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_delete_user(test_app, monkeypatch):
    async def mock_delete(id):
        return {"id": id}
    
    monkeypatch.setattr(crud, "delete_user", mock_delete)
    
    response = test_app.delete("/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == {'id': 1}

def test_update_user(test_app, monkeypatch):
    payload = {"name": "MyName", "password": "MyPassword"}
    async def mock_update(id, payload):
        response_object = UserDB(id=id, name=payload.name, password=payload.password)
        return response_object

    monkeypatch.setattr(crud, "update_user", mock_update)
    response = test_app.put("/users/1", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["password"] == payload["password"]


def test_read_user(test_app, monkeypatch):
    async def mock_get(id, name):
        response_object = UserDB(id=id, name="MyName", password="MyPassword")
        return response_object
    monkeypatch.setattr(crud, "get_user_by_id", mock_get)
    response = test_app.get("/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "MyName"
    assert response.json()["password"] == "MyPassword"

def test_read_all_users(test_app, monkeypatch):
    users_request_payload = [
        {"id": 1, "name": "MyName", "password": "MyPassword"},
        {"id": 2, "name": "StefanieLemesch", "password": "StefaniesPassword"},
    ]

    def mock_get_all_users():
        return users_request_payload

    monkeypatch.setattr(crud, "get_all_users", mock_get_all_users)
    response = test_app.get("/users/")

    assert response.status_code == 200
    assert response.json() == users_request_payload


def test_read_user_not_found(test_app):
    response = test_app.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user_not_found(test_app):
    payload = {"name": "UpdatedName", "password": "UpdatedPassword"}
    response = test_app.put("/users/999", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_not_found(test_app):
    response = test_app.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_create_user_wrong_datatype(test_app):
    payload = { "name": 123, "users": "MyPassword"}
    response = test_app.post("/users/", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

def test_update_user_wrong_datatype(test_app):
    payload = {"name": 123, "password": "MyPassword"}
    response = test_app.put("/users/1", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

def test_create_user_missing_name(test_app):
    payload = {"password": "MyPassword"}
    response = test_app.post("/users/", json=payload)

    assert response.status_code == 422
    assert "name" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_user_missing_name(test_app):
    payload = {"password": "MyPassword"}
    response = test_app.put("/users/1", json=payload)

    assert response.status_code == 422
    assert "name" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_user_missing_password(test_app):
    payload = {"name": "MyName"}
    response = test_app.post("/users/", json=payload)

    assert response.status_code == 422
    assert "password" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_user_missing_password(test_app):
    payload = {"name": "MyName"}
    response = test_app.put("/users/1", json=payload)

    assert response.status_code == 422
    assert "password" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_user_empty_payload(test_app):
    response = test_app.post("/users/", json={})
    assert response.status_code == 422
    assert "body" in response.json()["detail"][0]["loc"]
    assert "field required" in response.text.lower()

def test_update_user_empty_payload(test_app):
    response = test_app.put("/users/1", json={})
    assert response.status_code == 422
    assert "body" in response.json()["detail"][0]["loc"]
    assert "field required" in response.text.lower()

def test_read_user_invalid_id(test_app):
    response = test_app.get("/users/one")
    assert response.status_code == 422
    assert "Input should be a valid integer, unable to parse string as an integer" in response.json()["detail"][0]["msg"]

def test_update_user_invalid_id(test_app):
    response = test_app.put("/users/one", json={})
    assert response.status_code == 422
    assert "Input should be a valid integer, unable to parse string as an integer" in response.json()["detail"][0]["msg"]

def test_delete_user_invalid_id(test_app):
    response = test_app.delete("/users/one")
    assert response.status_code == 422
    assert "Input should be a valid integer, unable to parse string as an integer" in response.json()["detail"][0]["msg"]

def test_create_user_invalid_id(test_app):
    response = test_app.post("/users/one", json={})
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"
