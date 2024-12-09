from django.urls import path
from . import views

urlpatterns = [
    path('google-sign-in-callback/', views.google_sign_in_callback, name='google_sign_in_callback'),
    path('login/', views.login_user, name='login'),
    path('main/', views.main, name='main'),
    path("", views.main, name='home'),
    path('profile/', views.Profile, name='Profile'),
    path('logout/', views.logout_user, name='logout'),
]
