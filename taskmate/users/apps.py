from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.db.utils import OperationalError
        from allauth.socialaccount.models import SocialApp
        from allauth.socialaccount.providers.google.provider import GoogleProvider
        from django.db.models import ObjectDoesNotExist
        from django.contrib.sites.models import Site

        try:
            # Check if SocialApp for Google exists, and create it if it doesn't
            if not SocialApp.objects.filter(provider=GoogleProvider.id).exists():
                social_app = SocialApp.objects.create(
                    provider=GoogleProvider.id,
                    name="Google App",
                    client_id="438594923509-qoas2ulq9ia9sdvffp0fv9fp1bbu73pe.apps.googleusercontent.com",
                    secret="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",
                    key=""
                )
                social_app.sites.add(1)  # Replace with the correct site ID
        except OperationalError:
            # Handle cases where migrations are not yet applied
            pass
        try:
            site = Site.objects.get(id=1)
        except ObjectDoesNotExist:
            # If no Site exists with ID 1, create one
            Site.objects.create(domain='127.0.0.1:8000', name='127.0.0.1:8000')
