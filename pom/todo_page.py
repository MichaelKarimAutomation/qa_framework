import allure
from playwright.sync_api import Page


class TodoPage:
    def __init__(self, page: Page) -> None:
        """Initialize the todo page wrapper, locating the new-todo input and the rendered todo list items."""
        self.page = page
        self.new_todo_input = page.locator('.new-todo')
        self.todo_items = page.locator('.todo-list li')

    def navigate(self, url: str):
        """Open the todo application at the given URL in the browser."""
        self.page.goto(url)

    def add_item(self, title: str):
        """Type the given title into the new-todo input and submit it by pressing Enter."""
        with allure.step(f'Add todo item: {title}'):
            self.new_todo_input.fill(title)
        self.new_todo_input.press('Enter')

    def item_exists(self, title: str) -> bool:
        """Return True if at least one todo item with the given title is currently visible in the list."""
        with allure.step(f'Check item exists: {title}'):
            return self.todo_items.filter(has_text=title).count() > 0
