from datetime import datetime
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from requests import Response

from main import api
from models.user import User
from schemas.auth import Token

client = TestClient(api)

EXAMPLE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2V4YW1wbGUuYXV0aDAuY29tLyIsImF1ZCI6Imh0dHBzOi8vYXBpLmV4YW1wbGUuY29tL2NhbGFuZGFyL3YxLyIsInN1YiI6InVzcl8xMjMiLCJpYXQiOjE0NTg3ODU3OTYsImV4cCI6MTQ1ODg3MjE5Nn0.CA7eaHjIHz5NxeIJoFK9krqaeZrPLwmMmgI_XiQiIkQ"


def create_test_db_user(is_active=True):
    return User(
        user_id=1,
        username="admin",
        password="password",
        roles=None,
        is_active=is_active,
        created_datetime=datetime(year=2020, month=1, day=1),
    )


def test_read_main():
    response: Response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World!"


class TestLoginController:
    @patch("main.create_access_token")
    @patch("main.user_service.authenticate")
    def test_successful_login(self, user_service_auth_stub, create_access_token_stub):
        # Set up Stubs
        user_service_auth_stub.return_value = create_test_db_user()
        create_access_token_stub.return_value = EXAMPLE_ACCESS_TOKEN

        # Make Call to Controller
        response: Response = client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 200
        assert (
            response.json()
            == Token(access_token=EXAMPLE_ACCESS_TOKEN, token_type="bearer").dict()
        )

    @patch("main.user_service.authenticate")
    def test_user_not_found_for_login(self, user_service_auth_stub):
        # Set up Stubs
        user_service_auth_stub.return_value = None

        # Make Call to Controller
        response: Response = client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect email or password"}

    @patch("main.user_service.authenticate")
    def test_user_is_inactive_for_login(self, user_service_auth_stub):
        # Set up Stubs
        user_service_auth_stub.return_value = create_test_db_user(is_active=False)

        # Make Call to Controller
        response: Response = client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user"}
