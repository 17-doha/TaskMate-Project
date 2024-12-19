from django.urls import path
from . import views

app_name = "Notification"  # Define the app_name here

urlpatterns = [
    path('fetch-notifications/', views.fetch_notifications, name='fetch_notifications'),
]
