import json
import pytest
import allure
from pom.grocery_page import GroceryPage


@allure.feature("UI Mocking")
@allure.story("Mock product list")
@pytest.mark.ui
@pytest.mark.regression
def test_mock_product_list(page, grocery_url):
    mock_products = [
        {"id": 1, "name": "Brocolli - 1 Kg", "price": 120, "image": "./images/broccoli.jpg", "category": "vegetables"},
        {"id": 2, "name": "Cauliflower - 1 Kg", "price": 60, "image": "./images/cauliflower.jpg", "category": "vegetables"},
    ]

    def mock_response(route):
        route.fulfill(status=200, content_type="application/json", body=json.dumps(mock_products))

    page.route("**/products.json", mock_response)

    grocery = GroceryPage(page)
    grocery.navigate(grocery_url)

    with allure.step("Verify only mocked products are shown"):
        assert grocery.get_product_count() == 2
