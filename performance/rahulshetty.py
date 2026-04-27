from locust import HttpUser, task, between


# Demonstration only - do not run against third party sites without permission
class GroceryUser(HttpUser):
    host = "https://rahulshettyacademy.com"
    wait_time = between(1, 3)

    @task(3)
    def get_products(self):
        self.client.get("/seleniumPractise/data/products.json")

    @task(1)
    def load_home(self):
        self.client.get("/seleniumPractise/")
