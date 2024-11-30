from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from signup.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def home(request):
    """
    Render the home page.

    This view renders the base.html template as the home page.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered template.
    """
    return render(request, 'users/base.html')

def signup(request):
    """
    Handle user signup.

    This view handles the GET and POST requests to the signup page. If the request is a GET request, it renders the signup.html template. If the request is a POST request, it validates the input, creates the user, and logs the user in.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered template or a redirect to the login page.
    """
    if request.method == 'POST':
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        
        if not all([first_name, last_name, email, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=email,  # You can use email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        #log the user in
        messages.success(request, "Signup successful! Please Check your email to verify your account")
        return redirect("login") 

    return render(request, 'signup.html')

def activate_mail(request, uidb64, token):
    """
    Activate a user's email address.

    This view is used to activate a user's email address. It takes a uidb64 and a token as parameters, decodes the uidb64 to a user id, and checks if the corresponding user exists in the database. If the user exists, it sets the user's is_verified attribute to True and saves the user. If the user does not exist, it displays an error message and redirects the user to the signup page.

    Parameters:
        request (HttpRequest): The request object.
        uidb64 (str): The base64 encoded user id.
        token (str): The token used to verify the user.

    Returns:
        HttpResponse: A redirect to the login page if the user exists and the email is verified, a redirect to the signup page if the user does not exist.
    """
    
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(id=uid)  
        if user is not None: 
            user.is_verified = True  
            user.save() 
            messages.success(request, 'Email confirmation done successfully')
            return redirect('login')
    except User.DoesNotExist: 
         messages.error(request,"Please sign up") 
         return redirect('signup')


def create_user(request):
    """
    Creates a new user given a username and password.

    This view is used to create a new user given a username and password. It takes a POST request with the username and password, hashes the password, and creates a new user in the database. If the user is created successfully, it redirects the user to the login page.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A redirect to the login page if the user is created successfully, a redirect to the signup page if the user is not created successfully.
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        user.save()
        
        return redirect('login')
    
    return render(request, 'signup.html')
