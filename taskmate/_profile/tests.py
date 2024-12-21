from django.test import TestCase
from django.urls import reverse
from task.models import Task
from environment.models import Environment, Table
from signup.models import User
from badge.models import Badge, UserBadge
from django.contrib.sessions.middleware import SessionMiddleware
from django.utils import timezone
from datetime import timedelta
from django.contrib.messages import get_messages

class ProfileViewTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name="John",
            last_name="Doe",
            age="20",
            phone_number="1234567890"
        )
        self.client.login(username='testuser', password='password123')

        # Set the session to include 'user_id'
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Create a badge
        self.badge = Badge.objects.first()

        # Create UserBadge relation
        UserBadge.objects.create(user=self.user, badge=self.badge)

        # Create tasks and assign them to the user
        self.environment = Environment.objects.create(
            label='Test Environment',
            admin=self.user,
            is_private=True
        )
        self.table = Table.objects.create(
            label='To Do',
            environment=self.environment
        )
        self.table2 = Table.objects.create(
            label='Done',
            environment=self.environment
        )
        start_date = timezone.now()
        deadline = timezone.now() + timedelta(days=1) 

        self.task1 = Task.objects.create(
            content="Test Task",
            status=Task.PENDING,  
            start_date=start_date,
            deadline=deadline,
            priority=Task.MEDIUM,
            table=self.table,
            created_by=self.user,
            assigned_to=self.user,
            environment_id=self.environment
        )
        self.task2 = Task.objects.create(
            content="Test Task",
            status=Task.COMPLETED,  
            start_date=start_date,
            deadline=deadline,
            priority=Task.MEDIUM,
            table=self.table2,
            created_by=self.user,
            assigned_to=self.user,
            environment_id=self.environment
        )

    def test_profile_view(self):
        # Send GET request to profile view
        response = self.client.get(reverse('_profile:profile_view'))
        # # Check that the response is OK
        self.assertEqual(response.status_code, 200)
        # # Check the context data
        self.assertIn('user_profile', response.context)
        self.assertIn('badges', response.context)
        self.assertEqual(response.context['user_profile'], self.user)

        # # Ensure badges are in the context and check that at least one badge is present
        self.assertIsInstance(response.context['badges'], list)
        self.assertGreater(len(response.context['badges']), 0)

        # # Ensure the badge name is correct
        badge_names = [badge['name'] for badge in response.context['badges']]
        self.assertIn('Task Starter', badge_names)

        # # Check that the percentage of completed tasks is correct
        completed_tasks_count = 1  # Task 1 is Done
        all_tasks_count = 2  # Task 1 and Task 2
        expected_percentage = (completed_tasks_count / all_tasks_count) * 100
        self.assertEqual(response.context['percentage'], expected_percentage)

    def tearDown(self):
        # Cleanup after tests
        self.user.delete()
        self.task1.delete()
        self.task2.delete()
        self.badge.delete()

class ProfileEditTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name="John",
            last_name="Doe",
            age="20",
            phone_number="1234567890"
        )
        self.client.login(username='testuser', password='password123')

        # Set the session to include 'user_id'
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        
    def test_profile_edit(self):
        # Send GET request to edit profile
        response = self.client.get(reverse('_profile:profile_edit'))
        
        # Check that the response is OK
        self.assertEqual(response.status_code, 200)
        
        # Check if form is in the context
        self.assertIn('form', response.context)
        
        # Check if user profile data is prefilled
        self.assertEqual(response.context['form'].instance.username, self.user.username)

        # Send a valid POST request to edit profile
        response = self.client.post(reverse('_profile:profile_edit'), {
            'phone_number': '1245465',
            'age': '12',
            'first_name': 'John',
            'last_name': 'Doe',
        })

        # Check if the form is valid 
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('_profile:profile_view'))
        
        # Check if user data is updated in the database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        
    def tearDown(self):
        # Cleanup after tests
        self.user.delete()



class ProfileDeleteTestCase(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name="John",
            last_name="Doe",
            age="20",
            phone_number="1234567890"
        )
        self.client.login(username='testuser', password='password123')

        # Set the session to include 'user_id'
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        
    def test_profile_delete(self):
        # Send GET request to delete profile
        response = self.client.get(reverse('_profile:profile_delete'))
        
        # Check that the user is deleted
        with self.assertRaises(User.DoesNotExist):
            self.user.refresh_from_db()
        
    def tearDown(self):
        # Cleanup after tests
        if self.user:
            self.user.delete()
