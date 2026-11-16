"""Shared fixtures for web and API tests."""

import os

import pytest
from playwright.sync_api import APIRequestContext, Playwright

BOOKER_URL = os.getenv("BOOKER_URL", "https://restful-booker.herokuapp.com")
# Public demo credentials published by Restful-Booker; override with env vars if needed.
BOOKER_USER = os.getenv("BOOKER_USER", "admin")
BOOKER_PASS = os.getenv("BOOKER_PASS", "password123")


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    """HTTP client for the Restful-Booker API (Playwright's built-in request context)."""
    context = playwright.request.new_context(
        base_url=BOOKER_URL,
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def booker_token(api: APIRequestContext) -> str:
    """Auth token required by Restful-Booker for update and delete operations."""
    response = api.post("/auth", data={"username": BOOKER_USER, "password": BOOKER_PASS})
    assert response.ok, f"Auth request failed: {response.status}"
    token = response.json().get("token")
    assert token, f"No token in auth response: {response.text()}"
    return token
