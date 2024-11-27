from django.db import models
from django.contrib.auth.models import User


class Environment(models.Model):
    environment_id = models.AutoField(primary_key=True)  # identifier for the environment
    label = models.CharField(max_length=255, unique=True)  # Environment name
    is_private = models.BooleanField(default=True)  # Determines if the environment is shareable
    admin = models.ForeignKey(
        User,
        related_name='admin_environments',
        on_delete=models.CASCADE
    )  # referencing the User 

    # String representation for easier debugging
    def __str__(self):
        return self.label
