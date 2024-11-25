from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    # view all tasks page
    path("viewall/", views.ViewAllTasks, name="view_all_tasks"),
    # edit task page
    path('edit/<int:id>/', views.EditTask, name='edit_task'),
    # delete task (unhash for testing)
    # path('delete/<int:id>/', views.DeleteTask, name='delete_task'),
]