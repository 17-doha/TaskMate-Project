from django.shortcuts import render,  redirect
from django.utils.timezone import now
from django.db.models import Q, Count
from task.models import Task

def mainpage(request, user_id):
    session_user_id = request.session.get('user_id')
    if not session_user_id:
        return redirect('/login/')  # Redirect to login page if not logged in

    # Enforce the user to access only their own page
    if int(user_id) != session_user_id:
        return redirect(f'/main/{session_user_id}/')
    current_datetime = now()

    # Fetch tasks for the user with future deadlines, ordered by nearest deadline
    tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),
        deadline__gt=current_datetime
    ).order_by('deadline')[:4]

    # Add environment details to tasks
    tasks_with_environment = [
        {
            'task': task,
            'environment_name': task.environment_id.label if task.environment_id else "No Environment"
        }
        for task in tasks
    ]

    # Aggregate task counts by status
    task_counts = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id)
    ).aggregate(
        todo_count=Count('pk', filter=Q(status=Task.PENDING)),
        in_progress_count=Count('pk', filter=Q(status=Task.IN_PROGRESS)),
        done_count=Count('pk', filter=Q(status=Task.COMPLETED)),
    )

    # Calculate total tasks
    total_tasks = sum(
        task_counts.get(key, 0) for key in ['todo_count', 'in_progress_count', 'done_count']
    )


    # Pass context to the template
    context = {
        'tasks_with_environment': tasks_with_environment,
        'task_counts': task_counts,
        'total_tasks': total_tasks,
        'task_counts': {
            'todo': task_counts.get('todo_count', 0),
            'in_progress': task_counts.get('in_progress_count', 0),
            'done': task_counts.get('done_count', 0),
            'total': total_tasks,
        }
    }


    return render(request, 'mainpage.html', context)


