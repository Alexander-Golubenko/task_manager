
from rest_framework.routers import DefaultRouter
from django.urls import path
from task_manager.views import (
    task_statistics,
    TaskRetrieveUpdateDestroyAPIView,
    TaskListCreateAPIView,
    SubTaskListCreateAPIView,
    SubTaskRetrieveUpdateDestroyAPIView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = router.urls + [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    #path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),
    path('subtasks/', SubTaskListCreateAPIView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskRetrieveUpdateDestroyAPIView.as_view(), name='subtask-detail'),
]