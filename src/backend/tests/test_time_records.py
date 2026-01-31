from http.client import HTTPException
import json
from api.model import TimeRecordDB
from datetime import datetime, timedelta

import pytest # noqa

from crud import crud


def test_create_time_record(test_app, monkeypatch):
    date = datetime.now().isoformat()
    test_request_payload = {
        "startDateTime": date,
        "endDateTime": date,
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"    }
    test_response_payload = {
        "id": 1,
        "startDateTime": date,
        "endDateTime": date,
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post_time_record", mock_post)

    response = test_app.post(
        "/timerecords/",
        content=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_time_record_invalid_json(test_app):
    response = test_app.post(
        "/timerecords/",
        content=json.dumps({"comment": "something"}))
    assert response.status_code == 422

def test_update_time_record_invalid_json(test_app):
    response = test_app.put("/timerecords/1", content=json.dumps({"comment": "something"}))
    assert response.status_code == 422

def test_delete_time_record(test_app, monkeypatch):
    async def mock_delete(id):
        return {"id": id}
    
    monkeypatch.setattr(crud, "delete_time_record", mock_delete)
    
    response = test_app.delete("/timerecords/1")

    assert response.status_code == 200
    assert response.json()["id"] == {'id': 1}

def test_update_time_record(test_app, monkeypatch):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    async def mock_update(id, payload):
        response_object = TimeRecordDB(id=id, startDateTime=payload.startDateTime, endDateTime=payload.endDateTime ,user_id=payload.user_id, project_id=payload.project_id, comment=payload.comment)
        return response_object

    monkeypatch.setattr(crud, "update_time_record", mock_update)
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 200
    assert response.json()["startDateTime"] == payload["startDateTime"]
    assert response.json()["endDateTime"] == payload["endDateTime"]
    assert response.json()["user_id"] == payload["user_id"]
    assert response.json()["project_id"] == payload["project_id"]
    assert response.json()["comment"] == payload["comment"]


def test_read_time_record(test_app, monkeypatch):
    async def mock_get(id, user_id, project_id):
        response_object = TimeRecordDB(id=id, startDateTime=datetime.now().isoformat(), endDateTime=datetime.now().isoformat() ,user_id=1, project_id=1, comment="A Comment")
        return response_object
    monkeypatch.setattr(crud, "get_time_record_by_id", mock_get)
    response = test_app.get("/timerecords/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["comment"] == "A Comment"
    assert response.json()["user_id"] == 1
    assert response.json()["project_id"] == 1


def test_read_all_time_records(test_app, monkeypatch):
    time_records_request_payload = [
        {"id": 1 , "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"},
        {"id": 2, "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"},
    ]

    def mock_get_all_time_records():
        return time_records_request_payload

    monkeypatch.setattr(crud, "get_all_time_records", mock_get_all_time_records)
    response = test_app.get("/timerecords/")

    assert response.status_code == 200
    assert response.json() == time_records_request_payload


def test_read_time_record_not_found(test_app):
    response = test_app.get("/timerecords/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "TimeRecord not found"

def test_update_time_record_not_found(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/999", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "TimeRecord not found"

def test_delete_time_record_not_found(test_app):
    response = test_app.delete("/timerecords/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "TimeRecord not found"

def test_create_time_record_wrong_datatype(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : "a foreign key", 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]

def test_update_time_record_wrong_datatype(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : "a foreign key", 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]

def test_create_time_record_missing_user_id(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "user_id" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_time_record_missing_user_id(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "user_id" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_time_record_missing_project_id(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "project_id" in response.text.lower()
    assert "field required" in response.text.lower()

def test_update_time_record_missing_project_id(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "project_id" in response.text.lower()
    assert "field required" in response.text.lower()

def test_create_time_record_missing_startDateTime(test_app):
    payload = {
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "startDateTime" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_update_time_record_missing_startDateTime(test_app):
    payload = {
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "startDateTime" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_create_time_record_missing_endDateTime(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "endDateTime" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_update_time_record_missing_endDateTime(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "endDateTime" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_create_time_record_missing_comment(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "comment" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_update_time_record_missing_comment(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "comment" in response.json()['detail'][0]['loc']
    assert "Field required" in response.json()['detail'][0]['msg']

def test_create_time_record_invalid_date(test_app):
    payload = {
        "startDateTime": "not a date",
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 422
    assert "startDateTime" in response.json()['detail'][0]['loc']
    assert "Input should be a valid datetime or date, invalid character in year" in response.json()['detail'][0]['msg']

def test_update_time_record_invalid_date(test_app):
    payload = {
        "startDateTime": "not a date",
        "endDateTime": datetime.now().isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.put("/timerecords/1", json=payload)

    assert response.status_code == 422
    assert "startDateTime" in response.json()['detail'][0]['loc']
    assert "Input should be a valid datetime or date, invalid character in year" in response.json()['detail'][0]['msg']

def test_create_time_record_end_before_start(test_app):
    payload = {
        "startDateTime": datetime.now().isoformat(),
        "endDateTime": (datetime.now() - timedelta(days=1)).isoformat(),
        "user_id": 1, 
        "project_id" : 1, 
        "comment": "A Comment"}
    response = test_app.post("/timerecords/", json=payload)

    assert response.status_code == 404
    assert "endDateTime is before startDateTime" in response.json()['detail']
