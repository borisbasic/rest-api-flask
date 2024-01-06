import pytest
import json
import blocklist
from .client import client
from flask_jwt_extended import get_jwt


def test_create_item(client):
    response = client.post("/register", json={"username": "boris", "password": "123"})
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]
    response_store = client.post("/store", json={"name": "basic"})

    response_create_item = client.post(
        "/item",
        json={
            "name": "item_1",
            "price": 21.99,
            "store_id": 1,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data_item = json.loads(response_create_item.data.decode())

    assert response_create_item.status_code == 201
    assert data_item["name"] == "item_1"
    assert data_item["store"]["name"] == "basic"
    assert data_item["tags"] == {}


def test_get_items(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

    response_get_items = client.get(
        "/item", headers={"Authorization": f"Bearer {access_token}"}
    )
    data_items = json.loads(response_get_items.data.decode())
    assert response_get_items.status_code == 200
    assert data_items[0]["name"] == "item_1"


def test_get_item_by_id(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

    response_get_item = client.get(
        "/item/1", headers={"Authorization": f"Bearer {access_token}"}
    )
    data_items = json.loads(response_get_item.data.decode())
    assert response_get_item.status_code == 200
    assert data_items["name"] == "item_1"


def test_get_item_not_found(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

    response_get_item = client.get(
        "/item/2", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response_get_item.status_code == 404


def test_update_item(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

    response_update = client.put(
        "/item/3",
        json={"name": "basicbasic", "price": 19.99, "store_id": 1},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response_update_1 = client.put(
        "/item/1",
        json={
            "name": "basicbasicb",
            "price": 19.99,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    data_update = json.loads(response_update.data.decode())
    data_update_1 = json.loads(response_update_1.data.decode())
    assert data_update["name"] == "basicbasic"
    assert data_update["price"] == 19.99
    assert response_update.status_code == 200
    assert data_update_1["name"] == "basicbasicb"


def test_delete_item(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]
    response_delete = client.delete(
        "/item/1", headers={"Authorization": f"Bearer {access_token}"}
    )

    data_delete = json.loads(response_delete.data.decode())

    assert data_delete["message"] == "Item is deleted"
