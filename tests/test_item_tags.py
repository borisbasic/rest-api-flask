import pytest
import json
import blocklist
from .client import client
from flask_jwt_extended import get_jwt

def test_create_tag_store(client):
    response_store = client.post('/store', json={'name': 'boris'})
    data_store = json.loads(response_store.data.decode())

    id = data_store['id']

    response_tag_store = client.post(f'/store/{id}/tag',
                                     json={
                                           'name': 'tag_1'})
    
    data_tag = json.loads(response_tag_store.data.decode())

    assert response_tag_store.status_code == 201
    assert data_tag['name'] == 'tag_1'
    assert data_tag['store']['name'] == 'boris'
    assert data_tag['items'] == {}

def test_get_tags_from_store(client):
    response_tag_store_1 = client.post(f'/store/1/tag',
                                     json={
                                           'name': 'tag_2'})
    
    response_get_tags = client.get('/store/1/tag')
    data_tag = json.loads(response_get_tags.data.decode())

    assert data_tag[0]['name'] == 'tag_1'
    assert data_tag[1]['name'] == 'tag_2'


def test_create_item_tag(client):
    response = client.post("/register", json={"username": "boris", "password": "123"})
    response_login = client.post(
        "/login", json={"username": "boris", "password": "123"}
    )

    data_login = json.loads(response_login.data.decode())
    access_token = data_login["access_token"]

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

    response_item_tag = client.post('/item/1/tag/1')
    data_item_tag = json.loads(response_item_tag.data.decode())
    assert response_item_tag.status_code == 201
    assert data_item_tag['name'] == 'tag_1'