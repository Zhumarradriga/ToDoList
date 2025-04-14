from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import TodoList, Category, Task
from .serializers import TodoListSerializer, CategorySerializer, TaskSerializer
from .authentication import CustomJWTAuthentication

class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TodoList.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(created_by_id=self.request.user) | Category.objects.filter(is_default=True)

    def perform_create(self, serializer):
        serializer.save(created_by_id=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(todo_list__user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class InitializeUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        Category.objects.create(name="Работа", is_default=True, created_by_id=user_id)
        Category.objects.create(name="Личное", is_default=True, created_by_id=user_id)
        return Response({'status': 'success'})
