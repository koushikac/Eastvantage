![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


The goal of this assignment is to demonstrate your existing Python3 skills and how you can
create a minimal API using FastAPI.

```mermaid
erDiagram
    TASK {
        int id
        string name
        string description
    }
    USER {
        int id
        string username
        string email
        string password
    }
    ADDRESS {
        int id
        int user_id
        string shipping_address
        string created_at
    }
```

## Database

Postgres is used for the database and Alembic package is used for migrations which means accomodating real time changes in the database. The code sample below demonstates the integration of SQLAlchemy and Postgres in a FastAPI project.

```
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:pass12345@127.0.0.1/address-book"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

## Testing with Pytest

A separate database is used exclusively for testing, configuration has been put inside a config.py file in the root folder of the project.

```
DATABASE_USERNAME = 'postgres'
DATABASE_PASSWORD = 'pass12345'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'address-book'

TEST_DATABASE_NAME = 'address-book-test'
```

Code to test the app root end-point. We need to make sure 200 status code is returned when we hit this route.

```
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Address Book API"}
```

test_db.py 

```
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
```




