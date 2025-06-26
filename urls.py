from django.urls import path
from task_manager.views import create_task, list_tasks, get_task_by_id, task_statistics

urlpatterns = [
    path('tasks/create/', create_task, name='task-create'),
    path('tasks/', list_tasks, name='task-list'),
    path('task/<int:task_id>/', get_task_by_id, name='task-detail'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),
]