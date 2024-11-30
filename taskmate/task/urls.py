from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    ## view all tasks page
    path("viewall/", views.ViewAllTasks, name="view_all_tasks"),
    ## edit task page
    path('edit/<int:id>/', views.EditTask, name='edit_task'),
    ## delete task (unhash for testing)
    path('delete/<int:id>/', views.DeleteTask, name='delete_task'),
    path('create/', views.CreateTask, name='create_task'),
    path('search_task/', views.search_task, name='search_task'),
    path('<int:task_id>/', views.View_Task, name='view_task'),
    
]