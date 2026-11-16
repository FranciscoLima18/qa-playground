"""End-to-end tests for the SauceDemo store: login and purchase flow.

Test users and the shared password are published on the SauceDemo login page.
"""

import pytest
from playwright.sync_api import Page, expect

from pages.sauce_pages import CheckoutFlow, InventoryPage, LoginPage

pytestmark = pytest.mark.web

PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


def test_standard_user_can_log_in(login_page: LoginPage, page: Page) -> None:
    login_page.login("standard_user", PASSWORD)

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        ("locked_out_user", PASSWORD, "Sorry, this user has been locked out."),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked-out", "wrong-password", "missing-username", "missing-password"],
)
def test_invalid_login_shows_error(
    login_page: LoginPage, username: str, password: str, expected_error: str
) -> None:
    login_page.login(username, password)

    expect(login_page.error).to_contain_text(expected_error)


def test_checkout_flow_completes_order(login_page: LoginPage, page: Page) -> None:
    login_page.login("standard_user", PASSWORD)
    inventory = InventoryPage(page)

    inventory.add_to_cart("sauce-labs-backpack")
    inventory.add_to_cart("sauce-labs-bike-light")
    expect(inventory.cart_badge).to_have_text("2")

    inventory.open_cart()
    checkout = CheckoutFlow(page)
    expect(checkout.cart_items).to_have_count(2)

    checkout.checkout("Ada", "Lovelace", "11300")

    expect(checkout.complete_header).to_have_text("Thank you for your order!")
