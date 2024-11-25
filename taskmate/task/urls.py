from django.urls import path

from . import views

app_name = 'task'
urlpatterns = [
    path("viewall/", views.ViewAllTasks, name="view_all_tasks"),
    path('edit/<int:id>/', views.EditTask, name='edit_task'),
    path('delete/<int:id>/', views.DeleteTask, name='delete_task'),
]