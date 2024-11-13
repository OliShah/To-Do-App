import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_task(client):
    new_task = {
        'name':'Test Task',
        'description': 'This is a test task'
    }

    response = client.post('/tasks', json=new_task)

    assert response.status_code == 201

    data = response.get_json()
    assert 'id' in data
    assert data['name'] == new_task['name']
    assert data['description'] == new_task['description']
    assert data['status'] == new_task['status']

def test_add_task_empty_data(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 400