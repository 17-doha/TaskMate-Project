from django.urls import path
from .views import create_invitation, share_page

urlpatterns = [
    path('share/', share_page, name='share-page'),
    path('invitation/', create_invitation, name='invitation'),
]
