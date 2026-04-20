from playwright.sync_api import Page

class TodoPage:
    URL = "https://demo.playwright.dev/todomvc"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.new_todo_input = page.locator(".new-todo")
        self.todo_items = page.locator(".todo-list li")
    
    def navigate(self):
        self.page.goto(self.URL)

    def add_item(self, title: str):
        self.new_todo_input.fill(title)
        self.new_todo_input.press("Enter")

    def item_exists(self, title: str) -> bool:
        return self.todo_items.filter(has_text=title).count() > 0
    
