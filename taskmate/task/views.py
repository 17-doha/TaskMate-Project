from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
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

    users = User.objects.all()
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
            task.created_by = User.objects.get(id = 10) # default for now
            task.environment_id = Environment.objects.get(environment_id = 1) # defult for dlw2ty till fix 
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