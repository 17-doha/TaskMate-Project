from django.db import models
# Create your models here.
from signup.models import User

class Notification(models.Model):
    NOTIFICATION_STATUS_CHOICES = [
        ('UNREAD', 'Unread'),
        ('READ', 'Read'),
    ]

    notification_id = models.AutoField(primary_key=True)
    content = models.TextField()
    type = models.CharField(max_length=5,null=True)  # Example: "INVITATION"
    status = models.CharField(max_length=10, choices=NOTIFICATION_STATUS_CHOICES, default='UNREAD')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification({self.notification_id}): {self.content[:50]}"