from locust import HttpUser, task, between
import random
from django.views.decorators.csrf import csrf_exempt
class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # wait time between requests (1-5 seconds)
    

import string

class LoadTestUser(HttpUser):
    wait_time = between(1, 5)  # Simulates user think time

    def generate_random_email(self):
        """Generates a random email for signup."""
        domain = "example.com"
        random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{random_name}@{domain}"

    @task
    def signup(self):
        csrf_token = self.client.get("/signup/").cookies.get("csrftoken")
        signup_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": self.generate_random_email(),
            "password": "password123",
            "confirm_password": "password123"
        }
        headers = {"X-CSRFToken": csrf_token}
        response = self.client.post("/signup/", data=signup_data, headers=headers)
        if response.status_code != 200:
            print(f"Signup failed: {response.status_code}, {response.text}")




