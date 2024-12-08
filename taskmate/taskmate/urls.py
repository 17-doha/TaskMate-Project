"""
URL configuration for taskmate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from users import views
from signup.views import signup, activate_mail
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_user, name='login'),
    path('login/', include('django.contrib.auth.urls')),
    path('main/', views.main, name='main'),
    path('accounts/', include('allauth.urls')),
    path("", include("users.urls")),
    # redirection to environment app urls
    path("environment/", include("environment.urls")),
    path("task/", include("task.urls")),



    #Signup urls
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', activate_mail, name = "activate"),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html',
         success_url=reverse_lazy('login')
         ), 
        name='password_reset_confirm'),


    # profile urls
    path("profile/", include("_profile.urls")),

]
