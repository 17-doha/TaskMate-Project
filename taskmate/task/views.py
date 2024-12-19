from django.shortcuts import render,get_object_or_404, redirect
from .models import Task, Environment
from .forms import TaskEditForm, TaskCreateForm
from signup.models import User
from environment.models import Environment
from django.contrib import messages
from environment.models import Table
from django.core.mail import send_mail



user_id = 1

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
    queryset = Task.objects.all()
    print(len(queryset))  # Debugging: Print the number of tasks
    context = {
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
    env_id = task.environment_id_id
    task.delete()
    return  redirect(f'/environment/{env_id}/')


# A view to create a new task
def CreateTask(request,env_id):
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

    # Get all users to choose from ###### note will be chamged when the user can access env model is made
    users = User.objects.all()

    return render(request, 'task/create_task.html', {
        'users': users,
        'environment_id': env_id,
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



def send_task_assignment_email(task, assigned_to_username):
    try:
        assigned_to_user = User.objects.get(username=assigned_to_username)
        recipient_email = assigned_to_user.email
        
        print(f"Sending email to: {recipient_email}")  # Debugging
        
        subject = f"New Task Assigned: {task.assigned_to.username}"
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
            'noreply@taskmate.com',  # Sender's email
            [recipient_email],  # Recipient's email
            fail_silently=False,
        )
        print("Email sent successfully.")
    except User.DoesNotExist:
        print(f"User with username {assigned_to_username} does not exist.")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")


def send_task_completion_email(task):
    try:
        # Access the environment through the foreign key
        environment = task.environment_id  # Assuming `environment_id` is the ForeignKey in the Task model

        if not environment:
            raise ValueError("Task is not associated with any environment.")

        # Access the admin of the environment
        environment_admin = environment.admin
        if not environment_admin:
            raise ValueError("The environment does not have an admin assigned.")

        recipient_email = environment_admin.email
        print(f"Admin fetched: {environment_admin.username}, Email: {recipient_email}")  # Debugging

        # Prepare and send the email
        subject = f"Task Completed: {task.content}"
        message = (
            f"Hello {environment_admin.username},\n\n"
            f"The task '{task.content}' has been marked as completed.\n\n"
            f"Environment: {environment.label}\n"
            "Please log in to view the task details.\n\n"
            "Best regards,\nTask Management System"
        )

        send_mail(
            subject,
            message,
            'noreply@taskmate.com',  # Sender's email
            [recipient_email],  # Recipient's email
            fail_silently=False,
        )
        print("Completion email sent successfully.")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except User.DoesNotExist:
        print("Admin user does not exist.")
    except Exception as e:
        print(f"An error occurred while sending completion email: {e}")
