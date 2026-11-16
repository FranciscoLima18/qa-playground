"""End-to-end tests for the TodoMVC demo app."""

import pytest
from playwright.sync_api import Page, expect

from pages.todo_page import TodoPage

pytestmark = pytest.mark.web


@pytest.fixture
def todo(page: Page) -> TodoPage:
    todo_page = TodoPage(page)
    todo_page.open()
    return todo_page


def test_add_items_shows_them_in_order(todo: TodoPage) -> None:
    todo.add("Buy coffee", "Review PR", "Study algebra")

    expect(todo.items).to_have_text(["Buy coffee", "Review PR", "Study algebra"])
    expect(todo.counter).to_have_text("3 items left")


def test_completed_item_moves_between_filters(todo: TodoPage) -> None:
    todo.add("Buy coffee", "Review PR")
    todo.complete("Buy coffee")

    todo.show("Active")
    expect(todo.items).to_have_text(["Review PR"])

    todo.show("Completed")
    expect(todo.items).to_have_text(["Buy coffee"])
    expect(todo.counter).to_have_text("1 item left")


def test_delete_item(todo: TodoPage) -> None:
    todo.add("Keep me", "Delete me")
    todo.delete("Delete me")

    expect(todo.items).to_have_text(["Keep me"])


def test_items_persist_after_reload(todo: TodoPage, page: Page) -> None:
    todo.add("Persisted item")
    page.reload()

    expect(todo.items).to_have_text(["Persisted item"])


def test_empty_input_is_not_added(todo: TodoPage) -> None:
    todo.new_todo.press("Enter")

    expect(todo.items).to_have_count(0)
