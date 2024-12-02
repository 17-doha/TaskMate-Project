from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
from environment.models import Environment
from django.contrib import messages


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
    queryset = Task.objects.all().annotate(
        priority_order=Case(
            When(priority=Task.HIGH, then=Value(1)),
            When(priority=Task.MEDIUM, then=Value(2)),
            When(priority=Task.LOW, then=Value(3)),
            default=Value(4),  # Default case if priority is not recognized
            output_field=IntegerField()  # Set the output field type
        )
    ).order_by('priority_order', 'deadline')  # First by priority, then by deadline
    
    print(len(queryset))  # Debugging: Print the number of tasks
    context = {
        "tasks": queryset,
    }
    return render(request, 'task/view_all.html', context)


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
            return redirect('task:view_all_tasks')
    else:
        form = TaskEditForm(instance=task)

    users = User.objects.all()
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
    task.delete()
    return redirect('task:view_all_tasks')


# A view to create a new task
def CreateTask(request):
    """
    Purpose:
    - Create a new task.

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
            task.created_by = User.objects.get(id=15)  # Default user for now
            task.environment_id = Environment.objects.get(environment_id=6)  # Default environment

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
    Purpose:
    - Search for tasks based on content.

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