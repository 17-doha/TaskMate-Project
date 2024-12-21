from django.test import TestCase
from django.urls import reverse
from signup.models import User

class SignupTestCase(TestCase):
    def setUp(self):
        """
        Set up test data.
        """
        self.signup_url = reverse('signup')  # Replace 'signup' with your actual signup URL name
        self.valid_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'Test1234',
            'confirm_password': 'Test1234'
        }
        self.invalid_user_data = {
            'first_name': '',
            'last_name': '',
            'email': 'invalid',
            'password': 'short',
            'confirm_password': 'mismatch'
        }

    def test_signup_success(self):
        """
        Test successful user signup.
        """
        response = self.client.post(self.signup_url, data=self.valid_user_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(email='john.doe@example.com').exists())

    def test_signup_password_mismatch(self):
        """
        Test signup with mismatched passwords.
        """
        data = self.valid_user_data.copy()
        data['confirm_password'] = 'Different123'
        response = self.client.post(self.signup_url, data=data)
        self.assertEqual(response.status_code, 200)  # Stay on signup page
        self.assertContains(response, "Passwords do not match!")

    def test_signup_invalid_email(self):
        """
        Test signup with an invalid email format.
        """
        # Invalid email data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalidemail",  # Invalid email format
            "password": "password123",
            "confirm_password": "password123"
        }
        
        response = self.client.post(self.signup_url, data)
        
        # Ensure the response does NOT redirect (status code 200 expected)
        self.assertEqual(response.status_code, 200)
        
        # Check that the error message is displayed
        self.assertContains(response, "Enter a valid email address.")  # Adjust message if needed




    def test_signup_email_already_registered(self):
        """
        Test signup with an already registered email.
        """
        User.objects.create_user(
            username='existinguser',
            email='john.doe@example.com',
            password='Existing1234'
        )
        response = self.client.post(self.signup_url, data=self.valid_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Email is already registered!")

