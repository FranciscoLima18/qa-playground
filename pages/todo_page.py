"""Page Object for Playwright's official TodoMVC demo."""

from playwright.sync_api import Locator, Page


class TodoPage:
    URL = "https://demo.playwright.dev/todomvc/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo: Locator = page.get_by_placeholder("What needs to be done?")
        self.items: Locator = page.get_by_test_id("todo-item")
        self.counter: Locator = page.get_by_test_id("todo-count")

    def open(self) -> None:
        self.page.goto(self.URL)

    def add(self, *titles: str) -> None:
        for title in titles:
            self.new_todo.fill(title)
            self.new_todo.press("Enter")

    def item(self, title: str) -> Locator:
        return self.items.filter(has_text=title)

    def complete(self, title: str) -> None:
        self.item(title).get_by_role("checkbox").check()

    def delete(self, title: str) -> None:
        item = self.item(title)
        item.hover()
        item.locator("button.destroy").click()

    def show(self, filter_name: str) -> None:
        """Click one of the footer filters: All, Active or Completed."""
        self.page.get_by_role("link", name=filter_name).click()
