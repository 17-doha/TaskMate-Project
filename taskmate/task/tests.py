from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task, Environment, Table
from signup.models import User
from django.contrib.messages import get_messages
from environment.models import SearchHistory
class TaskViewsTestCase(TestCase):
    def setUp(self):
        # Set up a user and environment as before
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

        session = self.client.session
        session['user_id'] = self.user.id
        session.save()

        # Set up environment and table
        self.environment = Environment.objects.create(
            label='Test Environment',
            admin=self.user,
            is_private=True
        )

        self.table = Table.objects.create(
            label='To Do',
            environment=self.environment
        )

        # Create a task
        start_date = timezone.now()
        deadline = timezone.now() + timedelta(days=1)  # Adding one day to the current time

        self.task = Task.objects.create(
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


    def test_edit_task(self):
    # Ensure the task exists before updating
        self.assertEqual(self.task.content, "Test Task")

        # Prepare new datetime values for testing
        new_start_date = timezone.now() + timedelta(hours=2)
        new_deadline = timezone.now() + timedelta(days=2)  # Adding two days

        # Format these new datetime values as strings in the `datetime-local` format
        start_date_str = new_start_date.strftime('%Y-%m-%dT%H:%M')
        deadline_str = new_deadline.strftime('%Y-%m-%dT%H:%M')

        # Simulate POST request to update the task
        data = {
            'content': 'Updated Task',
            'status': Task.IN_PROGRESS,
            'priority': Task.HIGH,
            'assigned_to': self.user.id,  # Make sure to pass the user ID
            'start_date': start_date_str,
            'deadline': deadline_str,
        }

        # Send the POST request to the task edit URL
        response = self.client.post(reverse('task:edit_task', args=[self.task.task_id]), data)

        # Reload the task from the database to reflect changes
        self.task.refresh_from_db()

        # Assert that the response is successful
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Check if the task was updated correctly
        self.assertEqual(self.task.content, 'Updated Task')
        self.assertEqual(self.task.status, Task.IN_PROGRESS)

        # Compare the deadlines and start_dates up to seconds (ignoring microseconds)
        self.assertEqual(self.task.deadline.replace(microsecond=0, second=0), new_deadline.replace(microsecond=0, second=0))
        self.assertEqual(self.task.start_date.replace(microsecond=0, second=0), new_start_date.replace(microsecond=0, second=0))
    

    def test_delete_task(self):
        # Ensure the task exists before deletion
        task_count_before = Task.objects.count()
        self.assertEqual(task_count_before, 1)

        # Prepare the URL for deleting the task
        delete_url = reverse('task:delete_task', args=[self.task.task_id])

        # Send the DELETE request
        response = self.client.post(delete_url)

        # Check that the task was deleted and user is redirected
        task_count_after = Task.objects.count()
        self.assertEqual(task_count_after, 0)  # Task should be deleted

    def test_create_task(self):
        # **Scenario 1: POST Request (Successful Task Creation)**
        start_date = timezone.now()
        deadline = timezone.now() + timedelta(days=1)  # Adding one day to the current time
        self.client.login(username='testuser', password='password123')
        data = {
            'content': 'New Task',
            'status': Task.COMPLETED,
            'start_date': start_date.strftime('%Y-%m-%dT%H:%M'),
            'deadline': deadline.strftime('%Y-%m-%dT%H:%M'),
            'priority': Task.MEDIUM,
            'assigned_to': self.user.id,
            "created_by":self.user.id
        }

    #     # Send the POST request to create a new task
        response = self.client.post(reverse('task:create_task', args=[self.environment.environment_id]), data)

    #     # Check that the task was created successfully
        self.assertEqual(Task.objects.count(), 2)

        # # Check that the response is a redirect to the environment page
        self.assertRedirects(response, f'/environment/{self.environment.environment_id}/')

        # # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Task created successfully!')

        # **Scenario 2: POST Request (Failed Task Creation due to Invalid Data)**
        invalid_data = {
            'content': '',  # Content is required
            'status': Task.PENDING,
            'start_date': '',
            'deadline': '',
            'priority': Task.MEDIUM,
            'assigned_to': self.user.id,
        }

        # # Send the POST request with invalid data
        response = self.client.post(reverse('task:create_task', args=[self.environment.environment_id]), invalid_data)

        # # Check that no task was created
        self.assertEqual(Task.objects.count(), 2)


        # **Scenario 3: GET Request (Form Display)**
        # Send a GET request to create a new task (no data, just the form)
        response = self.client.get(reverse('task:create_task', args=[self.environment.environment_id]))

        # # Check that the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)

        # # Check that the correct template is used
        self.assertTemplateUsed(response, 'task/create_task.html')

        # # Check that the form is in the context
        self.assertIn('users', response.context)
        self.assertIn('environment_id', response.context)

    def test_search_task_post(self):
        # valid
        response = self.client.post(reverse('task:search_task'), {'searched': 'Test Task'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertEqual(len(response.context['tasks']), 1)

        # invalid
        response = self.client.post(reverse('task:search_task'), {'searched': 'Non-existing task'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tasks']), 0)

    def test_search_term_saved_in_history(self):
        response = self.client.post(reverse('task:search_task'), {'searched': 'Test Task'})
        self.assertTrue(SearchHistory.objects.filter(content='Test Task', user_id=self.user.id).exists())

        response = self.client.get(reverse('task:view_task', args=[self.task.task_id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/environment/{self.environment.environment_id}/')

        response = self.client.get(reverse('task:view_task', args=[9999]))  # Invalid task ID
        self.assertEqual(response.status_code, 404)