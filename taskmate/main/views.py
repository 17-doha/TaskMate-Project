from django.shortcuts import render
from django.utils.timezone import now  # For getting the current date and time
from django.db.models import Q
from task.models import Task  # Import your Table model


def mainpage(request, user_id):
    # user_id = request.session.get('user_id') #"Hash this to access the user_id in any other view"
    # This is the page to redirect to after login
    """
    Renders the main dashboard page after a successful login.

    Logic:
    - Displays the main page for authenticated users.
    - Redirects here after both local and Google sign-ins.

    Inputs:
    - request: HttpRequest object.

    Outputs:
    - Renders the 'mainpage.html' template.
    """
    current_datetime = now()

    # Fetch tasks for the user with future deadlines, ordered by the nearest deadline first
    tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),
        deadline__gt=current_datetime
    ).order_by('deadline')[:4]
    # Pass tasks to the template
    return render(request, 'mainpage.html', {'tasks': tasks})

# Create your views here.
