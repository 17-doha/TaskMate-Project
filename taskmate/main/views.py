from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Q, Count, F
from task.models import Task
import json
from environment.models import Environment


def mainpage(request, user_id):
    """
    Handles the main page for a user, displaying their tasks and task statistics.

    If the user is not logged in, redirects to the login page.
    If the user_id in the session does not match the user_id in the URL path, redirects to the main page with the session user_id.

    Queries the task table to get the tasks for the user, grouped by environment and ordered by deadline.
    Queries the task table to get the priority tasks for the user, grouped by environment and ordered by deadline.
    Queries the task table to get the count of tasks for the user, grouped by status.
    Queries the environment table to get environment statistics for the user.
    
    Renders the mainpage.html template with the context containing the tasks, task counts, total tasks, and environment statistics.
    """
    session_user_id = request.session.get('user_id')
    if not session_user_id:
        return redirect('/login/')
    if int(user_id) != session_user_id:
        return redirect(f'/main/{session_user_id}/')

    current_datetime = now()

    tasks_with_environment = get_tasks_with_environment(user_id, current_datetime)
    priority_tasks_with_environment = get_priority_tasks_with_environment(user_id, current_datetime)
    task_counts, total_tasks = get_task_counts(user_id)
    environment_stats_json = get_environment_stats(user_id)

    user_id = request.session.get('user_id')
    environments = Environment.objects.filter(admin_id=user_id)

    context = {
        'tasks_with_environment': tasks_with_environment,
        'priority_tasks': priority_tasks_with_environment,
        'task_counts': {
            'todo': task_counts.get('todo_count', 0),
            'in_progress': task_counts.get('in_progress_count', 0),
            'done': task_counts.get('done_count', 0),
            'total': total_tasks,
        },
        'total_tasks': total_tasks,
        'environment_stats': environment_stats_json,
        'environments': environments
    }
    

    return render(request, 'mainpage.html', context)

def get_task_counts(user_id):
    """Aggregate task counts by status."""
    task_counts = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id)
    ).aggregate(
        todo_count=Count('pk', filter=Q(status=Task.PENDING)),
        in_progress_count=Count('pk', filter=Q(status=Task.IN_PROGRESS)),
        done_count=Count('pk', filter=Q(status=Task.COMPLETED)),
    )

    total_tasks = sum(
        task_counts.get(key, 0) for key in ['todo_count', 'in_progress_count', 'done_count']
    )

    return task_counts, total_tasks


def get_priority_tasks_with_environment(user_id, current_datetime):
    """Fetch tasks prioritized by priority and nearest deadline, with environment details."""
    priority_tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),
        ~Q(status="Completed"),
        deadline__gt=current_datetime,
    ).annotate(
        priority_order=F('priority')  
    ).order_by(
        'priority_order', 
        'deadline'
    )[:2]

    return [
        {
            'task': task,
            'environment_name': task.environment_id.label if task.environment_id else "No Environment",
            'due_date': task.deadline,
            'priority': task.priority
        }
        for task in priority_tasks
    ]




def get_tasks_with_environment(user_id, current_datetime):
    """Fetch tasks with future deadlines and include environment details."""
    tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),
        ~Q(status="Completed"),
        deadline__gt=current_datetime
    ).order_by('deadline')[:4]

    return [
        {
            'task': task,
            'environment_name': task.environment_id.label if task.environment_id else "No Environment"
        }
        for task in tasks
    ]





def get_environment_stats(user_id):
    """Calculate task counts and done ratios by environment and return as JSON."""
    environment_stats = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id)
    ).values('environment_id__label').annotate(
        total_tasks=Count('pk'),
        done_tasks=Count('pk', filter=Q(status=Task.COMPLETED)),
        done_ratio=F('done_tasks') * 1.0 / F('total_tasks')
    ).order_by('-done_ratio')[:3]

    return json.dumps(list(environment_stats))
