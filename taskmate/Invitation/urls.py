from django.urls import path
from . import views

urlpatterns = [
    path('create_invitation/', views.create_invitation, name='create_invitation'),
]
