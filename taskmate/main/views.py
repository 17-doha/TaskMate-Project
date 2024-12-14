from django.shortcuts import render


def mainpage(request, user_id):
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
    return render(request, 'mainpage.html')
# Create your views here.
