from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
from environment.models import Environment
from django.contrib import messages


# A view to show all tasks with the edit and delete buttons for testing
def ViewAllTasks(request):
    """
    Fetches all tasks and displays them in a template along with options to edit or delete.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.

    Returns:
    - Renders the 'task/view_all.html' template with:
        - 'tasks': Queryset of all Task objects.
    """
    queryset = Task.objects.all()
    print(len(queryset))  # Debugging: Print the number of tasks
    context = {
        "tasks": queryset,
    }
    return render(request, 'task/view_all.html', context)


# A view to allow editing a task on another page
def EditTask(request, id):
    """
    Handles task editing functionality.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.
    - id: ID of the Task object to be edited.

    Returns:
    - If the request method is POST:
        - Saves the updated Task object and redirects to 'view_all_tasks'.
    - If the request method is not POST:
        - Renders the 'task/edit_task.html' template with:
            - 'form': Pre-filled TaskEditForm for the task.
            - 'task': The Task object to be edited.
            - 'users': Queryset of all User objects.
    """
    task = get_object_or_404(Task, task_id=id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task:view_all_tasks')
    else:
        form = TaskEditForm(instance=task)

    users = User.objects.all()
    return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


# A view to delete tasks on click
def DeleteTask(request, id):
    """
    Deletes a specific task based on its ID.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.
    - id: ID of the Task object to be deleted.

    Returns:
    - Redirects to 'view_all_tasks' after deletion.
    """
    task = get_object_or_404(Task, task_id=id)
    task.delete()
    return redirect('task:view_all_tasks')


# A view to create a new task
def CreateTask(request):
    """
    Handles task creation functionality.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.

    Returns:
    - If the request method is POST:
        - Saves the new Task object and redirects to 'environment:index'.
        - Displays a success or error message.
    - If the request method is not POST:
        - Renders the 'task/create_task.html' template with:
            - 'users': Queryset of all User objects.
    """
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = User.objects.get(id=10)  # Default user for now
            task.environment_id = Environment.objects.get(environment_id=1)  # Default environment
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('environment:index')
        else:
            messages.error(request, 'There was an error creating the task. Please try again.')

    # Get all users to choose from
    users = User.objects.all()

    return render(request, 'task/create_task.html', {
        'users': users,
    })


# A view to search for tasks based on content
def search_task(request):
    """
    Handles search functionality for tasks.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.

    Returns:
    - If the request method is POST:
        - Renders the 'search_environment.html' template with:
            - 'searched': The search term entered by the user.
            - 'tasks': Queryset of Task objects whose 'content' contains the search term.
    - If the request method is not POST:
        - Renders the 'search_environment.html' template with an empty context.
    """
    if request.method == "POST":
        searched = request.POST['searched']
        print(f"Search Term: {searched}")  # Debugging line
        tasks = Task.objects.filter(content__contains=searched)
        
        # Debugging: Print task IDs to check if they're valid
        for task in tasks:
            print(f"Task ID: {task.task_id}, Content: {task.content}")
        
        return render(request, 'search_environment.html', {'searched': searched, 'tasks': tasks})
    else:
        return render(request, 'search_environment.html', {})


# A view to redirect to the environment page of a task
def View_Task(request, task_id):
    """
    Redirects to the environment page of a specific task.

    Parameters:
    - request: HttpRequest object that contains metadata about the request.
    - task_id: ID of the Task object.

    Returns:
    - Redirects to the environment page using the environment ID related to the task.
    """
    task = get_object_or_404(Task, task_id=task_id)

    environment_id = task.environment_id_id
    environment_url = f"/environment/{environment_id}/"

    return redirect(environment_url)