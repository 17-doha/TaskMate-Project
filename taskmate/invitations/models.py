from django.db import models
from django.conf import settings

class Invitation(models.Model):
    PERMISSION_CHOICES = [
        ('view', 'View'),
        ('edit', 'Edit'),
    ]

    email = models.EmailField()
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='view')
    link = models.URLField()
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.permission})"
