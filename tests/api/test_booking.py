"""API tests for Restful-Booker: health check, CRUD and authorization rules.

Restful-Booker is a public practice API with some intentional quirks
(for example, DELETE answers 201). The tests document that behavior.
"""

import pytest
from playwright.sync_api import APIRequestContext

pytestmark = pytest.mark.api

NEW_BOOKING = {
    "firstname": "Ada",
    "lastname": "Lovelace",
    "totalprice": 150,
    "depositpaid": True,
    "bookingdates": {"checkin": "2027-01-10", "checkout": "2027-01-15"},
    "additionalneeds": "Breakfast",
}

BOOKING_SCHEMA = {
    "firstname": str,
    "lastname": str,
    "totalprice": int,
    "depositpaid": bool,
    "bookingdates": dict,
}


def assert_matches_schema(body: dict) -> None:
    for field, expected_type in BOOKING_SCHEMA.items():
        assert field in body, f"Missing field: {field}"
        assert isinstance(body[field], expected_type), f"{field} should be {expected_type.__name__}"


@pytest.fixture
def booking_id(api: APIRequestContext, booker_token: str) -> int:
    """Create a fresh booking for the test and delete it afterwards."""
    response = api.post("/booking", data=NEW_BOOKING)
    assert response.status == 200
    new_id = response.json()["bookingid"]
    yield new_id
    api.delete(f"/booking/{new_id}", headers={"Cookie": f"token={booker_token}"})


def test_health_check(api: APIRequestContext) -> None:
    response = api.get("/ping")
    assert response.status == 201


def test_created_booking_can_be_read_back(api: APIRequestContext, booking_id: int) -> None:
    response = api.get(f"/booking/{booking_id}")

    assert response.status == 200
    body = response.json()
    assert_matches_schema(body)
    assert body["firstname"] == NEW_BOOKING["firstname"]
    assert body["bookingdates"] == NEW_BOOKING["bookingdates"]


def test_update_without_token_is_forbidden(api: APIRequestContext, booking_id: int) -> None:
    response = api.put(f"/booking/{booking_id}", data={**NEW_BOOKING, "totalprice": 1})

    assert response.status == 403


def test_update_with_token_changes_booking(
    api: APIRequestContext, booking_id: int, booker_token: str
) -> None:
    updated = {**NEW_BOOKING, "totalprice": 200, "additionalneeds": "Late checkout"}
    response = api.put(
        f"/booking/{booking_id}", data=updated, headers={"Cookie": f"token={booker_token}"}
    )

    assert response.status == 200
    assert response.json()["totalprice"] == 200
    assert response.json()["additionalneeds"] == "Late checkout"


def test_deleted_booking_is_not_found(api: APIRequestContext, booker_token: str) -> None:
    created = api.post("/booking", data=NEW_BOOKING)
    booking = created.json()["bookingid"]

    deleted = api.delete(f"/booking/{booking}", headers={"Cookie": f"token={booker_token}"})
    assert deleted.status == 201  # Restful-Booker quirk: DELETE returns 201 Created

    assert api.get(f"/booking/{booking}").status == 404


def test_auth_with_bad_credentials_returns_no_token(api: APIRequestContext) -> None:
    response = api.post("/auth", data={"username": "admin", "password": "wrong"})

    assert response.status == 200  # Restful-Booker answers 200 with a reason, not 401
    assert "token" not in response.json()
