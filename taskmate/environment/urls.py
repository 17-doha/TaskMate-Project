from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'environment'  

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:environment_id>/', views.ViewTableTask, name='view_table_task'),
    path('<int:environment_id>/drag-and-drop/', views.dragAndDrop, name='drag-and-drop'),
    path('search_environment/', views.search_environment, name='search_environment'),
    path('show_environments/', views.ShowEnvironments, name='show_environments'),
    path('show_test/', views.show_test, name='show_test'),
]