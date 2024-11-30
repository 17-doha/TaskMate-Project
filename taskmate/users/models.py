from django.db import models

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128) 
    age = models.IntegerField(null=True, blank=True) 
    name = models.CharField(max_length=255, null=True, blank=True)  
    phone_num = models.CharField(max_length=15, null=True, blank=True)  
    theme_is_light = models.BooleanField(default=True)  
    badge_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'users_login'  