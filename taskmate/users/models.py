from django.db import models

class Login(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users_login'  # Make sure this matches your actual table name in the database
#commentfeay7aga