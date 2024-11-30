from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Login, Environment
from .forms import TaskEditForm, TaskCreateForm
from django.contrib.auth.models import User
from environment.models import Environment
from django.contrib import messages


#A view to show all tasks with the edit and delete buttons for testing
def ViewAllTasks(request):
    queryset = Task.objects.all()
    print(len(queryset))
    context={
        "tasks": queryset,
    }
    return render(request,'task/view_all.html',context)


# A view to allow edit in another page 
def EditTask(request, id):
    task = get_object_or_404(Task, task_id=id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task:view_all_tasks')
    else:
        form = TaskEditForm(instance=task)

    users = Login.objects.all()
    return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


# A view to delete tasks on click 
def DeleteTask(request, id):
    task = get_object_or_404(Task, task_id=id)
    task.delete()
    return redirect('task:view_all_tasks')


def CreateTask(request):
    if request.method == "POST":
        form = TaskCreateForm(request.POST)
        
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = Login.objects.get(id = 1) # default for now
            task.environment_id = Environment.objects.get(environment_id = 3) # defult for dlw2ty till fix 
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('environment:index') 
        else:
            messages.error(request, 'There was an error creating the task. Please try again.')

    # Get all users to choose from
    users = Login.objects.all()

    return render(request, 'task/create_task.html', {
        'users': users,
    })


def search_task(request):
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


def View_Task(request, task_id):
    # Fetch the task by its ID
    task = get_object_or_404(Task, task_id=task_id)

    # Get the environment ID (reference the id field of the related Environment object)
    environment_id = task.environment_id_id  # Access the ID of the related Environment object
    print('environment_id', environment_id)

    # Construct the correct URL to redirect to
    environment_url = f"/environment/{environment_id}/"  # Use the environment ID in the URL

    # Redirect to the environment page by IDid
    return redirect(environment_url)