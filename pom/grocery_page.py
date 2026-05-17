from playwright.sync_api import Page
import allure


class GroceryPage:
    def __init__(self, page: Page) -> None:
        """Initialize the grocery page wrapper and locate all product cards on the page."""
        self.page = page
        self.product_cards = page.locator('.products > .product')

    def navigate(self, url: str):
        """Open the grocery page at the given URL in the browser."""
        self.page.goto(url)

    def get_product_count(self) -> int:
        """Return the number of product cards currently displayed on the grocery page."""
        with allure.step('Get product count'):
            return self.product_cards.count()
