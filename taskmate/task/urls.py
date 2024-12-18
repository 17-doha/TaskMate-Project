from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    path("viewall/", views.ViewAllTasks, name="view_all_tasks"),
    path('edit/<int:id>/', views.EditTask, name='edit_task'),
    path('delete/<int:id>/', views.DeleteTask, name='delete_task'),
    path('create/', views.CreateTask, name='create_task'),
    path('search_task/', views.search_task, name='search_task'),
    path('<int:task_id>/', views.View_Task, name='view_task'),
    # path("send-reminders/", views.send_deadline_notifications, name="send_deadline_notifications"),
]