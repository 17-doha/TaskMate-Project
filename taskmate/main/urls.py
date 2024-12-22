from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'main'  

urlpatterns = [
    path('<int:user_id>/', views.mainpage, name='mainpage'),
    
    
]