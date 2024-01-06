import pytest
import json
import blocklist
from .client import client
from flask_jwt_extended import get_jwt


def test_create(client):
    response = client.post("/store", json={"name": "basic"})

    data_store = json.loads(response.data.decode())

    assert data_store["name"] == "basic"
    assert response.status_code == 201
    assert data_store["items"] == []
    assert data_store["tags"] == []


def test_store_already_exists(client):
    response = client.post("/store", json={"name": "basic"})
    response_1 = client.post("/store", json={"name": "basic"})
    assert response_1.status_code == 400


def test_get_stores(client):
    response_1 = client.post("/store", json={"name": "basic_1"})
    response = client.get("/store")

    data_stores = json.loads(response.data.decode())

    assert data_stores[0]["name"] == "basic"
    assert data_stores[1]["name"] == "basic_1"


def test_get_store(client):
    response = client.get("/store/1")

    data_store = json.loads(response.data.decode())

    assert data_store["name"] == "basic"
    assert response.status_code == 200


def test_store_not_found(client):
    response = client.get("/store/3")

    assert response.status_code == 404


def test_delete_store(client):
    response = client.delete("/store/1")

    data_delete = json.loads(response.data.decode())

    assert data_delete["message"] == "store is deleted"
