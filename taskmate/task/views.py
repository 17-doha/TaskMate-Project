from django.shortcuts import render,get_object_or_404, redirect
from .models import Task
from .forms import TaskForm  

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
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task:view_all_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/edit_task.html', {'form': form})


# A view to delete tasks on immediate click 
def DeleteTask(request, id):
    task = get_object_or_404(Task, task_id=id)
    task.delete()
    return redirect('task:view_all_tasks')