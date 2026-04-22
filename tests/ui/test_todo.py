import pytest
from pages.todo_page import TodoPage


@pytest.mark.ui
@pytest.mark.smoke
def test_add_todo_item(page, todo_url):
    todo = TodoPage(page)
    todo.navigate(todo_url)
    todo.add_item("Buy milk")
    assert todo.item_exists("Buy milk")
