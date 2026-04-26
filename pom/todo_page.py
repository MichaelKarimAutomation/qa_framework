import allure
from playwright.sync_api import Page


class TodoPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo_input = page.locator(".new-todo")
        self.todo_items = page.locator(".todo-list li")

    def navigate(self, url: str):
        self.page.goto(url)

    def add_item(self, title: str):
        with allure.step(f"Add todo item: {title}"):
            self.new_todo_input.fill(title)
        self.new_todo_input.press("Enter")

    def item_exists(self, title: str) -> bool:
        with allure.step(f"Check item exists: {title}"):
            return self.todo_items.filter(has_text=title).count() > 0
