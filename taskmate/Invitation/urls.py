from django.urls import path
from . import views

app_name = 'Invitation'  # Define the app namespace

urlpatterns = [
    path('create_invitation/', views.create_invitation, name='create_invitation'),
]
