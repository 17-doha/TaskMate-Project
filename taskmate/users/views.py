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
    '''
    Handles the login process for local users.

    Logic:
    - Retrieves the user's email and password from the POST request.
    - Validates the email and checks if it exists in the database.
    - Compares the provided password with the hashed password stored in the database.
    - Redirects to the main page on success.
    - Displays error messages for incorrect credentials or non-existent users.

    Inputs:
    - request: HttpRequest object containing login credentials.

    Outputs:
    - On successful login: Redirects to the 'main' page.
    - On failure: Renders the login page with error messages.
    '''

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
    Renders the main dashboard page after a successful login.

    Logic:
    - Displays the main page for authenticated users.
    - Redirects here after both local and Google sign-ins.

    Inputs:
    - request: HttpRequest object.

    Outputs:
    - Renders the 'main.html' template.
    """
    return render(request, 'main.html')



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




