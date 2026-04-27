from playwright.sync_api import Page
import allure


class GroceryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_cards = page.locator(".products > .product")

    def navigate(self, url: str):
        self.page.goto(url)

    def get_product_count(self) -> int:
        with allure.step("Get product count"):
            return self.product_cards.count()
