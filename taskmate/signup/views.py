from django.shortcuts import render,redirect
from .forms import SignUpForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from signup.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

def home(request):
    return render(request, 'users/base.html')

def signup(request):
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
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        user.save()
        
        return redirect('login')
    
    return render(request, 'signup.html')


    
# Create your views here.
