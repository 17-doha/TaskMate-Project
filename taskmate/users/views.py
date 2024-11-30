from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from signup.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher

# The password to hash




def login_user(request):
    """
    Handles local sign-in and ensures the user exists.
    Uses the Local user from the User model (User model is a custom model for custom users)
    """

    if request.method == 'POST':
        # Get email and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')


        # Perform the exact match query for the email
        try:
            user = User.objects.get(email=email)

            #Comparing both hashed passwords
            if  check_password(password, user.password):
                return redirect('main')
            else:
                messages.error(request, "Incorrect password. Please try again.")
        
        except User.DoesNotExist:
            messages.error(request, "Email not correct. Please check your input.")

    return render(request, 'authentication/login.html')



def main(request):
    # This is the page to redirect to after login
    """
    The main page that users are redirected to after logging in.
    """
    return render(request, 'main.html')



def google_sign_in_callback(request):
    """
    Handles Google sign-in and ensures the user exists and if not will create one.
    Redirects to main after sign-in
    """

    if request.user.is_authenticated:
        # Check if user exists in the custom User model
        social_account = SocialAccount.objects.filter(user=request.user, provider="google").first()
       
        
        if social_account:
            email = social_account.extra_data.get("email")

            try:
                User.objects.get(email=email)
                print("User already exists")
            except User.DoesNotExist:
                User.objects.create(
                    email=email,
                    username=request.user.username,
                    password="",  # Leave password empty as this is Google sign-in
                )

        return redirect("main")

    return redirect("login")





