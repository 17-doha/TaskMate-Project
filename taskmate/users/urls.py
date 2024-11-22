from django.urls import path
from . import views

urlpatterns = [

     path('login/', views.login_user, name = 'login'),
     path('main/', views.main, name = 'main'),
     path("", views.home),
     path("logout", views.logout_view)

]