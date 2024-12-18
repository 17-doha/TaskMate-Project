from django.db import models

# Create your models here.

from signup.models import User
from environment.models import Environment

class Invitation(models.Model):
    INVITATION_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    invitation_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitation')
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE,null=True)
    invitation_status = models.CharField(max_length=10,choices=INVITATION_STATUS_CHOICES,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation({self.sender} → {self.receiver})"