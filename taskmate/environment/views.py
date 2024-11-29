from django.shortcuts import render, get_object_or_404
from .models import Environment, Table
from django.http import JsonResponse
from task.models import Task
import json
# Create your views here.
mapping = {
    'To Do' : 'Pending',
    'In Progress': 'In Progress',
    'Done': 'Completed'
}

def index(request):
    return render(request, "environment/index.html")    


def ViewTableTask(request, environment_id):
    # Retrieve the environment by ID
    environment = get_object_or_404(Environment, environment_id=environment_id)
    
    # Filter tasks associated with this environment
    tasks = Task.objects.filter(environment_id=environment)
    
    # Categorize tasks based on their status
    todo_tasks = tasks.filter(status='Pending')
    inprogress_tasks = tasks.filter(status='In Progress')
    done_tasks = tasks.filter(status='Completed')
    print(todo_tasks)
    print(inprogress_tasks)
    print(done_tasks)
       
    # Prepare context for the template
    context = {
        "environment": environment,
        "todo_tasks": todo_tasks,
        "inprogress_tasks": inprogress_tasks,
        "done_tasks": done_tasks,
    }
    
    return render(request, 'environment/index.html', context)





def dragAndDrop(request, environment_id):

    print(f"Environment ID: {environment_id}")
    print('entered')
    if request.method == "POST":
        # Get JSON data from request body
        data = json.loads(request.body)
        task_id = data.get('task_id')
        target_table_name = data.get('target_table')

        # Get the task object from the database
        task = get_object_or_404(Task, task_id=task_id)

        # Get the environment (from URL parameter or task object)
        environment = task.environment_id

        # Assuming you have a `Table` model (or something similar) that defines task status columns
        # Example logic (you may need to adjust depending on your actual Table model)
        target_table = get_object_or_404(Table, environment=environment, label=target_table_name)

        # Update the task's table ID and status
        task.table = target_table
        task.status = mapping[target_table_name]  # Update the status to match the table name
        task.table_id = target_table.table_id
        print(target_table.table_id)
        task.save()

        # Return success response
        return JsonResponse({'status': 'success', 'message': 'Task moved successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})



