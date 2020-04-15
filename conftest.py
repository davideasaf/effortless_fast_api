from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests import Session

from main import api


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    client = TestClient(api)

    yield client


@pytest.fixture(scope="module")
def test_app() -> Generator[FastAPI, None, None]:
    yield api
