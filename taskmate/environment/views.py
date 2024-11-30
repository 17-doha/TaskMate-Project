from django.shortcuts import render, get_object_or_404
from .models import Environment, Table
from django.http import JsonResponse
from task.models import Task
import json

# used in dragAndDrop function
mapping = {
    'To Do' : 'Pending',
    'In Progress': 'In Progress',
    'Done': 'Completed'
}

def index(request):
    return render(request, "environment/index.html")    


def ViewTableTask(request, environment_id):
    # Retrieve the environment by ID
    """
    A view to render the the tasks for the given environment.
    
    :param request: The request object
    :param environment_id: The ID of the environment to display
    :return: A rendered HTML page with the tasks
    """
    environment = get_object_or_404(Environment, environment_id=environment_id)
    
    # Filter tasks associated with this environment
    tasks = Task.objects.filter(environment_id=environment)
    
    # make a list for each type 
    todo_tasks = tasks.filter(status='Pending')
    inprogress_tasks = tasks.filter(status='In Progress')
    done_tasks = tasks.filter(status='Completed')

       
    # Prepare context for the html
    context = {
        "environment": environment,
        "todo_tasks": todo_tasks,
        "inprogress_tasks": inprogress_tasks,
        "done_tasks": done_tasks,
    }
    
    return render(request, 'environment/index.html', context)


def dragAndDrop(request, environment_id):

    """
    Handle drag and drop of a task to a new table.

    This view expects a POST request with the following JSON data:
        {
            'task_id': <task_id>,
            'target_table': <target_table_name>
        }

    It will update the task's table ID and status in the database.

    Returns a JSON response with a status and message.
    """
    if request.method == "POST":
        # Get JSON data from request body
        data = json.loads(request.body)
        task_id = data.get('task_id')
        target_table_name = data.get('target_table')

        # Get the task object from the database
        task = get_object_or_404(Task, task_id=task_id)

        # Get the environment 
        environment = task.environment_id

        target_table = get_object_or_404(Table, environment=environment, label=target_table_name)

        # Update the task's table ID and status
        task.table = target_table
        task.status = mapping[target_table_name] 
        task.table_id = target_table.table_id
        task.save()

        return JsonResponse({'status': 'success', 'message': 'Task moved successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


 
def search_environment(request):
    """
    Handles search functionality for environments.

    Parameters:
    - request: HttpRequest object that contains metadata about the request. 
      It includes the HTTP method and any data submitted via POST.

    Returns:
    - If the request method is POST:
        - Renders the 'search_environment.html' template with:
          - 'searched': The search term entered by the user.
          - 'environments': Queryset of Environment objects whose 'label' contains the search term.
    - If the request method is not POST:
        - Renders the 'search_environment.html' template with an empty context.
    """
    if request.method == "POST":
        # Get the search term from the POST request
        searched = request.POST['searched']
        # Query the database for environments with labels containing the search term
        environments = Environment.objects.filter(label__contains=searched)
        # Render the template with the search term and the results
        return render(request, 'search_environment.html', {'searched': searched, 'environments': environments})
    else:
        # Render the template without any context if the method is not POST
        return render(request, 'search_environment.html', {})