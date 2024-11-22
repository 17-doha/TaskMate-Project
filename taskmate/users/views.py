from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import Login



def login_user(request):
    # Get email and password from the POST request
    email = request.POST.get('email')  # Strip spaces from email
    password = request.POST.get('password')

    print(f"Email from form: {email}")  # Debugging line

    # Perform the exact match query for the email (case-sensitive)
    try:
        user = Login.objects.get(email=email)  # This ensures exact match for email
        print(f"User found: {user.email}")  # Debugging line
        
        # Directly compare the password (since we're not hashing)
        if password == user.password:  # Compare plain-text passwords
            print("Validated")
            messages.success(request, "Successfully logged in")
            return redirect('main')  # Redirect to main page
        else:
            print("Not validated - Incorrect password")
            messages.error(request, "Incorrect password")
    
    except Login.DoesNotExist:
        print(f"Email {email} not found")
        messages.error(request, "Email not found")

    return render(request, 'authentication/home.html')






def main(request):
    # This is the page to redirect to after login
    return render(request, 'main.html')



def home(request):
    return render(request, 'home2.html')


def logout_view(request):
    logout(request)
    return redirect('/')