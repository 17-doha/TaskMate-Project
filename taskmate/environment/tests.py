from django.test import TestCase
from signup.models import User
from .models import Environment, Table, SearchHistory, UserCanAccess
from django.urls import reverse
from task.models import Task
from signup.models import User
from django.utils import timezone
import datetime
import json
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.client import RequestFactory

# class ModelsTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='password123'
#         )
        
#         self.environment = Environment.objects.create(
#             label='Test Environment',
#             is_private=True,
#             admin=self.user
#         )

#         self.table = Table.objects.create(
#             label='Test Table',
#             environment=self.environment
#         )

#         self.search_history = SearchHistory.objects.create(
#             content='Test Search Content',
#             user_id=self.user
#         )

#         self.user_access = UserCanAccess.objects.create(
#             type_of_accessibility='Participant',
#             invitation_status='Pending',
#             user=self.user,
#             environment=self.environment
#         )

#     def test_environment_creation(self):
#         self.assertEqual(self.environment.label, 'Test Environment')
#         self.assertEqual(self.environment.admin, self.user)
#         self.assertTrue(self.environment.is_private)

#     def test_table_creation(self):
#         self.assertEqual(self.table.label, 'Test Table')
#         self.assertEqual(self.table.environment, self.environment)

#     def test_search_history_creation(self):
#         self.assertEqual(self.search_history.content, 'Test Search Content')
#         self.assertEqual(self.search_history.user_id, self.user)

#     def test_user_can_access_creation(self):
#         self.assertEqual(self.user_access.type_of_accessibility, 'Participant')
#         self.assertEqual(self.user_access.invitation_status, 'Pending')
#         self.assertEqual(self.user_access.user, self.user)
#         self.assertEqual(self.user_access.environment, self.environment)

#     def test_user_can_access_methods(self):
#         # Test granting access
#         self.user_access.grant_access()
#         self.assertEqual(self.user_access.type_of_accessibility, 'Participant')

#         # Test revoking access
#         self.user_access.revoke_access()
#         self.assertEqual(self.user_access.type_of_accessibility, 'Revoked')

#         # Test checking access
#         self.user_access.type_of_accessibility = 'subadmin'
#         self.assertTrue(self.user_access.check_access())

#         self.user_access.type_of_accessibility = 'Revoked'
#         self.assertFalse(self.user_access.check_access())

#     def test_user_can_access_invitation_status_update(self):
#         # Test updating invitation status
#         self.user_access.update_invitation_status('Accepted')
#         self.assertEqual(self.user_access.invitation_status, 'Accepted')

#         self.user_access.update_invitation_status('Rejected')
#         self.assertEqual(self.user_access.invitation_status, 'Rejected')

#     def test_environment_str(self):
#         self.assertEqual(str(self.environment), 'Test Environment')

class EnvironmentViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.login(username='testuser', password='password123')

        # Set up session with user_id
        factory = RequestFactory()
        request = factory.get('/')
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        self.client.session['user_id'] = self.user.id
        self.client.session.save()

        # Create environments
        self.environment1 = Environment.objects.create(
            label='Test Environment',
            is_private=True,
            admin=self.user
        )

        self.environment2 = Environment.objects.create(
            label='Another Environment',
            is_private=True,
            admin=self.user
        )


# # ------------------------------- Test View Table Task -------------------------------
#     def test_view_table_task_with_id(self):
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()

#         url = reverse('environment:view_table_task', args=[self.environment1.environment_id])
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Test Environment')
#         self.assertTemplateUsed(response, 'environment/index.html')

#     def test_view_table_task_redirects_to_first_environment(self):
#         """
#         It should redirect the user to the first environment created by them.
#         Test with non extisting environment
#         """
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()

#         invalid_environment_id = 999
#         url = reverse('environment:view_table_task', args=[invalid_environment_id]) 
#         response = self.client.get(url)

#         expected_redirect_url = reverse('environment:view_table_task', args=[self.environment1.environment_id])
#         self.assertRedirects(response, expected_redirect_url)

#     def test_view_table_task_no_environment(self):
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()
#         Environment.objects.all().delete() 
#         url = reverse('environment:view_table_task', args=[0])  
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, 404)

# # ------------------------------- Test Add Environment -------------------------------
#     def test_add_environment_success(self):
#         url = reverse('environment:add_environment')
#         data = {
#             'label': 'New Environment'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {'success': True, 'message': "Environment 'New Environment' added successfully."})

#         # Check if the environment and tables were created
#         environment = Environment.objects.get(label='New Environment')
#         self.assertIsNotNone(environment)
#         self.assertEqual(environment.admin, self.user)

#         tables = Table.objects.filter(environment=environment)
#         self.assertEqual(tables.count(), 3)
#         self.assertTrue(tables.filter(label='To Do').exists())
#         self.assertTrue(tables.filter(label='Done').exists())
#         self.assertTrue(tables.filter(label='In Progress').exists())

#     def test_add_environment_missing_label(self):
#         url = reverse('environment:add_environment')
#         response = self.client.post(url, {})
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {'success': False, 'error': 'Environment label is required.'})

#     def test_add_environment_duplicate_label(self):
#         url = reverse('environment:add_environment')
#         data = {
#             'label': 'Test Environment'
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {'success': False, 'error': 'An environment with this label already exists.'})

# # ------------------------------- Test Search Environment -------------------------------
#     def test_search_environment_success(self):
#         url = reverse('environment:search_environment')
#         data = {
#             'searched': 'Test'
#         }

#         # Set the session key for user_id
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()

#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'search_environment.html')
#         self.assertContains(response, 'Test Environment')



#     def test_search_environment_no_results(self):
#         url = reverse('environment:search_environment')
#         data = {
#             'searched': 'NonExistentEnvironment'
#         }
        
#         # Set the session key for user_id
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'search_environment.html')
#         self.assertNotContains(response, 'Test Environment')



#     def test_search_environment_get_request(self):
#         url = reverse('environment:search_environment')
        
#         # Set the session key for user_id explicitly
#         session = self.client.session
#         session['user_id'] = self.user.id 
#         session.save()

#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'search_environment.html')
#         self.assertNotContains(response, 'Test Environment')
#         self.assertNotContains(response, 'Another Environment')


# ------------------------------- Test Search Environment -------------------------------
