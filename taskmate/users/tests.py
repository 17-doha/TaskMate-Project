from django.test import TestCase
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.shortcuts import render, redirect
from django.contrib import messages
from signup.models import User
from django.contrib.auth.hashers import check_password
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from django.contrib.auth import login, logout
from _profile.views import profile_view
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model




class LoginUserTestCase(TestCase):
    '''
    Test the login by setting first correct email and password and create this user with the hashed password 
    and then try to login

    Test input a non existing email and it should return message saying wrong email

    Test input wrong password and it should return message saying wrong password

    Test that user is logged in and try to log in again so redirects to profile


    '''

    def setUp(self):
        """
        Setup a test user in the database.
        """
        self.email = "dohaahemdan@gmail.com"
        self.password = "Dohah@885522"
        self.user = User.objects.create(
            email=self.email,
            password=make_password(self.password)  
        )
        self.url = reverse('login')  

    def test_login_successful(self):
        """
        Test successful login with correct credentials.
        """
        response = self.client.post(self.url, {
            'email': self.email,
            'password': self.password
        })
  
        self.assertEqual(response.url, '/main/')  
        self.assertEqual(self.client.session.get('user_id'), self.user.id)


    def test_login_email_not_found(self):
        """
        Test login with email not found in the system.
        """
        nonexistent_email = "nonexistent@example.com"
        response = self.client.post(self.url, {
            'email': nonexistent_email,
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Email not correct. Please check your input.')  


    def test_login_password_not_correct(self):
        """
        Test login with email not found in the system.
        """
        not_correct_password = "wrong_password"
        response = self.client.post(self.url, {
            'email': self.email,
            'password': not_correct_password
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Incorrect password. Please try again.')  


    def test_user_logged_in_redirect(self):
        """
        Test that a logged-in user is redirected to the profile page.
        """
        session = self.client.session
        session['user_id'] = self.user.id  
        session.save()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.url, '/profile/') 




class MainViewTestCase(TestCase):
    """
    Test that a user is redirected to their own '/main/user_id/' 
    if they try to access '/main/<id>' with a mismatched ID.
    """

    def setUp(self):
        """
        Setup a test user in the database.
        """
        self.user = User.objects.create_user(
            username="dohaahemdan",
            email="dohaahemdan@gmail.com",
            password="Dohah@885522"
        )
        self.url = reverse('main')  


    def test_redirect_mismatched_user_id(self):
     
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        mismatched_user_id = self.user.id + 1 
        response = self.client.get(f'/main/{mismatched_user_id}/')

     
        self.assertRedirects(response, f'/main/{self.user.id}/')




User = get_user_model()

class GoogleSignInCallbackTestCase(TestCase):

    def setUp(self):
        """
        Set up test data for the Google sign-in callback tests.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username="dohaahemdan",
            email="s-doha.hassanien@zewailcity.edu.eg"
        )

        # Create a social account for the user
        self.social_account_data = {
            "provider": "google",
            "uid": "123456789",
            "extra_data": {
                "email": "s-doha.hassanien@zewailcity.edu.eg",
                "name": "DohaHemdan"
            }
        }

        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider=self.social_account_data["provider"],
            uid=self.social_account_data["uid"],
            extra_data=self.social_account_data["extra_data"]
        )

    def test_authenticated_user_existing_account(self):
        """
        Test that an authenticated user with an existing account is redirected to the main page.
        """
        self.client.force_login(self.user) 

        response = self.client.get(reverse('google_sign_in_callback')) 
        self.assertRedirects(response, f"/main/{self.user.id}/")

    def test_authenticated_user_new_account(self):
        """
        Test that a new user is created and redirected to the main page if not already registered.
        """
        new_user_email = "doha.hemdan7@gmail.com"

        # Create a social account with a new email for a different user
        new_social_account_data = {
            "provider": "google",
            "uid": "987654321",
            "extra_data": {
                "email": new_user_email,
                "name": "DohaHemdan7"
            }
        }

        new_social_account = SocialAccount.objects.create(
            user=self.user,
            provider=new_social_account_data["provider"],
            uid=new_social_account_data["uid"],
            extra_data=new_social_account_data["extra_data"]
        )

        self.client.force_login(self.user)  

        response = self.client.get(reverse('google_sign_in_callback'))  
        self.assertEqual(response.status_code, 302)

    
        session = self.client.session
        session['user_id'] = self.user.id  
        session.save()
        self.assertRedirects(response, f"/main/{self.user.id }/")



  
