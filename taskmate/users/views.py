from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from .models import Login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher

# The password to hash




def login_user(request):
    """
    Handles local sign-in and ensures the user exists.
    """

    if request.method == 'POST':
        # Get email and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')


        # Perform the exact match query for the email
        try:
            user = Login.objects.get(email=email)

            #Comparing both hashed passwords
            if  check_password(password, user.password):
                return redirect('main')
            else:
                messages.error(request, "Incorrect password. Please try again.")
        
        except Login.DoesNotExist:
            messages.error(request, "Email not correct. Please check your input.")

    return render(request, 'authentication/login.html')



@login_required
def custom_redirect_view(request):
    return redirect('/main/')  # Redirect to your desired path

def main(request):
    # This is the page to redirect to after login
    return render(request, 'main.html')



def google_sign_in_callback(request):
    """
    Handles Google sign-in and ensures the user exists and if not will create one.
    """
    if request.user.is_authenticated:
        # Check if user exists in the custom Login model
        social_account = SocialAccount.objects.filter(user=request.user, provider="google").first()
        
        if social_account:
            email = social_account.extra_data.get("email")

            try:
                Login.objects.get(email=email)
            except Login.DoesNotExist:
                Login.objects.create(
                    email=email,
                    username=request.user.username,
                    password="",  # Leave password empty as this is Google sign-in
                )

        return redirect("main")

    return redirect("login")





