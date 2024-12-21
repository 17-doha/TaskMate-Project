# from django.test import TestCase
# from django.utils.timezone import now
# from django.db.models import Q
# from django.urls import reverse
# from task.models import Task
# from environment.models import Table, Environment
# from signup.models import User
# import json
# from datetime import timedelta
# from main.views import (
#     get_tasks_with_environment,
#     get_priority_tasks_with_environment,
#     get_task_counts,
#     get_environment_stats,
# )


# class MainPageViewTestCase(TestCase):
#     def setUp(self):
#         """
#         Set up a test user, environment, and tasks for the tests.
#         """
#         # Create user using Django ORM
#         self.user = User.objects.create_user(
#             username="dohaahemdan",
#             email="dohaahemdan@gmail7.com",
#             password="Dohah@885522"
#         )

#         # Create environment and related objects
#         self.environment = Environment.objects.create(
#             label="Test Environment",
#             admin=self.user,
#             is_private=0
#         )
#         self.table1 = Table.objects.create(label="To Do", environment=self.environment)
#         self.table2 = Table.objects.create(label="In Progress", environment=self.environment)
#         self.table3 = Table.objects.create(label="Done", environment=self.environment)

#         # Create tasks
#         self.task1 = Task.objects.create(
#             assigned_to=self.user,
#             created_by=self.user,
#             status=Task.PENDING,
#             priority=Task.HIGH,
#             deadline=now() + timedelta(days=5),
#             environment_id=self.environment,
#             table=self.table1
#         )
#         self.task2 = Task.objects.create(
#             assigned_to=self.user,
#             created_by=self.user,
#             status=Task.IN_PROGRESS,
#             priority=Task.MEDIUM,
#             deadline=now() + timedelta(days=10),
#             environment_id=self.environment,
#             table=self.table2
#         )
#         self.task3 = Task.objects.create(
#             assigned_to=self.user,
#             created_by=self.user,
#             status=Task.COMPLETED,
#             priority=Task.LOW,
#             deadline=now() - timedelta(days=1),
#             environment_id=self.environment,
#             table=self.table3
#         )

#         # URL construction
#         self.url = reverse('main:mainpage', kwargs={'user_id': self.user.id})

#     def test_get_tasks_with_environment(self):
#         """
#         Test that get_tasks_with_environment returns correct tasks.
#         """
#         current_datetime = now()
#         tasks = get_tasks_with_environment(self.user.id, current_datetime)

#         self.assertEqual(len(tasks), 2)  # Only two tasks are not completed
#         self.assertEqual(tasks[0]['task'], self.task1)  # Ordered by deadline
#         self.assertEqual(tasks[1]['environment_name'], "Test Environment")


#     def test_get_priority_tasks_with_environment(self):
#         """
#         Test that get_priority_tasks_with_environment returns tasks ordered by priority and deadline.
#         """
#         current_datetime = now()
#         priority_tasks = get_priority_tasks_with_environment(self.user.id, current_datetime)

#         self.assertEqual(len(priority_tasks), 2)
#         self.assertEqual(priority_tasks[0]['task'], self.task1)  # Highest priority
#         self.assertEqual(priority_tasks[1]['priority'], Task.MEDIUM)

#     def test_get_task_counts(self):
#         """
#         Test that get_task_counts correctly aggregates task statuses.
#         """
#         task_counts, total_tasks = get_task_counts(self.user.id)

#         self.assertEqual(task_counts['todo_count'], 1)  
#         self.assertEqual(task_counts['in_progress_count'], 1)  
#         self.assertEqual(task_counts['done_count'], 1)  
#         self.assertEqual(total_tasks, 3)  

#     def test_get_environment_stats(self):
#         """
#         Test that get_environment_stats returns environment statistics correctly.
#         """
#         environment_stats = get_environment_stats(self.user.id)
#         stats = json.loads(environment_stats)

#         self.assertEqual(len(stats), 1)  # One environment
#         self.assertEqual(stats[0]['environment_id__label'], "Test Environment")
#         self.assertEqual(stats[0]['total_tasks'], 3) 
#         self.assertEqual(stats[0]['done_tasks'], 1) 


#     def test_mainpage_redirect_if_user_id_mismatch(self):
#         """
#         Test that a user is redirected to their own main page if the user ID in the URL does not match the session.
#         """
#         session = self.client.session
#         session['user_id'] = self.user.id
#         session.save()

#         mismatched_user_id = self.user.id + 1
#         response = self.client.get(reverse('main:mainpage', kwargs={'user_id': mismatched_user_id}))

#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, f'/main/{self.user.id}/')


