from django.db import models
from signup.models import User

# Create your models here.
class Badge(models.Model):
    badge_name = models.CharField(max_length=255)
    num_of_tasks = models.IntegerField()
    icon = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.badge_name