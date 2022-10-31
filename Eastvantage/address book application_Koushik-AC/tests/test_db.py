from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from db import Base, get_db
from main import app


DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_NAME = config.TEST_DATABASE_NAME

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/account/",
        json={"username": "Deadpool", "email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "deadpool@example.com"


def test_duplicate_user():
    response = client.post(
        "/account/",
        json={"username": "Deadpool", "email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "This user with this email already exists in the system."
    
