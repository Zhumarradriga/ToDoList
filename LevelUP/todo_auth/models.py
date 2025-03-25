from django.db import models
from  django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    epx_points=models.PositiveIntegerField(default=0)
    create_at=models.DateTimeField(auto_now_add=True)
    avatar_url=models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        db_table='user'

    def __str__(self):
        return self.username
class UserStats(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    stat=models.ForeignKey('todo_stats.Stat', on_delete=models.CASCADE)
    value=models.PositiveIntegerField(default=0)

    class Meta:
        db_table='user_stats'
        unique_together=('user','stat')
    def __str__(self):
        return f"{self.user.username} - {self.stat.name}: {self.value}"
