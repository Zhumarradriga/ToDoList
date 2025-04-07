from  rest_framework import serializers
from .models import TodoList, Category, Task

class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model=TodoList
        fields=['id', 'title', 'created_at', 'updated_at']
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'name', 'is_default', 'created_at']
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['id', 'todo_list', 'category', 'title', 'description', 'is_completed', 'created_at', 'due_date', 'priority']
