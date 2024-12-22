from django.db import models
from signup.models import User

# Create your models here.
class Badge(models.Model):
    badge_name = models.CharField(max_length=255)
    num_of_tasks = models.IntegerField()
    icon = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.badge_name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.badge}"