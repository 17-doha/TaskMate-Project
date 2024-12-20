from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Environment, Table, SearchHistory, UserCanAccess
from task.models import Task
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import Http404
from .models import SearchHistory, User
from django.template.loader import render_to_string

from signup.models import User


# Mapping for drag-and-drop functionality
mapping = {
    'To Do': 'Pending',
    'In Progress': 'In Progress',
    'Done': 'Completed'
}


def index(request, id = None):
    # user_id = request.session.get('user_id') "Hash this to access the user_id in any other view"
    """
    Purpose:
        Renders the homepage for the environment application.
        If an `id` is provided, it will display a specific environment;
        otherwise, it will show all environments for the current user.

    Input:
        - HTTP Method: GET
        - Path Parameter: 
            - id: Optional, an environment ID to display a specific environment.

    Output:
        - Renders 'environment/index.html' template.
        - Context:
            - If `id` is provided: A single environment object.
            - If `id` is not provided: A list of all environments belonging to the current user.

    Logic:
        1. If an `id` is provided, render the page with that specific environment ID.
        2. If no `id` is provided, fetch all environments associated with the logged-in user using their `user_id`.
        3. Render the `index.html` page with either the selected environment or a list of environments.
    """
    if id is not None:
        return render(request, "environment/index.html", {"environment_id": id})
    else:
        user_id = request.session.get('user_id')
        environments = Environment.objects.filter(admin_id=user_id)
        return render(request, "environment/index.html", {"environments": environments})








def ViewTableTask(request, environment_id):
    """
    Purpose:
        Displays tasks associated with a specific environment, grouped by their status
        (Pending, In Progress, Completed).

    Input:
        - HTTP Method: GET
        - Path Parameter:
            - environment_id: The ID of the environment to filter tasks by.
        - Query Parameters: None.

    Output:
        - Renders 'environment/index.html' with tasks grouped by their status.
        - Redirects to the new environment if necessary.
    """
    user_id = request.session.get('user_id')
    # Ensure the user is logged in
    if user_id == "None":
        raise Http404("User is not authenticated.")
    
    # Try to retrieve the environment
    try:
        environment = Environment.objects.get(environment_id=environment_id, admin=user_id)
    except Environment.DoesNotExist:
        # If the environment is not found or doesn't belong to the logged-in user, get the first environment that belongs to the user
        environment = Environment.objects.filter(admin=user_id).first()

        if environment is None:
            raise Http404("No environment found for this user.")
        
        # Redirect to the new environment's page
        return redirect('environment:view_table_task', environment_id=environment.environment_id)

    # Now that we have the correct environment, fetch the tasks for it
    tasks = Task.objects.filter(environment_id=environment.environment_id)  # Change environment to environment_id

    environment = get_object_or_404(Environment, environment_id=environment_id)
    tasks = Task.objects.filter(environment_id=environment)
    
    # Group tasks by their status
    # make a list for each task type 
    todo_tasks = tasks.filter(status='Pending')
    inprogress_tasks = tasks.filter(status='In Progress')
    done_tasks = tasks.filter(status='Completed')

    user_id = request.session.get('user_id')
    environments = Environment.objects.filter(admin_id=user_id)
    
    context = {
        "environment": environment,
        "todo_tasks": todo_tasks,
        "inprogress_tasks": inprogress_tasks,
        "done_tasks": done_tasks,
        "environments": environments,

    }
    
    return render(request, 'environment/index.html', context)



def dragAndDrop(request, environment_id):
    """
    Purpose:
        Handles drag-and-drop actions for moving tasks between tables in the same environment.

    Input:
        - HTTP Method: POST
        - Path Parameter:
            - environment_id: The ID of the environment to move tasks within.
        - JSON Body:
            - task_id: The ID of the task to be moved.
            - target_table: The name of the target table (e.g., 'To Do', 'In Progress', 'Done').

    Output:
        - JSON Response:
            - Success: {'status': 'success', 'message': 'Task moved successfully'}
            - Error: {'status': 'error', 'message': 'Invalid request.'}

    Logic:
        1. Parse the request body to get the task ID and target table name.
        2. Retrieve the task using its ID.
        3. Get the target table and update the task's table and status based on the mapping.
        4. Save the task and return a success response.
        5. Return an error response for invalid methods or missing data.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get('task_id')
        target_table_name = data.get('target_table')

        task = get_object_or_404(Task, task_id=task_id)
        environment = task.environment_id
        target_table = get_object_or_404(Table, environment=environment, label=target_table_name)

        task.table = target_table
        task.status = mapping[target_table_name]
        task.table_id = target_table.table_id
        task.save()

        return JsonResponse({'status': 'success', 'message': 'Task moved successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})






def search_environment(request):
    """
    Purpose:
        Implements search functionality to find environments by their label and store the search term in the search history.

    Input:
        - HTTP Method: POST
        - Form Data:
            - searched: The search term entered by the user.

    Output:
        - Renders 'search_environment.html'.
        - Context (for POST requests):
            - searched: The search term.
            - environments: Queryset of Environment objects matching the search term.
        - Context (for non-POST requests):
            - Empty.

    Logic:
        1. If the request method is POST:
            - Retrieve the search term from the form.
            - Query the database for environments whose labels contain the search term.
            - Add the search term to the SearchHistory table.
            - Pass the search results to the template.
        2. If the request method is not POST:
            - Render the template with an empty context.
    """
    user_id = request.session.get('user_id')
    if request.method == "POST":

        # Retrieve the search term
        searched = request.POST['searched']
        
        # Query environments based on the search term
        environments = Environment.objects.filter(label__contains=searched, admin_id=user_id)
        
        # Retrieve the User instance based on the user_id
        user = User.objects.get(id=user_id)

        # Store the search term in SearchHistory if it's not already there
        if not SearchHistory.objects.filter(content=searched, user_id=user).exists():
            SearchHistory.objects.create(content=searched, user_id=user)
        
        return render(request, 'search_environment.html', {'searched': searched, 'environments': environments})
    else:
        return render(request, 'search_environment.html', {})   


@login_required   #Not ready yet
def add_environment(request):
    if request.method == "POST":
        label = request.POST['label']
        is_private = 'is_private' in request.POST
        environment = Environment.objects.create(
            label=label,
            is_private=is_private,
            admin=request.user
        )
    return render(request, 'base.html', {'environment': environment})




def ShowParticipants(request, environment_id):
    """
    Purpose:
        Displays the list of participants who have access to the environment.

    Input:
        - HTTP Method: GET
        - Path Parameter:
            - environment_id: The ID of the environment whose participants to display.

    Output:
        - JSON Response:
            - Success: A JSON containing dynamically generated HTML for participants.
            - Error: If the request was not an AJAX request, returns the full page.

    Logic:
        1. Retrieve the environment and its participants from the UserCanAccess table.
        2. If the request is AJAX, return the participants as HTML.
        3. Otherwise, render the full page with the participants.
    """
    environment = get_object_or_404(Environment, environment_id=environment_id)
    participants = UserCanAccess.objects.filter(environment=environment)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Create the participant HTML dynamically
        participants_html = ''
        for participant in participants:
            participants_html += f'''
                <div class="participant-item" data-participant-id="{participant.id}">
                    <p>{participant.user.username} 
                        <select class="form-select accessibility-select">
                            <option value="read" {'selected' if participant.type_of_accessibility == 'Participant' else ''}>Participant</option>
                            <option value="write" {'selected' if participant.type_of_accessibility == 'subadmin' else ''}>subadmin</option>
                            <option value="admin" {'selected' if participant.type_of_accessibility == 'Admin' else ''}>Admin</option>
                        </select>
                    </p>
                </div>
            '''

        # if no participants
        if not participants.exists():
            participants_html = "<p>There are no participants.</p>"

        return JsonResponse({'html': participants_html})

    # For full-page render (fallback)
    return render(request, 'base.html', {'participants_html': participants_html})




def guest_environment_view(request, environment_id):
    environment = get_object_or_404(Environment, environment_id=environment_id)

    user_id = request.session.get('user_id')
    if user_id is None:
       

        # Render the environment for guests
        tasks = Task.objects.filter(environment_id=environment.environment_id)

        context = {
            "environment": environment,
            "tasks": tasks,
            "todo_tasks": tasks.filter(status='Pending'),
            "inprogress_tasks": tasks.filter(status='In Progress'),
            "done_tasks": tasks.filter(status='Completed'),
        }
        return render(request, "environment/guest_view.html", context)


    return render(request, 'base.html', {'participants': participants})


def save_participant_accessibility(request):  # Not ready yet
    """
    Purpose:
        Updates the accessibility type of participants in the environment.

    Input:
        - HTTP Method: POST
        - JSON Body:
            - changes: A list of changes made to participant accessibilities.
            - Each change includes participantId and newAccess.

    Output:
        - JSON Response:
            - Success: {'success': True, 'message': 'Changes saved successfully.'}
            - Error: {'success': False, 'message': 'Failed to save changes.'}

    Logic:
        1. Parse the changes from the request body.
        2. For each change, update the participant's accessibility.
        3. Return a success response after all changes are saved.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        changes = data.get('changes', [])
        for change in changes:
            participant_id = change.get('participantId')
            new_access = change.get('newAccess')

            participant = get_object_or_404(UserCanAccess, id=participant_id)
            participant.type_of_accessibility = new_access
            participant.save()

        return JsonResponse({'success': True, 'message': 'Changes saved successfully.'})

    return JsonResponse({'success': False, 'message': 'Failed to save changes.'})




def add_environment(request):
    if request.method == 'POST':
        label = request.POST.get('label', '').strip()

        if not label:
            return JsonResponse({'success': False, 'error': 'Environment label is required.'}, status=400)

        if Environment.objects.filter(label=label).exists():
            return JsonResponse({'success': False, 'error': 'An environment with this label already exists.'}, status=400)

        try:
            # Create the environment
            environment = Environment.objects.create(
                label=label,
                is_private=True,
                admin=request.user
            )
            statuses = ['To Do', 'Done', 'In Progress']
            for status in statuses:
                Table.objects.create(
                    environment=environment,
                    label=status
                )
            return JsonResponse({'success': True, 'message': f"Environment '{label}' added successfully."})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)
