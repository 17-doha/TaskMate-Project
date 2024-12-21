from django.test import TestCase
from signup.models import User
from .models import Environment, Table, SearchHistory, UserCanAccess
from django.urls import reverse
from task.models import Task
from signup.models import User
from django.utils import timezone
import datetime

class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        
        self.environment = Environment.objects.create(
            label='Test Environment',
            is_private=True,
            admin=self.user
        )

        self.table = Table.objects.create(
            label='Test Table',
            environment=self.environment
        )

        self.search_history = SearchHistory.objects.create(
            content='Test Search Content',
            user_id=self.user
        )

        self.user_access = UserCanAccess.objects.create(
            type_of_accessibility='Participant',
            invitation_status='Pending',
            user=self.user,
            environment=self.environment
        )

    def test_environment_creation(self):
        self.assertEqual(self.environment.label, 'Test Environment')
        self.assertEqual(self.environment.admin, self.user)
        self.assertTrue(self.environment.is_private)

    def test_table_creation(self):
        self.assertEqual(self.table.label, 'Test Table')
        self.assertEqual(self.table.environment, self.environment)

    def test_search_history_creation(self):
        self.assertEqual(self.search_history.content, 'Test Search Content')
        self.assertEqual(self.search_history.user_id, self.user)

    def test_user_can_access_creation(self):
        self.assertEqual(self.user_access.type_of_accessibility, 'Participant')
        self.assertEqual(self.user_access.invitation_status, 'Pending')
        self.assertEqual(self.user_access.user, self.user)
        self.assertEqual(self.user_access.environment, self.environment)

    def test_user_can_access_methods(self):
        # Test granting access
        self.user_access.grant_access()
        self.assertEqual(self.user_access.type_of_accessibility, 'Participant')

        # Test revoking access
        self.user_access.revoke_access()
        self.assertEqual(self.user_access.type_of_accessibility, 'Revoked')

        # Test checking access
        self.user_access.type_of_accessibility = 'subadmin'
        self.assertTrue(self.user_access.check_access())

        self.user_access.type_of_accessibility = 'Revoked'
        self.assertFalse(self.user_access.check_access())

    def test_user_can_access_invitation_status_update(self):
        # Test updating invitation status
        self.user_access.update_invitation_status('Accepted')
        self.assertEqual(self.user_access.invitation_status, 'Accepted')

        self.user_access.update_invitation_status('Rejected')
        self.assertEqual(self.user_access.invitation_status, 'Rejected')

    def test_environment_str(self):
        self.assertEqual(str(self.environment), 'Test Environment')


class EnvironmentViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

        self.environment1 = Environment.objects.create(
            label='Test Environment',
            is_private=True,
            admin=self.user
        )

        self.table1 = Table.objects.create(
            label='Test Table',
            environment=self.environment1
        )

        start_date = timezone.make_aware(datetime.datetime(2023, 8, 1))
        deadline = timezone.make_aware(datetime.datetime(2025, 8, 31))

        self.task1 = Task.objects.create(
            content='Task1',
            status='Pending',
            table=self.table1,
            created_by=self.user,
            assigned_to=self.user, 
            start_date=start_date,
            deadline=deadline,
            priority='LOW'
        )

        self.task2 = Task.objects.create(
            content='Task2',
            status='In Progress',
            table=self.table1,
            created_by=self.user,
            assigned_to=self.user, 
            start_date=start_date,
            deadline=deadline,
            priority='HIGH'
        )

    def test_view_table_task_with_id(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        url = reverse('environment:view_table_task', args=[self.environment1.environment_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Environment')
        self.assertTemplateUsed(response, 'environment/index.html')

    def test_view_table_task_redirects_to_first_environment(self):
        """
        It should redirect the user to the first environment created by them.
        Test with non extisting environment
        """
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        invalid_environment_id = 999
        url = reverse('environment:view_table_task', args=[invalid_environment_id]) 
        response = self.client.get(url)

        expected_redirect_url = reverse('environment:view_table_task', args=[self.environment1.environment_id])
        self.assertRedirects(response, expected_redirect_url)

    def test_view_table_task_no_environment(self):
        session = self.client.session
        session['user_id'] = self.user.id
        session.save()
        Environment.objects.all().delete() 
        url = reverse('environment:view_table_task', args=[0])  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
