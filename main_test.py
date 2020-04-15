from datetime import datetime
from fastapi.testclient import TestClient
from requests import Response

from unittest.mock import patch, MagicMock
from models.user import User

# from schemas.auth import Token


from main import api

client = TestClient(api)

EXAMPLE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2V4YW1wbGUuYXV0aDAuY29tLyIsImF1ZCI6Imh0dHBzOi8vYXBpLmV4YW1wbGUuY29tL2NhbGFuZGFyL3YxLyIsInN1YiI6InVzcl8xMjMiLCJpYXQiOjE0NTg3ODU3OTYsImV4cCI6MTQ1ODg3MjE5Nn0.CA7eaHjIHz5NxeIJoFK9krqaeZrPLwmMmgI_XiQiIkQ"


def create_test_db_user():
    return User(
        user_id=1,
        username="admin",
        password="password",
        roles=None,
        is_active=True,
        created_datetime=datetime(year=2020, month=1, day=1),
    )


def test_read_main():
    response: Response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World!"


@patch("main.user_service")
@patch("main.create_access_token")
def test_login(user_service_stub, create_access_token_stub):
    # Set up Stubs
    user_service_stub.authenticate.return_value = create_test_db_user()
    create_access_token_stub.return_value = EXAMPLE_ACCESS_TOKEN

    response: Response = client.post(
        "/login", {"username": "admin", "password": "password"}
    )
    assert response.status_code == 200
    # assert response.json() == Token(
    #     access_token=EXAMPLE_ACCESS_TOKEN, token_type="bearer"
    # )
