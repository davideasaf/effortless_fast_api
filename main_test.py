import json
from datetime import datetime
from typing import List
from unittest.mock import MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import parse_obj_as, BaseModel
from requests import Response

from models.user import User as DBUser
from schemas.auth import Token
from schemas.user import User, UserWithPassword
from utils.security_utils.route_dep import get_current_user

EXAMPLE_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2V4YW1wbGUuYXV0aDAuY29tLyIsImF1ZCI6Imh0dHBzOi8vYXBpLmV4YW1wbGUuY29tL2NhbGFuZGFyL3YxLyIsInN1YiI6InVzcl8xMjMiLCJpYXQiOjE0NTg3ODU3OTYsImV4cCI6MTQ1ODg3MjE5Nn0.CA7eaHjIHz5NxeIJoFK9krqaeZrPLwmMmgI_XiQiIkQ"


def create_test_db_user(*, is_active=True, roles=None):
    return DBUser(
        user_id=1,
        username="admin",
        password="password",
        roles=roles,
        is_active=is_active,
        created_datetime=datetime(year=2020, month=1, day=1),
    )


def get_current_user_ovveride(**kwargs):

    return lambda: create_test_db_user(**kwargs)


def test_read_main(test_client: TestClient):
    response: Response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World!"


class TestLoginController:
    @patch("main.create_access_token")
    @patch("main.user_service.authenticate")
    def test_successful_login(
        self, user_service_auth_stub, create_access_token_stub, test_client: TestClient
    ):
        # Set up Stubs
        user_service_auth_stub.return_value = create_test_db_user()
        create_access_token_stub.return_value = EXAMPLE_ACCESS_TOKEN

        # Make Call to Controller\
        response: Response = test_client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 200
        assert (
            response.json()
            == Token(access_token=EXAMPLE_ACCESS_TOKEN, token_type="bearer").dict()
        )

    @patch("main.user_service.authenticate")
    def test_user_not_found_for_login(
        self, user_service_auth_stub, test_client: TestClient
    ):
        # Set up Stubs
        user_service_auth_stub.return_value = None

        # Make Call to Controller
        response: Response = test_client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect email or password"}

    @patch("main.user_service.authenticate")
    def test_user_is_inactive_for_login(
        self, user_service_auth_stub, test_client: TestClient
    ):
        # Set up Stubs
        user_service_auth_stub.return_value = create_test_db_user(is_active=False)

        # Make Call to Controller
        response: Response = test_client.post(
            "/login", {"username": "admin", "password": "password"}
        )

        # Assertions
        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user"}


@patch("main.user_service.get_all")
class TestUserController:
    def test_get_all_users_with_passwords(
        self,
        user_service_get_all_stub: MagicMock,
        test_client: TestClient,
        test_app: FastAPI,
    ):
        # Set up Stubs
        test_app.dependency_overrides[get_current_user] = get_current_user_ovveride(
            roles="admin"
        )

        list_of_users = [
            create_test_db_user(),
            create_test_db_user(),
        ]

        class UsersWithPasswordList(BaseModel):
            __root__: List[UserWithPassword]

        user_service_get_all_stub.return_value = list_of_users

        # Make Call to Controller
        response: Response = test_client.get("/users-with-passwords")

        # Assertions
        assert response.status_code == 200
        assert (
            str(json.dumps(response.json()))
            == UsersWithPasswordList.parse_obj(list_of_users).json()
        )

    def test_get_all_users_admin_only(
        self,
        user_service_get_all_stub: MagicMock,
        test_client: TestClient,
        test_app: FastAPI,
    ):
        # Set up Stubs
        test_app.dependency_overrides[get_current_user] = get_current_user_ovveride(
            roles=None
        )

        # Make Call to Controller
        response: Response = test_client.get("/users-with-passwords")

        # Assertions
        assert response.status_code == 400
        assert response.json() == {"detail": "The user doesn't have enough privilege"}
