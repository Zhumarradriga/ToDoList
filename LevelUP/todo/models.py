from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    xp = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False, unique=True)

    @property
    def level(self):
        return self.xp // 100

    def str(self):
        return f"{self.first_name} {self.last_name} ({self.username})"