from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment, User
from environment.models import SearchHistory
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
from environment.models import Environment
from django.contrib import messages
from environment.models import Table, UserCanAccess
from django.db.models import Q
from environment.models import Table
from environment.models import UserCanAccess



user_id = 1

# A view to show all tasks with the edit and delete buttons for testing

def ViewAllTasks(request):
    """
    Purpose:
    - Display all tasks with edit and delete options for testing.

    Logic:
    - Fetches all Task objects.
    - Passes the tasks to the template.

    Input:
    - request: HttpRequest object.

    Output:
    - Renders 'task/view_all.html' with:
      - 'tasks': Queryset of all Task objects.
    """
    queryset = Task.objects.all()
    print(len(queryset))
    context={
        "tasks": queryset,
    }
    return render(request,'task/view_all.html',context)


# A view to allow editing a task on another page
def EditTask(request, id):
    """
    Purpose:
    - Allow editing of a specific task.

    Logic:
    - Fetches the task by ID.
    - If POST, updates the task with form data and saves.
    - If not POST, pre-fills the form with the task data.

    Input:
    - request: HttpRequest object.
    - id: ID of the Task to edit.

    Output:
    - If POST:
      - Redirects to 'view_all_tasks'.
    - Else:
      - Renders 'task/edit_task.html' with:
        - 'form': Pre-filled TaskEditForm.
        - 'task': Task object.
    """
    task = get_object_or_404(Task, task_id=id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            env_id = task.environment_id_id
            return  redirect(f'/environment/{env_id}/')
    else:
        form = TaskEditForm(instance=task)

    users = User.objects.filter(
        user_access__environment_id=task.environment_id,  
        user_access__type_of_accessibility__in=['subadmin', 'Admin'],  
        user_access__invitation_status='Accepted'  
        )
    return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


# A view to delete tasks on click
def DeleteTask(request, id):
    """
    Purpose:
    - Delete a specific task.

    Logic:
    - Fetches the task by ID and deletes it.

    Input:
    - request: HttpRequest object.
    - id: ID of the Task to delete.

    Output:
    - Redirects to 'view_all_tasks'.
    """
    task = get_object_or_404(Task, task_id=id)
    env_id = task.environment_id_id
    task.delete()
    return  redirect(f'/environment/{env_id}/')


# A view to create a new task
def CreateTask(request,env_id):
    """
    Purpose:
    - Create a new  task.

    Logic:
    - If POST, validates form data and creates a task with default user and environment.
    - If not POST, displays a blank form for task creation.

    Input:
    - request: HttpRequest object.

    Output:
    - If POST and valid:
      - Redirects to 'environment:index' with a success message.
    - Else:
      - Renders 'task/create_task.html' with:
      - 'users': Queryset of all User objects.
    """
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = User.objects.get(id=user_id)  # Default user for now
            task.environment_id = Environment.objects.get(environment_id=env_id)  
            table = get_object_or_404(Table, environment_id=env_id, label="To Do")
            task.table = table

            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect(f'/environment/{env_id}/')
        else:
            messages.error(request, 'There was an error creating the task. Please try again.')

    # Get all users to choose from 
    users = User.objects.filter(
        user_access__environment_id=Environment.objects.get(environment_id=env_id)  ,  
        user_access__type_of_accessibility__in=['subadmin', 'Admin'],  
        user_access__invitation_status='Accepted'  
    )

    return render(request, 'task/create_task.html', {
        'users': users,
        'environment_id': env_id,
    })


def search_task(request):
    """
    Purpose:
    - Search for tasks based on content and store the search term in the search history.

    Logic:
    - If POST, filters Task objects matching the search term.
    - If not POST, renders a blank search form.

    Input:
    - request: HttpRequest object.

    Output:
    - If POST:
      - Renders 'search_environment.html' with:
        - 'searched': Search term.
        - 'tasks': Matching Task objects.
    - Else:
      - Renders 'search_environment.html' with no context.
    """
    user_id = request.session.get('user_id')
    if request.method == "POST":
        # Logs
        print("user_id", user_id)

        # Retrieve the search term
        searched = request.POST['searched']
        
        # Query tasks based on the search term and user ID
        tasks = Task.objects.filter(
            Q(content__contains=searched, created_by_id=user_id) | Q(content__contains=searched, assigned_to_id=user_id)
        )
        
        # Retrieve the User instance based on the user_id
        user = User.objects.get(id=user_id)

        # Store the search term in SearchHistory if it's not already there
        if not SearchHistory.objects.filter(content=searched, user_id=user).exists():
            SearchHistory.objects.create(content=searched, user_id=user)
        
        return render(request, 'search_environment.html', {'searched': searched, 'tasks': tasks})
    else:
        return render(request, 'search_environment.html', {})



# A view to redirect to the environment page of a task
def View_Task(request, task_id):
    """
    Purpose:
    - Redirect to the environment page of a specific task.

    Logic:
    - Fetches the task by ID.
    - Extracts the associated Environment ID.
    - Constructs and redirects to the environment URL.

    Input:
    - request: HttpRequest object.
    - task_id: ID of the Task.

    Output:
    - Redirects to the environment page URL.
    """
    task = get_object_or_404(Task, task_id=task_id)

    environment_id = task.environment_id_id
    environment_url = f"/environment/{environment_id}/"

    return redirect(environment_url)