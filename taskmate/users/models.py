# from django.contrib.auth.models import AbstractUser
# from django.db import models


# class Login(AbstractUser):
#     # Override or extend default fields
#     email = models.EmailField(unique=True)  # Ensures unique email for each user
#     age = models.IntegerField(null=True, blank=True)
#     phone_num = models.CharField(max_length=15, null=True, blank=True)
#     theme_is_light = models.BooleanField(default=True)
#     badge_name = models.CharField(max_length=255, null=True, blank=True)
#     password = models.CharField(max_length=128, verbose_name='password')
#     # Customize username and authentication fields
#     username = models.CharField(max_length=255, null=True, blank=True)
#     USERNAME_FIELD = 'email'  # Use email instead of username for login
#     REQUIRED_FIELDS = ['username']  # Add fields you want to require when creating a superuser

#     class Meta:
#         db_table = 'users_login'  # Specify custom table name
