import json
from api.model import ProjectDB
from datetime import datetime

import pytest # noqa

from crud import crud


def test_create_project(test_app, monkeypatch):
    date = datetime.now().isoformat()
    test_request_payload = {
        "name": "MyProject",
        "isfinished": False,
        "dueDate": date }
    test_response_payload = {
        "id": 1,
        "name": "MyProject",
        "isfinished": False,
        "dueDate": date}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post_project", mock_post)

    response = test_app.post(
        "/projects/",
        content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_project_invalid_json(test_app):
    response = test_app.post(
        "/projects/",
        content=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_update_project_invalid_json(test_app):
    response = test_app.put("/projects/1", content=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_delete_project(test_app, monkeypatch):
    async def mock_delete(id):
        return {"id": id}
    
    monkeypatch.setattr(crud, "delete_project", mock_delete)
    
    response = test_app.delete("/projects/1")

    assert response.status_code == 200
    assert response.json()["id"] == {'id': 1}

def test_update_project(test_app, monkeypatch):
    payload = {
        "name": "MyProject",
        "isfinished": False,
        "dueDate": datetime.now().isoformat()}
    async def mock_update(id, payload):
        response_object = ProjectDB(id=id, name=payload.name, isfinished=payload.isfinished, dueDate=payload.dueDate)
        return response_object

    monkeypatch.setattr(crud, "update_project", mock_update)
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["isfinished"] == payload["isfinished"]
    assert response.json()["dueDate"] == payload["dueDate"]


def test_read_project(test_app, monkeypatch):
    async def mock_get(id):
        response_object = ProjectDB(id=id, name="MyName", isfinished=False, dueDate=datetime.now().isoformat())
        return response_object
    monkeypatch.setattr(crud, "get_project_by_id", mock_get)
    response = test_app.get("/projects/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "MyName"
    assert response.json()["isfinished"] == False

def test_read_all_projects(test_app, monkeypatch):
    projects_request_payload = [
        {"id": 1, "name": "MyProject", "isfinished": False, "dueDate": datetime.now().isoformat()},
        {"id": 2, "name": "HerProject","isfinished": False, "dueDate": datetime.now().isoformat()},
    ]

    def mock_get_all_projects(isfinished):
        return projects_request_payload

    monkeypatch.setattr(crud, "get_all_projects", mock_get_all_projects)
    response = test_app.get("/projects/")

    assert response.status_code == 200
    assert response.json() == projects_request_payload


def test_read_project_not_found(test_app):
    response = test_app.get("/projects/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_update_project_not_found(test_app):
    payload = {"name": "UpdatedName","isfinished": False, "dueDate": datetime.now().isoformat()}
    response = test_app.put("/projects/999", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_delete_project_not_found(test_app):
    response = test_app.delete("/projects/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"

def test_create_project_wrong_datatype(test_app):
    payload = { "name": 123, "isfinished": False, "dueDate": datetime.now().isoformat()}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

def test_update_project_wrong_datatype(test_app):
    payload = {"name": 123, "isfinished": False, "dueDate": datetime.now().isoformat()}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid string" in response.json()["detail"][0]["msg"]

def test_create_project_missing_name(test_app):
    payload = {"isfinished": False, "dueDate": datetime.now().isoformat()}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "name" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_project_missing_name(test_app):
    payload = {"isfinished": False, "dueDate": datetime.now().isoformat()}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "name" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_project_missing_dueDate(test_app):
    payload = {"name": "MyProject", "isfinished": False}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "duedate" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_project_missing_dueDate(test_app):
    payload = {"name": "MyProject", "isfinished": False}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "duedate" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_project_missing_isfinished(test_app):
    payload = {"name": "MyProject", "dueDate": datetime.now().isoformat()}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "isfinished" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_project_missing_isfinished(test_app):
    payload = {"name": "MyProject", "dueDate": datetime.now().isoformat()}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "isfinished" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_project_invalid_date(test_app):
    payload = {"name": "MyProject", "isfinished": False, "dueDate": "invalid_date"}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid datetime or date, invalid character in year" in response.json()["detail"][0]["msg"]

def test_update_project_invalid_date(test_app):
    payload = {"name": "MyProject", "isfinished": False, "dueDate": "invalid_date"}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid datetime or date, invalid character in year" in response.json()["detail"][0]["msg"]

def test_create_project_invalid_isfinished(test_app):
    payload = {"name": "MyProject", "isfinished": "invalid", "dueDate": datetime.now().isoformat()}
    response = test_app.post("/projects/", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid boolean, unable to interpret input" in response.json()["detail"][0]["msg"]

def test_update_project_invalid_isfinished(test_app):
    payload = {"name": "MyProject", "isfinished": "invalid", "dueDate": datetime.now().isoformat()}
    response = test_app.put("/projects/1", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid boolean, unable to interpret input" in response.json()["detail"][0]["msg"]
