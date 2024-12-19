from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Environment, Table, SearchHistory, UserCanAccess
from task.models import Task
import json
from django.contrib.auth.decorators import login_required


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

    Input:
        - HTTP Method: GET
        - Query Parameters: None.

    Output:
        - Renders 'environment/index.html'.
        - Context: Includes a list of all environments.
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
        Displays tasks associated with a specific environment, grouped by their status.

    Input:
        - HTTP Method: GET
        - Path Parameters:
            - environment_id: The ID of the environment.
        - Query Parameters: None.

    Output:
        - Renders 'environment/index.html'.
        - Context:
            - environment: The requested Environment object.
            - todo_tasks: Tasks with a status of 'Pending'.
            - inprogress_tasks: Tasks with a status of 'In Progress'.
            - done_tasks: Tasks with a status of 'Completed'.

    Logic:
        1. Retrieve the specified environment by `environment_id`.
        2. Query for tasks associated with this environment and filter them by status.
        3. Pass the environment and tasks to the template for rendering.
    """
    environment = get_object_or_404(Environment, environment_id=environment_id)
    tasks = Task.objects.filter(environment_id=environment)
    
    # make a list for each type 
    todo_tasks = tasks.filter(status='Pending')
    # print(todo_tasks[0].priority)
    inprogress_tasks = tasks.filter(status='In Progress')
    done_tasks = tasks.filter(status='Completed')

    user_id = request.session.get('user_id')
    environments = Environment.objects.filter(admin_id=user_id)
    print('environments', environments)
    context = {
        "environment": environment,
        "todo_tasks": tasks.filter(status='Pending'),
        "inprogress_tasks": tasks.filter(status='In Progress'),
        "done_tasks": tasks.filter(status='Completed'),
        "environments": environments,
    }
    return render(request, 'environment/index.html', context)


def dragAndDrop(request, environment_id):
    """
    Purpose:
        Handles drag-and-drop actions for moving tasks between tables in the same environment.

    Input:
        - HTTP Method: POST
        - Path Parameters:
            - environment_id: The ID of the environment.
        - JSON Body:
            - task_id: The ID of the task to be moved.
            - target_table: The name of the target table (e.g., 'To Do', 'In Progress', 'Done').

    Output:
        - JSON Response:
            - Success: {'status': 'success', 'message': 'Task moved successfully'}
            - Error: {'status': 'error', 'message': 'Invalid request'}

    Logic:
        1. Parse the request body to get the task ID and target table name.
        2. Retrieve the specified task and its environment.
        3. Retrieve the target table for the task within the same environment.
        4. Update the task's table and status based on the mapping.
        5. Save the updated task and return a success response.
        6. Return an error response for invalid methods or missing data.
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




from .models import SearchHistory, User

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
    return render(request, 'base.html', {'participants': participants})

def save_participant_accessibility(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        changes = data.get('changes', [])

        for change in changes:
            participant_id = change.get('participantId')
            new_access = change.get('newAccess')

            # Find the participant and update their accessibility
            participant = get_object_or_404(UserCanAccess, id=participant_id)
            participant.type_of_accessibility = new_access
            participant.save()

        return JsonResponse({'success': True, 'message': 'Changes saved successfully.'})