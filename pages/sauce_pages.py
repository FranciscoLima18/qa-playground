"""Page Objects for the Sauce Labs demo store (https://www.saucedemo.com)."""

from playwright.sync_api import Locator, Page

BASE_URL = "https://www.saucedemo.com/"


def by_data_test(page: Page, value: str) -> Locator:
    """SauceDemo uses data-test attributes (not data-testid)."""
    return page.locator(f'[data-test="{value}"]')


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = by_data_test(page, "username")
        self.password = by_data_test(page, "password")
        self.submit = by_data_test(page, "login-button")
        self.error = by_data_test(page, "error")

    def open(self) -> None:
        self.page.goto(BASE_URL)

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = by_data_test(page, "title")
        self.cart_badge = by_data_test(page, "shopping-cart-badge")
        self.cart_link = by_data_test(page, "shopping-cart-link")

    def add_to_cart(self, product_slug: str) -> None:
        by_data_test(self.page, f"add-to-cart-{product_slug}").click()

    def open_cart(self) -> None:
        self.cart_link.click()


class CheckoutFlow:
    """Cart, customer information, overview and completion steps."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_items = by_data_test(page, "inventory-item")
        self.complete_header = by_data_test(page, "complete-header")

    def checkout(self, first_name: str, last_name: str, postal_code: str) -> None:
        by_data_test(self.page, "checkout").click()
        by_data_test(self.page, "firstName").fill(first_name)
        by_data_test(self.page, "lastName").fill(last_name)
        by_data_test(self.page, "postalCode").fill(postal_code)
        by_data_test(self.page, "continue").click()
        by_data_test(self.page, "finish").click()
