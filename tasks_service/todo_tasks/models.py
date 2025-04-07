
from django.db import models


class TodoList(models.Model):
    user_id = models.IntegerField()
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)
    created_by_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'created_by_id'], name='unique_category_name_per_user')
        ]

    def str(self):
        return self.name


class Task(models.Model):
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=1)

    def str(self):
        return self.title

