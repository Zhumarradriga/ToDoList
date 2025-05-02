from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import TodoList, Category, Task
from .serializers import TodoListSerializer, CategorySerializer, TaskSerializer
from .authentication import CustomJWTAuthentication
from logger import logger

class TodoListViewSet(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение списка задач для пользователя {self.request.user.id}")
        return TodoList.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        logger.info(f"Создание нового списка задач для пользователя {self.request.user.id}")
        serializer.save(user_id=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение категорий для пользователя {self.request.user.id}")
        return Category.objects.filter(created_by_id=self.request.user) | Category.objects.filter(is_default=True)

    def perform_create(self, serializer):
        logger.info(f"Создание новой категории для пользователя {self.request.user.id}")
        serializer.save(created_by_id=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        logger.debug(f"Получение задач для пользователя {self.request.user.id}")
        return Task.objects.filter(todo_list__user_id=self.request.user)

    def perform_create(self, serializer):
        logger.info(f"Создание новой задачи для пользователя {self.request.user.id}")
        serializer.save()

class InitializeUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        logger.info(f"Инициализация пользователя {user_id}: создание дефолтных категорий")
        try:
            Category.objects.create(name="Работа", is_default=True, created_by_id=user_id)
            Category.objects.create(name="Личное", is_default=True, created_by_id=user_id)
            logger.info(f"Успешно созданы дефолтные категории для пользователя {user_id}")
            return Response({'status': 'success'})
        except Exception as e:
            logger.error(f"Ошибка при создании дефолтных категорий для пользователя {user_id}: {str(e)}")
            return Response({'status': 'error', 'message': str(e)}, status=500)
