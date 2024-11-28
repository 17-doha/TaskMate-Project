from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import Login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def login_user(request):
    if request.method == 'POST':
        # Get email and password from the POST request
        email = request.POST.get('email')
        password = request.POST.get('password')


        # Perform the exact match query for the email
        try:
            user = Login.objects.get(email=email)

            # Compare the password (assuming plain-text comparison)
            if password == user.password:
                return redirect('main')
            elif password != user.password:
                messages.error(request, "Incorrect password. Please try again.")
        
        except Login.DoesNotExist:
            messages.error(request, "Email not correct. Please check your input.")

    return render(request, 'authentication/login.html')





def main(request):
    # This is the page to redirect to after login
    return render(request, 'main.html')



def home(request):
    return render(request, 'main.html')





