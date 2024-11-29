from django.db import models
from django.contrib.auth.models import User
from users.models import Login

class Environment(models.Model):
    environment_id = models.AutoField(primary_key=True)  # identifier for the environment
    label = models.CharField(max_length=255, unique=True)  # Environment name
    is_private = models.BooleanField(default=True)  # Determines if the environment is shareable
    admin = models.ForeignKey(
        Login,
        related_name='admin_environments',
        on_delete=models.CASCADE
    )  # referencing the User 

class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=255)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='tables')
    user_login = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='user_tables')




    # String representation for easier debugging

    def __str__(self):
        return self.label
