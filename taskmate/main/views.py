from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Q, Count
from task.models import Task
import json
from django.db.models import F

def mainpage(request, user_id):
    session_user_id = request.session.get('user_id')
    if not session_user_id:
        return redirect('/login/')  # Redirect to login page if not logged in

    # Enforce the user to access only their own page
    if int(user_id) != session_user_id:
        return redirect(f'/main/{session_user_id}/')

    current_datetime = now()

    # First set of filtered tasks: Tasks for the user with future deadlines, ordered by nearest deadline
    tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),  ~Q(status="Completed"),
        deadline__gt=current_datetime
    ).order_by('deadline')[:4]

    # Add environment details to the first set of tasks
    tasks_with_environment = [
        {
            'task': task,
            'environment_name': task.environment_id.label if task.environment_id else "No Environment"
        }
        for task in tasks
    ]

    # Second filtered task set: Tasks sorted by priority and nearest deadline, limit to 2
    priority_order = {
        'high': 1,
        'mid': 2,
        'low': 3
    }
    priority_tasks = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id),  ~Q(status="Completed") ,
        deadline__gt=current_datetime,
       
    ).annotate(
        priority_order=F('priority')  # Replace 'priority' with the actual priority field name
    ).order_by(
        'priority_order',  # Sort by priority order (high -> mid -> low)
        'deadline'         # Then by nearest deadline
    )[:2]
    

    priority_tasks_with_environment = [
        {
            'task': task,
            'environment_name': task.environment_id.label if task.environment_id else "No Environment",
            'due_date': task.deadline,
            'priority': task.priority
        }
        for task in priority_tasks
    ]
    print(priority_tasks_with_environment)

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

    # Calculate task counts and done ratios by environment
    environment_stats = Task.objects.filter(
        Q(assigned_to=user_id) | Q(created_by=user_id)
    ).values('environment_id__label').annotate(
        total_tasks=Count('pk'),
        done_tasks=Count('pk', filter=Q(status=Task.COMPLETED)),
        done_ratio=F('done_tasks') * 1.0 / F('total_tasks')
    ).order_by('-done_ratio')[:3]

    # Serialize environment_stats to JSON
    environment_stats_json = json.dumps(list(environment_stats))

    # Pass context to the template
    context = {
        'tasks_with_environment': tasks_with_environment,  # First filtered tasks
        'priority_tasks': priority_tasks_with_environment,                 # Second filtered tasks
        'task_counts': {
            'todo': task_counts.get('todo_count', 0),
            'in_progress': task_counts.get('in_progress_count', 0),
            'done': task_counts.get('done_count', 0),
            'total': total_tasks,
        },
        'total_tasks': total_tasks,
        'environment_stats': environment_stats_json,  # Add environment_stats to the context
    }

    # print(environment_stats_json)  # Debugging output
    return render(request, 'mainpage.html', context)
