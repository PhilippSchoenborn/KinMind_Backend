from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BoardViewSet, TaskViewSet, AssignedToMeTasksView, ReviewingTasksView,
    CommentListCreateView, CommentDeleteView
)

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/assigned-to-me/', AssignedToMeTasksView.as_view(), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', ReviewingTasksView.as_view(), name='tasks-reviewing'),
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view(), name='task-comments'),
    path('tasks/<int:task_id>/comments/<int:pk>/', CommentDeleteView.as_view(), name='task-comment-delete'),
]
