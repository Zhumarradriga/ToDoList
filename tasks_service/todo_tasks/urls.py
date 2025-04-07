
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoListViewSet, CategoryViewSet, TaskViewSet, InitializeUserView

router = DefaultRouter()
router.register(r'todo-lists', TodoListViewSet, basename='todolist')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('initialize_user/', InitializeUserView.as_view(), name='initialize_user'),
]