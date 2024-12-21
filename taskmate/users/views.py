from django.shortcuts import render, redirect
from django.contrib import messages
from signup.models import User
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login
from _profile.views import profile_view
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

def login_user(request):
    '''
    Handles the login process for local users.
    Stores the user's ID in the session upon successful login.

    Inputs:
    - request: HttpRequest object containing login credentials.

    Outputs:
    - On successful login: Redirects to the 'main' page.
    - On failure: Renders the login page with error messages.
    '''

    if 'user_id' in request.session:
        return redirect('_profile:profile_view')

    if request.method == 'POST':
        # Get email and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform the exact match query for the email
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            messages.error(request, "Email not correct. Please check your input.")
            return redirect('login')

        # Check if user is verified
        if not user.is_verified:
            messages.error(request, "Your email is not verified. Please check your inbox.")
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)

        # Comparing both hashed passwords
        if check_password(password, user.password):
            # Save the user's ID in the session
            request.session['user_id'] = user.id

            # Optional: Save additional user data if needed
            request.session['user_email'] = user.email

            print(user.id, "in the login")
            return redirect('main')  # Redirect to the main page
        else:
            messages.error(request, "Incorrect password. Please try again.")

    return render(request, 'authentication/login.html')


def main(request):
    """
    Renders the main dashboard page after a successful login.
    
    Logic:
    - Displays the main page for authenticated users.
    - Redirects here after both local and Google sign-ins.
    
    Inputs:
    - request: HttpRequest object.
    
    Outputs:
    - Renders the 'main.html' template or redirects to 'main/user_id' if user_id is in the session.
    """
    
    # Check if 'user_id' is stored in session
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        # Redirect to 'main/user_id' if user_id exists in session
        return redirect(f'/main/{user_id}/')
    
    # If no user_id in session, just render the main page
    return render(request, 'main.html')


# Get the custom User model
User = get_user_model()

def google_sign_in_callback(request):
    """
    Handles Google OAuth sign-in and user registration if not already registered.

    Logic:
    - Verifies the user's authentication status.
    - Retrieves Google account information from the SocialAccount model.
    - Checks if a user with the associated email exists in the custom User model.
    - If the user doesn't exist, creates a new user without a password (Google sign-in only).
    - Redirects authenticated users to the 'main' page.

    Inputs:
    - request: HttpRequest object.

    Outputs:
    - On success: Redirects to the 'main' page.
    - On failure: Redirects to the 'login' page.
    """

    if request.user.is_authenticated:
        # Check if user has a linked Google account
        social_account = SocialAccount.objects.filter(user=request.user, provider="google").first()

        if social_account:
            email = social_account.extra_data.get("email")

            try:
                # Check if the user already exists
                user = User.objects.get(email=email)
                print("User already exists")
            except User.DoesNotExist:
                # Create a new user if it doesn't exist
                user = User.objects.create(
                    email=email,
                    username=request.user.username,
                    password="",  # Leave password empty as this is Google sign-in
                )
                print("New user created")

            # Save the user ID to the session
            request.session["user_id"] = user.id
            user_id = user.id  # Set user_id for redirect

            return redirect(f"/main/{user_id}/")

    # If not authenticated, redirect to the login page
    return redirect("login")



def logout_user(request):
    """
    Logs out the currently authenticated user and redirects to the login page.
    """
    logout(request)  
    return redirect('login') 


def activate_user(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect('signup')

