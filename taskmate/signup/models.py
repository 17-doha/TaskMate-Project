from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string

class User(AbstractUser):
    """
    Extends the default Django user model with additional fields.

    Attributes:
        phone_number (str): An optional field for storing the user's phone number,
                            with a maximum length of 30 characters.
        is_verified (bool): A boolean field indicating whether the user's account
                            is verified. Defaults to False.
    """
    phone_number = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)
    age = models.IntegerField(null=True, blank=True)
    phone_num = models.CharField(max_length=15, null=True, blank=True)
    theme_is_light = models.BooleanField(default=True)
    badge_name = models.CharField(max_length=255, null=True, blank=True)

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Sends an account activation email to a newly created user.

    This function is triggered after a new user instance is saved. It generates
    a unique token and user ID, constructs an HTML email message, and sends it
    to the user's email address for account verification.

    Args:
        sender (Model): The model class that sent the signal.
        instance (User): The instance of the user model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments.

    Raises:
        BadHeaderError: If there is an issue with the email header.
    """
    if created:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        subject = "TaskMate Account Verification"
        html_message = f"""
        <p>Hi {instance.first_name},</p>
        <p>Please confirm your email address by clicking the link below:</p>
        <a href="http://127.0.0.1:8000/activate/{uid}/{token}style="color:white; text-decoration: none;border-radius: 25px; background-color: #8661ff; padding: 7px 25px;"> <strong>Verify Email<strong></a>
        <p>Thank you!</p>
        """
        try:
            send_mail(
                subject,
                '',
                settings.EMAIL_HOST_USER,  # Use sender email from settings
                [instance.email],
                fail_silently=False,
                html_message=html_message
            )
        except BadHeaderError:
            pass