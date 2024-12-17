from django.urls import path
<<<<<<< HEAD
from .views import create_invitation, share_page

urlpatterns = [
    path('share/', share_page, name='share-page'),
=======
from .views import create_invitation

urlpatterns = [
>>>>>>> LastMerge
    path('invitation/', create_invitation, name='invitation'),
]
