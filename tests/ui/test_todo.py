from pages.todo_page import TodoPage

def test_add_todo_item(page):
    todo = TodoPage(page)
    todo.navigate()
    todo.add_item("Buy milk")
    assert todo.item_exists("Buy milk")
