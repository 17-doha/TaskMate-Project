from django.urls import path
from users import views

urlpatterns = [

     path('login/', views.login_user, name = 'login'),
     path('main/', views.main, name = 'main'),
     path('accounts/profile/', views.custom_redirect_view), 
     path("", views.home),


]