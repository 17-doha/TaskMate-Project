from locust import HttpUser, task, between
import random
import string

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)  # wait time between requests (1-5 seconds)

    def generate_random_email(self):
        """Generates a random email for signup."""
        domain = "example.com"
        random_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{random_name}@{domain}"

    def generate_random_credentials(self):
        """Generates random email and password for testing."""
        random_email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return random_email, random_password

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

        @task
        def login_and_view_profile(self):
            # First, simulate visiting the login page to get the CSRF token
            response = self.client.get("/login/")
            csrf_token = response.cookies.get("csrftoken")
            
            if not csrf_token:
                print("CSRF token missing")
                return
            
            # Now, perform login with CSRF token included in the headers
            login_data = {
                "email": "existing_user@example.com", 
                "password": "password123"
            }
            headers = {
                "X-CSRFToken": csrf_token
            }
            
            login_response = self.client.post("/login/", data=login_data, headers=headers)
            
            if login_response.status_code == 200:
                print("Login succeeded!")

                # After logging in, fetch the profile page
                profile_response = self.client.get("/profile/", headers={"X-CSRFToken": csrf_token})
                
                if profile_response.status_code == 200:
                    print("Profile page loaded successfully.")
                else:
                    print(f"Failed to load profile page: {profile_response.status_code}, {profile_response.text}")
            else:
                print(f"Login failed: {login_response.status_code}, {login_response.text}")


    @task
    def view_all_tasks(self):
        self.client.get("/task/viewall/")

   