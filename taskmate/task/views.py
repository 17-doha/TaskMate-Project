from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
from environment.models import Environment
from django.contrib import messages
from environment.models import Table, UserCanAccess
from django.db.models import Q
from environment.models import UserCanAccess
from django.core.mail import send_mail
from Notification.models import Notification
from environment.models import SearchHistory







# A view to show all tasks with the edit and delete buttons for testing not an actual ui 
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
    queryset = Task.objects.all()

    context={

        "tasks": queryset,
    }
    return render(request, 'task/view_all.html', context)


# A view to allow editing a task on another page
# def EditTask(request, id):
#     """
#     Purpose:
#     - Allow editing of a specific task.

#     Logic:
#     - Fetches the task by ID.
#     - If POST, updates the task with form data and saves.
#     - If not POST, pre-fills the form with the task data.

#     Input:
#     - request: HttpRequest object.
#     - id: ID of the Task to edit.

#     Output:
#     - If POST:
#       - Redirects to 'view_all_tasks'.
#     - Else:
#       - Renders 'task/edit_task.html' with:
#         - 'form': Pre-filled TaskEditForm.
#         - 'task': Task object.
#     """
#     task = get_object_or_404(Task, task_id=id)
#     original_status = task.status  # Store the original status for comparison

#     if request.method == 'POST':
#         form = TaskEditForm(request.POST, instance=task)
#         if form.is_valid():
#             task = form.save(commit=False)

#             # Check if the status changed to "Completed"
#             if original_status != "Completed" and task.status == "Completed":
#                 try:
#                     send_task_completion_email(task)  # Call the email function
#                 except Exception as e:
#                     print(f"Error sending completion email: {e}")
#                     messages.error(request, "Task updated, but the email could not be sent.")

#             task.save()  # Save the updated task
#             env_id = task.environment_id_id
#             return redirect(f'/environment/{env_id}/')
#     else:
#         form = TaskEditForm(instance=task)

#     users = User.objects.all()
#     return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


def EditTask(request, id):

    user_id = request.session.get('user_id')
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
    original_status = task.status  # Store the original status for comparison

    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            print(f"Original Status: {original_status}, Updated Status: {task.status}")  # Debugging

            # Check if the status changed to "Completed"
            if original_status != "COMPLETED" and task.status == "COMPLETED":
                try:
                    print("Status changed to Completed. Sending email...")  # Debugging
                    send_task_completion_email(task)  # Call the email function
                except Exception as e:
                    print(f"Error sending completion email: {e}")
                    messages.error(request, "Task updated, but the email could not be sent.")

            task.save()  # Save the updated task
            env_id = task.environment_id_id
            return redirect(f'/environment/{env_id}/')
    else:
        form = TaskEditForm(instance=task)

    users = User.objects.filter(
        user_access__environment_id=task.environment_id,  
        user_access__type_of_accessibility__in=['subadmin', 'Admin'],  
        user_access__invitation_status='Accepted'  
        )
    user_queryset = User.objects.filter(id=user_id) 
    users = users | user_queryset
    return render(request, 'task/edit_task.html', {'form': form, 'task': task, 'users': users})


# A view to delete tasks on click
def DeleteTask(request, id):
    user_id = request.session.get('user_id')
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
    env_id = task.environment_id_id
    task.delete()
    return  redirect(f'/environment/{env_id}/')


# A view to create a new task
def CreateTask(request,env_id):
    user_id = request.session.get('user_id')
    """
    Purpose:
    - Create a new  task.

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
            task.created_by = User.objects.get(id=user_id)  # Default user for now
            task.environment_id = Environment.objects.get(environment_id=env_id)  
            table = get_object_or_404(Table, environment_id=env_id, label="To Do")
            task.table = table

            task.save()
            
            if task.assigned_to:
                try:
                    send_task_assignment_email(task, task.assigned_to.username)
                except Exception as e:
                    print(f"Error sending email: {e}")
                    messages.error(request, "Task created, but the email could not be sent.")

            messages.success(request, 'Task created successfully!')
            return redirect(f'/environment/{env_id}/')
        else:
            messages.error(request, 'There was an error creating the task. Please try again.')

    # Get all users to choose from 
    users = User.objects.filter(
        user_access__environment_id=Environment.objects.get(environment_id=env_id)  ,  
        user_access__type_of_accessibility__in=['subadmin', 'Admin'],  
        user_access__invitation_status='Accepted'  
    )
    user_queryset = User.objects.filter(id=user_id) 
    users = users | user_queryset

    return render(request, 'task/create_task.html', {
        'users': users,
        'environment_id': env_id,
    })


# A view to search for tasks based on content
def search_task(request):
    user_id = request.session.get('user_id')
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
        # Retrieve the search term

        searched = request.POST['searched']

        tasks = Task.objects.filter(
            Q(content__contains=searched, created_by_id=user_id) | Q(content__contains=searched, assigned_to_id=user_id)
        )
        
        user = User.objects.get(id=user_id)
        if not SearchHistory.objects.filter(content=searched, user_id=user).exists():
            SearchHistory.objects.create(content=searched, user_id=user)

        
        return render(request, 'search_environment.html', {'searched': searched, 'tasks': tasks})
    else:
        return render(request, 'search_environment.html', {})


# A view to redirect to the environment page of a task
def View_Task(request, task_id):
    user_id = request.session.get('user_id')
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

#send email for the assigned user
def send_task_assignment_email(task, assigned_to_username):
    try:
        assigned_to_user = User.objects.get(username=assigned_to_username)
        recipient_email = assigned_to_user.email
        
        print(f"Sending email to: {recipient_email}")  
        
        subject = f"New Task Assigned: {task.assigned_to.username}"
        #preparing mail 
        message = (
            f"Hello {assigned_to_user.username},\n\n"
            f"You have been assigned a new task:\n\n"
            f"Task: {task.content}\n"
            "Please log in to your account to view more details.\n\n"
            "Best regards,Your Task Management System"
        )
        send_mail(
            subject,
            message,
            'noreply@taskmate.com',   #the application is the sender
            [recipient_email], 
            fail_silently=False,
        ) 
        #b7ot record fel notification database
        Notification.objects.create(
            content=f"You have been assigned a new task: {task.content}",
            receiver=assigned_to_user,
            status="UNREAD"
        )
        print("Email sent successfully.")
    except User.DoesNotExist:
        print(f"User with username {assigned_to_username} does not exist.")
    except Exception as e:
        print(f"There is an error through sending the email: {e}")


def send_task_completion_email(task):
    try:
        # baged id of the environment nm el foreign key elly fel task model
        environment = task.environment_id

        if not environment:
            raise ValueError("Task is not exists in this environment.")

        #baged el admin 3lshan ab3tlo en el task 5lst
        environment_admin = environment.admin
        if not environment_admin:
            raise ValueError("The environment does not have an admin")

        recipient_email = environment_admin.email

        #preparing mail
        subject = f"Task Completed: {task.content}"
        message = (
            f"Hello {environment_admin.username},\n\n"
            f"The task '{task.content}' has been marked as completed.\n\n"
            f"Environment: {environment.label}\n"
            "Please log in to view the task details.\n\n"
            "Best regards,\nTask Management System"
        )
        #bb3at el mail
        send_mail(
            subject,
            message,
            'noreply@taskmate.com',  # Sender's email
            [recipient_email],  # Recipient's email
            fail_silently=False,
        )
        #b7ot record in database
        Notification.objects.create(
            content=f"The task '{task.content}' has been marked as completed.",
            receiver=environment_admin,
            status="UNREAD"
        )
        print("Completion email sent successfully.")
    except User.DoesNotExist:
        print("There is an error through sending the email")

