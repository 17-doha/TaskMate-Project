# Notification/tests.py

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from .models import Notification
from signup.models import User  # Ensure this is the correct path to your User model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
import datetime

User = get_user_model()

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class NotificationViewTests(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = Client()

        # Create test users
        self.user_with_notifications = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )

        self.user_without_notifications = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

        # Create notifications for user_with_notifications
        self.notification1 = Notification.objects.create(
            content='You have a new invitation.',
            type='INVIT',
            status='UNREAD',
            receiver=self.user_with_notifications
        )

        self.notification2 = Notification.objects.create(
            content='Your task has been updated.',
            type='TASK',
            status='READ',
            receiver=self.user_with_notifications
        )

    def _login_user(self, user):
        """
        Helper method to log in a user by setting 'user_id' in the session.
        """
        session = self.client.session
        session['user_id'] = user.id
        session.save()

    def test_fetch_notifications_authenticated_with_notifications(self):
        """
        Ensure that an authenticated user with notifications receives them correctly.
        """
        self._login_user(self.user_with_notifications)
        url = reverse('Notification:fetch_notifications')  # Use namespaced URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "notifications": [
                    {
                        "id": self.notification1.notification_id,
                        "content": self.notification1.content,
                        "status": self.notification1.status
                    },
                    {
                        "id": self.notification2.notification_id,
                        "content": self.notification2.content,
                        "status": self.notification2.status
                    }
                ]
            }
        )

    def test_fetch_notifications_authenticated_no_notifications(self):
        """
        Ensure that an authenticated user without notifications receives an empty list.
        """
        self._login_user(self.user_without_notifications)
        url = reverse('Notification:fetch_notifications')  # Use namespaced URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"notifications": []})

    def test_fetch_notifications_not_authenticated(self):
        """
        Ensure that an unauthenticated user receives a 401 Unauthorized response.
        """
        url = reverse('Notification:fetch_notifications')  # Use namespaced URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"error": "User not authenticated"})

    def test_fetch_notifications_user_does_not_exist(self):
        """
        Ensure that if the user_id in session does not correspond to any user, a 404 Not Found is returned.
        """
        # Set a non-existent user_id in session
        session = self.client.session
        session['user_id'] = 9999  # Assuming this ID does not exist
        session.save()

        url = reverse('Notification:fetch_notifications')  # Use namespaced URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {"error": "User not found"})

    def test_mark_read_valid_request(self):
        """
        Ensure that a valid POST request successfully marks a notification as read.
        """
        self._login_user(self.user_with_notifications)
        url = reverse('Notification:mark_read', kwargs={'notification_id': self.notification1.notification_id})  # Use namespaced URL
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "success"})

        # Refresh the notification from the database
        self.notification1.refresh_from_db()
        self.assertEqual(self.notification1.status, "READ")

    def test_mark_read_invalid_notification_id(self):
        """
        Ensure that a POST request with an invalid notification_id returns a 404 Not Found.
        """
        self._login_user(self.user_with_notifications)
        invalid_notification_id = 9999  # Assuming this ID does not exist
        url = reverse('Notification:mark_read', kwargs={'notification_id': invalid_notification_id})  # Use namespaced URL
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Notification does not exist."}
        )

    def test_mark_read_notification_not_owned_by_user(self):
        """
        Ensure that a user cannot mark another user's notification as read.
        """
        # Create a notification for user_without_notifications
        other_notification = Notification.objects.create(
            content='This is another user\'s notification.',
            type='OTHER',
            status='UNREAD',
            receiver=self.user_without_notifications
        )

        self._login_user(self.user_with_notifications)
        url = reverse('Notification:mark_read', kwargs={'notification_id': other_notification.notification_id})  # Use namespaced URL
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Notification does not exist."}
        )

    def test_mark_read_not_authenticated(self):
        """
        Ensure that an unauthenticated user cannot mark notifications as read.
        """
        url = reverse('Notification:mark_read', kwargs={'notification_id': self.notification1.notification_id})  # Use namespaced URL
        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "User not authenticated"}
        )

    def test_mark_read_invalid_method(self):
        """
        Ensure that non-POST requests to mark_read return a 400 Bad Request.
        """
        self._login_user(self.user_with_notifications)
        url = reverse('Notification:mark_read', kwargs={'notification_id': self.notification1.notification_id})  # Use namespaced URL
        
        # Attempt a GET request
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Invalid request method."}
        )
        
        # Attempt a PUT request
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"status": "error", "message": "Invalid request method."}
        )

    def test_mark_read_expired_token(self):
        """
        (Optional) If you have token-based access, ensure that expired tokens are handled.
        """
        # This test is not directly applicable since your views do not use tokens.
        # However, if you implement token-based access in the future, you can add tests here.
        pass

    def test_fetch_notifications_runtime_warning(self):
        """
        (Optional) Ensure that no RuntimeWarnings related to naive datetime objects are raised.
        """
        # This can be monitored via Django's test settings or by using Python's warnings module.
        # For simplicity, we ensure that our test data uses timezone-aware datetimes.
        self.assertTrue(timezone.is_aware(self.notification1.created_at))
        self.assertTrue(timezone.is_aware(self.notification2.created_at))
