from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    """
    This module defines the configuration for the 'users' app in a Django project.

    It includes:
    - UsersConfig: The app configuration class for the 'users' app.
    - Sets the default auto field for models to 'BigAutoField'.
    - Registers a signal handler to execute the 'create_socialapp_on_migrate' function after database migrations (post_migrate).

    The purpose of the 'ready' method is to ensure that the 'create_socialapp_on_migrate' 
    signal handler is connected when the app is ready, allowing for the
     creation of the social app during the migration process.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import create_socialapp_on_migrate
        post_migrate.connect(create_socialapp_on_migrate, sender=self)
