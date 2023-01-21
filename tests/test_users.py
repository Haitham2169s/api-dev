from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def overrid_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = overrid_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_root(client):
    res = client.get("/")
    print(res.json().get("Hello"))
    assert res.json().get("Hello") == "Welcome to my api"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    print(res.json())

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Hello World"}
