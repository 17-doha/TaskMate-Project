from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Badge(models.Model):
    badge_name = models.CharField(max_length=255, unique=True) 
    num_of_tasks = models.PositiveIntegerField()
    # icon = models.ImageField(upload_to='badges/icons/')  

    users = models.ManyToManyField(User, related_name='badges', blank=True)

    def __str__(self):
        return self.badge_name