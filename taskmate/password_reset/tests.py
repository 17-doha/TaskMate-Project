# password_reset/tests.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import re

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetTestCase(TestCase):
    """
    Test cases for password reset functionality.
    """

    def setUp(self):
        """
        Setup a test user in the database.
        """
        self.client = Client()
        self.user_email = 'testuser@example.com'
        self.user_password = 'TestPassword123'
        self.user = User.objects.create_user(
            username='testuser',
            email=self.user_email,
            password=self.user_password
        )
        self.password_reset_url = reverse('password_reset')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_confirm_url = lambda uidb64, token: reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        self.password_reset_complete_url = reverse('password_reset_complete')
        mail.outbox = []  # Clear the outbox before each test
        self.client.logout()  # Ensure user is logged out before each test

    def test_password_reset_view_status_code(self):
        """
        Test that the password reset view returns a 200 status code.
        """
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset/password_reset.html')

    def test_password_reset_form_submission_valid_email(self):
        """
        Test submitting the password reset form with a valid email sends an email.
        """
        response = self.client.post(self.password_reset_url, {'email': self.user_email})
        self.assertEqual(response.status_code, 302)  # Redirect to 'password_reset_done'
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 1)
        # Check email content
        self.assertIn('Password reset', mail.outbox[0].subject)
        self.assertIn(self.user_email, mail.outbox[0].to)

    def test_password_reset_form_submission_invalid_email(self):
        """
        Test submitting the password reset form with an invalid email does not send an email.
        """
        invalid_email = 'nonexistent@example.com'
        response = self.client.post(self.password_reset_url, {'email': invalid_email})
        self.assertEqual(response.status_code, 302)  # Redirect to 'password_reset_done'
        self.assertRedirects(response, self.password_reset_done_url)
        self.assertEqual(len(mail.outbox), 0)  # No email sent

    def test_password_reset_done_view_status_code(self):
        """
        Test that the password reset done view returns a 200 status code.
        """
        response = self.client.get(self.password_reset_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset/password_reset_done.html')

