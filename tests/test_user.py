import pytest
import json
import blocklist
from .client import client
from flask_jwt_extended import get_jwt


def test_create_user(client):
    response = client.post("/register", json={"username": "boris", "password": "123"})
    response_1 = json.loads(response.data.decode())
    assert response.status_code == 201
    assert response_1["message"] == "User created successfully"


def test_user_already_exists(client):
    response = client.post("/register", json={"username": "boris", "password": "123"})
    data = json.loads(response.data.decode())
    assert response.status_code == 409
    assert data["message"] == "A user with that username already exists!"


def test_get_user_by_id(client):
    response_get_user = client.get(f"/user/1")
    user_data = json.loads(response_get_user.data.decode())
    assert "username" in user_data
    assert user_data["username"] == "boris"


def test_user_not_found(client):
    response_user_not_found = client.get(f"user/2")
    assert response_user_not_found.status_code == 404


def test_login(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())

    assert response_login.status_code == 200
    assert "access_token" in data_login


def test_logout(client):
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

    response_logout = client.post(
        "/logout", headers={"Authorization": f"Bearer {access_token}"}
    )
    data_logout = json.loads(response_logout.data.decode())
    jti = get_jwt()["jti"]
    assert data_logout["message"] == "Successfully logged out!"
    assert jti in blocklist.BLOCKLIST


def test_delete_user_by_id(client):
    response_delete_user = client.delete(f"/user/1")
    delete_data = json.loads(response_delete_user.data.decode())
    assert delete_data["message"] == "User deleted!"
    assert response_delete_user.status_code == 200
