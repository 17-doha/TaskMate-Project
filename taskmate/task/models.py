from django.db import models
from django.contrib.auth.models import User
from users.models import Login
from environment.models import Environment
from environment.models import Table
import datetime
class Task(models.Model):
    # Constants for task status and priority
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    
    PRIORITY_CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    ]
    
    # SQL table content
    task_id = models.AutoField(primary_key=True)
    content = models.TextField()  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    start_date = models.DateTimeField(default=datetime.date.today)  
    deadline = models.DateTimeField()  
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=1)   # refrence Table when created un hash
    created_by = models.ForeignKey(Login, related_name='created_tasks', on_delete=models.CASCADE) # refrence User
    assigned_to = models.ForeignKey(Login, related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True) # refrence User
    environment_id = models.ForeignKey(Environment, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True) # refrence Environment

    # return str of content of table
    def __str__(self):
        return self.content
        
    class Meta:
        ordering = ['priority', 'deadline']

