from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, "environment\index.html")    

def dashboard(request):
    environment = "Development"
    return render(request, 'dashboard.html', {'environment': environment})
