from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from task.models import Task 
from Notification.models import Notification
from signup.models import User

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        today = timezone.now().date()  #today's date
        next_day = today + timedelta(days=1)  # Tomorrow's date
        print(next_day)
    # b filter data in the database
        tasks = Task.objects.filter(deadline__date=next_day)

        print(tasks)
        for task in tasks:
            if task.assigned_to:  # Ensure the task has an assigned user
                subject = "Task Deadline Reminder"
                message = f"""
                Dear {task.assigned_to.username},
                
                This is a friendly reminder that the task '{task.content}' is due on {task.deadline.strftime('%Y-%m-%d')}.

                Please make sure to complete it before the deadline.

                Best regards,
                TaskMate Team
                """
                user_object = User.objects.get(username=task.assigned_to.username)
                Notification.objects.create(
                    content=f"{task.assigned_to.username}, This is reminder for {task.content} task",
                    receiver=user_object,
                    status="UNREAD"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email="noreply@taskmate.com",
                    recipient_list=[task.assigned_to.email],
                    fail_silently=False,
                )
                print(f"Reminder sent to {task.assigned_to.email} for task: {task.content}")

        print("Deadline reminders completed successfully.")