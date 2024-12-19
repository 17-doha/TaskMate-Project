from django.db import models
from signup.models import User

class Environment(models.Model):
    environment_id = models.AutoField(primary_key=True) 
    label = models.CharField(max_length=255, unique=True)  
    is_private = models.BooleanField(default=True)  
    admin = models.ForeignKey(
        User,
        related_name='admin_environments',
        on_delete=models.CASCADE
    )  # referencing the User 

    class Meta:
        db_table = 'environment'  

    def __str__(self):
        return self.label 


class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='tables')

    
    class Meta:
        db_table = 'table'  



class UserCanAccess(models.Model):
    ACCESSIBILITY_CHOICES = [
        ('Participant', 'Participant'),
        ('subadmin', 'subadmin'),
        ('Admin', 'Admin')
    ]
    
    INVITATION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]
    
    type_of_accessibility = models.CharField(max_length=20, choices=ACCESSIBILITY_CHOICES)
    invitation_status = models.CharField(max_length=20, choices=INVITATION_STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(User, related_name='user_access', on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, related_name='user_accesses', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_can_access'
        unique_together = ('user', 'environment')  # Ensures no duplicate entries for the same user and environment
    def grant_access(self):
        self.type_of_accessibility = 'Participant'
        self.save()

    def revoke_access(self):
        self.type_of_accessibility = 'Revoked'
        self.save()

    def check_access(self):
        return self.type_of_accessibility in ['Participant', 'subadmin', 'Admin']

    def update_invitation_status(self, status):
        if status in dict(self.INVITATION_STATUS_CHOICES):
            self.invitation_status = status
            self.save()