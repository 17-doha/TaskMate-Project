from django.db import models
from django.contrib.auth.models import User

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
    
    task_id = models.AutoField(primary_key=True)
    content = models.TextField()  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    deadline = models.DateTimeField()  
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM)
    # table = models.ForeignKey(Table, on_delete=models.CASCADE)  
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assigned = models.ForeignKey(User, related_name='assigned_tasks', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content

