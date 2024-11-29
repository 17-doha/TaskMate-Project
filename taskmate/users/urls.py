from django.urls import path
from . import views

urlpatterns = [

     path('login/', views.login_user, name = 'login'),
     path('main/', views.main, name = 'main'),
     path("", views.main),

]