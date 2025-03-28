from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class TodoList(models.Model):
    user = models.ForeignKey('todo_users.Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Todo_lists"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    created_by = models.ForeignKey('todo_users.Users', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by'], name='unique_category_name_per_user')
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        db_table = 'Tasks'

    def __str__(self):
        return self.title
