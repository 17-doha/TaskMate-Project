from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Login, Environment
from .forms import TaskEditForm, TaskCreateForm
from django.contrib.auth.models import User
from environment.models import Environment
from django.contrib import messages


#A view to show all tasks with the edit and delete buttons
def ViewAllTasks(request):
    queryset = Task.objects.all()
    print(len(queryset))
    context={
        "tasks": queryset,
    }
    return render(request,'task/view_all.html',context)


# A view to allow edit in another page (pop up later)
def EditTask(request, id):
    task = get_object_or_404(Task, task_id=id)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('environment:index')
    else:
        form = TaskEditForm(instance=task)

    users = Login.objects.all()
    return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


# A view to delete tasks on immediate click 
def DeleteTask(request, id):
    task = get_object_or_404(Task, task_id=id)
    task.delete()
    return redirect('environment:indexa')

def CreateTask(request):
    if request.method == "POST":
        # Create a form instance 
        form = TaskCreateForm(request.POST)
        
        if form.is_valid():
            # If the form is valid save the new task
            task = form.save(commit=False)
            task.created_by = Login.objects.get(id = 1) # Automatically assign the logged-in user as the creator
            task.environment_id = Environment.objects.get(environment_id = 3) # defult for dlw2ty till fix 
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('environment:index') 
        else:
            messages.error(request, 'There was an error creating the task. Please try again.')

    # Get all users and environments to choose from
    users = Login.objects.all()
    environments = Environment.objects.all()

    return render(request, 'task/create_task.html', {
        'users': users,
        'environments': environments
    })