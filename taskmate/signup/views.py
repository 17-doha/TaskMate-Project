from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from signup.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# View to render the homepage
def home(request):
    """
    Renders the base/homepage of the application.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - Rendered HTML template 'users/base.html'.
    """
    return render(request, 'users/base.html')

# View to handle user signup
def signup(request):
    """
    Handles the user signup process:
    - Validates the input data.
    - Checks for duplicate email registration.
    - Creates and saves a new user in the database.

    Parameters:
    - request: HttpRequest object containing form data submitted via POST.

    Returns:
    - On success: Redirects to the login page with a success message.
    - On failure: Renders the signup page with error messages.
    """
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        
        # Ensure all fields are filled
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        # Create the new user
        user = User.objects.create_user(
            username=email,  # Using email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        # Notify user to verify email
        messages.success(request, "Signup successful! Please Check your email to verify your account.")
        return redirect("login") 

    return render(request, 'signup.html')

# View to activate user account through email
def activate_mail(request, uidb64, token):
    """
    Activates a user account based on email verification.

    Parameters:
    - request: HttpRequest object.
    - uidb64: Base64-encoded user ID.
    - token: Token for email verification.

    Returns:
    - On success: Redirects to login with a success message.
    - On failure: Redirects to signup with an error message.
    """
    try:  
        # Decode user ID and fetch user
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
        if user is not None: 
            user.is_verified = True  # Mark user as verified
            user.save()
            messages.success(request, 'Email confirmation done successfully')
            return redirect('login')
    except User.DoesNotExist: 
        # Handle invalid user cases
        messages.error(request, "Please sign up.") 
        return redirect('signup')

# View to create a new user with hashed password
def create_user(request):
    """
    Handles the creation of a new user:
    - Hashes the provided password.
    - Saves the user to the database.

    Parameters:
    - request: HttpRequest object containing form data submitted via POST.

    Returns:
    - On success: Redirects to login page.
    """
    if request.method == "POST":
        # Extract username and password from form
        username = request.POST['username']
        password = request.POST['password']
        
        # Hash the password before saving
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        user.save()
        
        return redirect('login')
    
    return render(request, 'signup.html')