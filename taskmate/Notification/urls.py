from django.urls import path
from .views import fetch_notifications, mark_read

app_name = 'Notification'

urlpatterns = [
    path('fetch_notifications/', fetch_notifications, name='fetch_notifications'),
    path('mark_read/<int:notification_id>/', mark_read, name='mark_read'),
]