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


class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='tables')
    user_login = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tables')
    
    class Meta:
        db_table = 'table'  
