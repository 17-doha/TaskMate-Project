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
    
    def generate_random_credentials(self):
        """Generates random email and password for testing."""
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return random_email, random_password

    @task
    def login(self):
        # Fetch CSRF token from the login page
        response = self.client.get("/login/")
        csrf_token = response.cookies.get("csrftoken", None)

        if not csrf_token:
            print("Failed to retrieve CSRF token")
            return

        # Simulate login using test credentials
        login_data = {
            "email": "existing_user@example.com",  # Replace with a valid test email
            "password": "password123"             # Replace with a valid test password
        }
        headers = {"X-CSRFToken": csrf_token}
        response = self.client.post("/login/", data=login_data, headers=headers)

        if response.status_code == 200:
            print("Login succeeded!")
        else:
            print(f"Login failed: {response.status_code}, {response.text}")

    @task
    def view_all_tasks(self):
        self.client.get("/task/viewall/")





