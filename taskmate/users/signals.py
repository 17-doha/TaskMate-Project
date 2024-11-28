from django.db import OperationalError
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider


def create_socialapp_on_migrate(sender, **kwargs):
    try:
        site, _ = Site.objects.get_or_create(
            id=1, defaults={"domain": "127.0.0.1:8000", "name": "127.0.0.1:8000"}
        )

        if not SocialApp.objects.filter(provider=GoogleProvider.id).exists():
            social_app = SocialApp.objects.create(
                provider=GoogleProvider.id,
                name="Google App",
                client_id="438594923509-qoas2ulq9ia9sdvffp0fv9fp1bbu73pe.apps.googleusercontent.com",
                secret="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",
                key=""
            )
            social_app.sites.add(site)

    except OperationalError:
        pass 
