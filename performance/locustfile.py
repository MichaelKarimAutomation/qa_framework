from locust import HttpUser, task, between


class APIUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"
    wait_time = between(1, 3)

    @task(2)
    def get_post(self):
        self.client.get("/posts/1")

    @task(1)
    def create_post(self):
        self.client.post("/posts", json={
            "title": "Load Test Post",
            "body": "Testing under load",
            "userId": 1
        })