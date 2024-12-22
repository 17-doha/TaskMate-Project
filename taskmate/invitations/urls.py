from django.urls import path
from . import views

app_name = 'invitation'

urlpatterns = [
    path('invite/', views.invite_participants, name='invite_participants'),
    path('<int:environment_id>/send-invitation/', views.send_invitation, name='send_invitation'),
]
