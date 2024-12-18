from django.urls import path
from .views import create_invitation

urlpatterns = [
    path('invitation/', create_invitation, name='invitation'),
]
