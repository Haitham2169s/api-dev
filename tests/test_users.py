from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get("Hello"))
    assert res.json().get("Hello") == "Welcome to my api"
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    print(res.json())

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
