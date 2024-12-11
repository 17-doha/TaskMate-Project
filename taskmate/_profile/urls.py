from django.urls import path

from . import views

app_name = '_profile'
urlpatterns = [
    # path("", views.profilepage, name="profilepage"), 
     path('', views.profile_view, name='profile_view'), 
    path('edit/', views.profile_edit, name='profile_edit'),
    path('delete/', views.profile_delete, name='profile_delete'),

]