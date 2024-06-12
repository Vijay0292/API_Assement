import pytest
from app import app, mongo

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_bisection(client):
    response = client.post('/bisection', json={
        "function": "x**3 - x - 2",
        "interval": [1, 2],
        "tolerance": 0.001
    }, headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})  # Base64 for 'user:password'
    assert response.status_code == 201

def test_get_bisection(client):
    id = mongo.db.bisections.insert_one({
        "function": "x**3 - x - 2",
        "interval": [1, 2],
        "tolerance": 0.001,
        "root": 1.521484375
    }).inserted_id
    response = client.get(f'/bisection/{id}', headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200

def test_update_bisection(client):
    id = mongo.db.bisections.insert_one({
        "function": "x**3 - x - 2",
        "interval": [1, 2],
        "tolerance": 0.001,
        "root": 1.521484375
    }).inserted_id
    response = client.put(f'/bisection/{id}', json={
        "interval": [1, 2.5],
        "tolerance": 0.0001
    }, headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200

def test_delete_bisection(client):
    id = mongo.db.bisections.insert_one({
        "function": "x**3 - x - 2",
        "interval": [1, 2],
        "tolerance": 0.001,
        "root": 1.521484375
    }).inserted_id
    response = client.delete(f'/bisection/{id}', headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="})
    assert response.status_code == 200
